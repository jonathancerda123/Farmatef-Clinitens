from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import FileResponse, Http404
from django.db import transaction
from django.db.models import Case, Exists, OuterRef, Prefetch, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, TemplateView
from urllib.parse import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin

from core.mixins import PermitsPositionMixin
from core.permissions import cargo, recetas_visibles_para_docente
from .codigos_barras import ancho_code128, codigo_para_etiqueta, imagen_code128, patron_code128
from .comprobantes import comprobante_dispensacion
from .forms import (
    EntregaLineaFormSet,
    EtiquetaLoteForm,
    LoteInventarioForm,
    MedicamentoForm,
    RecetaForm,
    RecetaLineaFormSet,
    RespuestaRecetaForm,
)
from .inventario import TIPOS_ALERTA, filtrar_inventario, inventario_visible
from .models import Dispensacion, DispensacionLote, LoteInventario, Medicamento, Receta, RecetaLinea, RespuestaReceta
from .services import eliminar_receta, entregar_receta, lotes_de_practica, responder_receta


class EtiquetaBaseView(View):
    template_name = "pages/farmatef/etiquetado.html"
    preview_template_name = "pages/farmatef/_etiqueta_preview.html"
    uso = None

    def render_page(self, request, form, etiqueta=None):
        solo_vista_previa = request.method == "POST" and request.headers.get("X-Label-Preview") == "1"
        return render(
            request,
            self.preview_template_name if solo_vista_previa else self.template_name,
            {
                "form": form,
                "etiqueta": etiqueta,
                "copias": range(1, etiqueta["copias"] + 1) if etiqueta else (),
                "uso": self.uso,
                "solo_vista_previa": solo_vista_previa,
            },
        )

    def get(self, request, *args, **kwargs):
        return self.render_page(request, self.get_form(request))

    def post(self, request, *args, **kwargs):
        return self.render_preview(request, self.get_form(request, request.POST))

    def render_preview(self, request, form):
        if not form.is_valid():
            return self.render_page(request, form=form)
        medicamento = form.cleaned_data["medicamento"]
        lote = form.cleaned_data["lote"]
        return self.render_page(
            request,
            form=form,
            etiqueta={
                "medicamento": medicamento,
                "lote": lote,
                "ancho_mm": form.cleaned_data["ancho_mm"],
                "alto_mm": form.cleaned_data["alto_mm"],
                "copias": form.cleaned_data["copias"],
                "codigo": form.cleaned_data["codigo"],
                "ancho_codigo": form.cleaned_data["ancho_codigo"],
                "imagen_codigo": imagen_code128(form.cleaned_data["patron_codigo"]),
            },
        )


class EtiquetadoView(PermitsPositionMixin, EtiquetaBaseView):
    def get_form(self, request, data=None):
        return EtiquetaLoteForm(data, actor=request.user)


class InventarioView(PermitsPositionMixin, TemplateView):
    template_name = "pages/farmatef/inventario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medicamentos = inventario_visible(self.request.user)
        clasificaciones = (
            medicamentos.exclude(clasificacion="").order_by("clasificacion")
            .values_list("clasificacion", flat=True).distinct()
        )
        busqueda = self.request.GET.get("q", "").strip()[:160]
        clasificacion = self.request.GET.get("clasificacion", "")[:120]
        alerta = self.request.GET.get("alerta", "")
        if clasificacion:
            medicamentos = medicamentos.filter(clasificacion=clasificacion)
        context.update(
            medicamentos=list(filtrar_inventario(medicamentos.prefetch_related("lotes"), busqueda, alerta)),
            busqueda=busqueda,
            clasificacion=clasificacion,
            clasificaciones=clasificaciones,
            alerta=alerta if alerta in TIPOS_ALERTA else "",
            titulo_alerta=TIPOS_ALERTA.get(alerta, ("", None))[0],
        )
        return context

    def post(self, request, *args, **kwargs):
        return RegistroInventarioView.as_view()(request, *args, **kwargs)


class RegistroInventarioView(PermitsPositionMixin, TemplateView):
    template_name = "pages/farmatef/registro_inventario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form_medicamento" not in context:
            context["form_medicamento"] = MedicamentoForm(
                prefix="medicamento", actor=self.request.user
            )
        if "form_lote" not in context:
            context["form_lote"] = LoteInventarioForm(
                prefix="lote", actor=self.request.user
            )
        return context

    def post(self, request, *args, **kwargs):
        if "crear_medicamento" in request.POST:
            form = MedicamentoForm(
                request.POST, prefix="medicamento", actor=request.user
            )
            if form.is_valid():
                medicamento = form.save(commit=False)
                medicamento.creado_por = request.user
                medicamento.save()
                messages.success(request, "Medicamento registrado.")
                return redirect("farmatef:inventario")
            return self.render_to_response(
                self.get_context_data(form_medicamento=form)
            )

        if "crear_lote" in request.POST:
            form = LoteInventarioForm(
                request.POST, prefix="lote", actor=request.user
            )
            if form.is_valid():
                lote = form.save(commit=False)
                lote.registrado_por = request.user
                lote.save()
                messages.success(request, "Lote de inventario registrado.")
                return redirect("farmatef:inventario")
            return self.render_to_response(self.get_context_data(form_lote=form))

        messages.error(request, "No se reconoció la operación solicitada.")
        return redirect("farmatef:registro_inventario")


class RecetasView(PermitsPositionMixin, View):
    template_name = "pages/farmatef/recetas.html"

    def get_queryset(self):
        return recetas_visibles_para_docente(
            Receta.objects.prefetch_related(
                "lineas__medicamento",
                "dispensaciones__lotes_usados__lote",
                "dispensaciones__lotes_usados__linea__medicamento",
            ),
            self.request.user,
        )

    def render_page(self, request, *, receta_form=None, lineas_formset=None, receta=None):
        visibles = self.get_queryset()
        busqueda = request.GET.get("q", "").strip()[:32]
        coincidencias = []
        if busqueda:
            coincidencias = list(
                visibles.filter(numero__icontains=busqueda)
                .order_by(
                    Case(
                        When(numero__iexact=busqueda, then=Value(0)),
                        When(numero__istartswith=busqueda, then=Value(1)),
                        default=Value(2),
                    ),
                    "numero",
                )
                .values("numero")[:13]
            )
        if receta is None:
            numero = request.GET.get("numero", "").strip().upper()
            if numero:
                receta = visibles.select_related("curso").filter(numero=numero).first()
                if not receta:
                    messages.error(request, "No se encontró una receta con ese número en tu ámbito de acceso.")
        context = {
            "receta_form": receta_form or RecetaForm(actor=request.user),
            "lineas_formset": lineas_formset or RecetaLineaFormSet(form_kwargs={"actor": request.user}),
            "tiene_intentos": receta is not None and receta.respuestas_estudiantiles.exists(),
            "receta": receta,
            "busqueda": busqueda,
            "coincidencias": coincidencias[:12],
            "mas_coincidencias": len(coincidencias) > 12,
            "today": timezone.localdate(),
            "historial": visibles.prefetch_related(
                "lineas__medicamento"
            ).annotate(
                tiene_respuestas=Exists(
                    RespuestaReceta.objects.filter(receta_id=OuterRef("pk"))
                ),
                tiene_dispensaciones=Exists(
                    Dispensacion.objects.filter(receta_id=OuterRef("pk"))
                ),
                tiene_unidades_entregadas=Exists(
                    RecetaLinea.objects.filter(
                        receta_id=OuterRef("pk"), unidades_entregadas__gt=0
                    )
                ),
            ).order_by("-creado_en")[:30],
        }
        if receta:
            entrega_formset = EntregaLineaFormSet(
                initial=[
                    {"linea_id": linea.pk, "unidades": linea.unidades_pendientes}
                    for linea in receta.lineas.all()
                ],
                prefix="entrega",
            )
            context["entrega_formset"] = entrega_formset
            context["lineas_entrega"] = list(zip(receta.lineas.all(), entrega_formset.forms))
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        receta_form = RecetaForm(request.POST, actor=request.user)
        lineas_formset = RecetaLineaFormSet(
            request.POST, form_kwargs={"actor": request.user}
        )
        if not receta_form.is_valid() or not lineas_formset.is_valid():
            return self.render_page(request, receta_form=receta_form, lineas_formset=lineas_formset)
        with transaction.atomic():
            receta = Receta.objects.create(
                numero=receta_form.cleaned_data["numero"],
                persona_ficticia=receta_form.cleaned_data["persona_ficticia"],
                vence_el=receta_form.cleaned_data["vence_el"],
                curso=receta_form.cleaned_data["curso"],
                motivo_rechazo_esperado=receta_form.cleaned_data["motivo_rechazo_esperado"],
                sospecha_falsificacion=receta_form.cleaned_data["motivo_rechazo_esperado"] == "FALSIFICACION",
                pista_estudiante=receta_form.cleaned_data["pista_estudiante"].strip(),
                retroalimentacion_docente=receta_form.cleaned_data["retroalimentacion_docente"].strip(),
                creado_por=request.user,
            )
            RecetaLinea.objects.bulk_create([
                RecetaLinea(
                    receta=receta,
                    medicamento=form.cleaned_data["medicamento"],
                    unidades=form.cleaned_data["unidades"],
                    dosis=form.cleaned_data["dosis"],
                    indicaciones=form.cleaned_data["indicaciones"],
                )
                for form in lineas_formset.forms
                if form.cleaned_data.get("medicamento")
            ])
        messages.success(request, f"Receta {receta.numero} asignada al curso {receta.curso.nombre}.")
        return redirect(f"{reverse('farmatef:recetas')}?{urlencode({'numero': receta.numero})}")


class IntentosRecetaView(PermitsPositionMixin, View):
    def get(self, request, receta_id):
        receta = get_object_or_404(
            recetas_visibles_para_docente(Receta.objects.select_related("curso"), request.user),
            pk=receta_id,
        )
        return render(request, "pages/farmatef/intentos_receta.html", {
            "receta": receta,
            "intentos": receta.respuestas_estudiantiles.select_related("estudiante").order_by("-respondida_en", "-pk"),
        })


class EntregarRecetaView(PermitsPositionMixin, View):
    def post(self, request, receta_id, *args, **kwargs):
        numero = recetas_visibles_para_docente(
            Receta.objects.filter(pk=receta_id), request.user
        ).values_list("numero", flat=True).first()
        if not numero:
            messages.error(request, "No se encontró la receta en tu ámbito de acceso.")
            return redirect("farmatef:recetas")
        receta = recetas_visibles_para_docente(
            Receta.objects.prefetch_related("lineas"), request.user
        ).get(pk=receta_id)
        formset = EntregaLineaFormSet(request.POST, prefix="entrega")
        if not formset.is_valid():
            messages.error(request, "Revisa las cantidades elegidas para esta entrega.")
            query = urlencode({"numero": numero})
            return redirect(f"{reverse('farmatef:recetas')}?{query}")
        cantidades = {
            form.cleaned_data["linea_id"]: form.cleaned_data["unidades"]
            for form in formset.forms
        }
        try:
            receta = entregar_receta(receta_id, request.user, cantidades)
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
        else:
            messages.success(request, f"Entrega simulada registrada para {receta.numero}.")
        query = urlencode({"numero": numero}) if numero else ""
        return redirect(f"{reverse('farmatef:recetas')}?{query}" if query else "farmatef:recetas")


class EliminarRecetaView(PermitsPositionMixin, View):
    def post(self, request, receta_id, *args, **kwargs):
        try:
            numero = eliminar_receta(receta_id, request.user)
        except ValidationError as exc:
            for error in exc.messages:
                messages.error(request, error)
        else:
            messages.success(request, f"Se eliminó la receta simulada {numero}.")
        return redirect("farmatef:recetas")


class EstudianteFarmaMixin(LoginRequiredMixin):
    login_url = "account_login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not request.user.is_active or cargo(request.user) != "RESTRICTED":
            raise Http404("La práctica está disponible solo para estudiantes activos.")
        return super().dispatch(request, *args, **kwargs)


def usos_etiquetables(estudiante):
    return DispensacionLote.objects.filter(
        dispensacion__es_simulada=True,
        dispensacion__respuesta__estudiante=estudiante,
        dispensacion__respuesta__correcta=True,
        dispensacion__receta__curso__estudiantes=estudiante,
    ).select_related("lote__medicamento", "linea", "dispensacion__receta")


class MisEtiquetasView(EstudianteFarmaMixin, ListView):
    template_name = "pages/farmatef/mis_etiquetas.html"
    context_object_name = "etiquetas"
    paginate_by = 30

    def get_queryset(self):
        return usos_etiquetables(self.request.user).order_by("-pk")


class EtiquetaDispensacionView(EstudianteFarmaMixin, EtiquetaBaseView):
    def get_form(self, request, data=None):
        self.uso = get_object_or_404(usos_etiquetables(request.user), pk=self.kwargs["uso_id"])
        if data is None:
            patron = patron_code128(codigo_para_etiqueta(self.uso.lote.medicamento))
            data = {
                "ancho_mm": max(EtiquetaLoteForm.base_fields["ancho_mm"].initial, ancho_code128(patron) + 5),
                "alto_mm": 55,
                "copias": 1,
            }
        return EtiquetaLoteForm(data, lote_dispensado=self.uso.lote)

    def get(self, request, *args, **kwargs):
        return self.render_preview(request, self.get_form(request))


class ComprobanteDispensacionView(EstudianteFarmaMixin, View):
    def get(self, request, dispensacion_id):
        dispensacion = get_object_or_404(
            Dispensacion.objects.select_related("receta").prefetch_related(
                "lotes_usados__linea__medicamento", "lotes_usados__lote",
            ),
            pk=dispensacion_id,
            es_simulada=True,
            respuesta__estudiante=request.user,
            respuesta__correcta=True,
            receta__curso__estudiantes=request.user,
        )
        response = FileResponse(
            comprobante_dispensacion(dispensacion), as_attachment=True,
            filename=f"comprobante-farmatef-{dispensacion.pk}.pdf",
            content_type="application/pdf",
        )
        response["Cache-Control"] = "private, no-store"
        return response


class PracticaRecetasView(EstudianteFarmaMixin, View):
    template_name = "pages/farmatef/practica_recetas.html"

    def get_queryset(self):
        return (
            Receta.objects.filter(curso__estudiantes=self.request.user)
            .select_related("curso")
            .prefetch_related(Prefetch("lineas", queryset=RecetaLinea.objects.select_related("medicamento").order_by("pk")))
            .defer("sospecha_falsificacion", "motivo_rechazo_esperado")
            .order_by("-creado_en")
        )

    def render_page(self, request, *, receta_id=None, form=None):
        receta = None
        respuesta_existente = None
        casos = []
        numero = request.GET.get("numero", "").strip()
        if receta_id is None:
            recetas = self.get_queryset()
            if numero:
                recetas = recetas.filter(numero__iexact=numero)
            page_recetas = recetas[:50]
            page_recetas = list(page_recetas.prefetch_related(
                Prefetch(
                    "respuestas_estudiantiles",
                    queryset=RespuestaReceta.objects.filter(estudiante=request.user).order_by("-intento"),
                    to_attr="respuesta_actual",
                )
            ))
            casos = [
                {"receta": item, "respuesta": item.respuesta_actual[0] if item.respuesta_actual else None}
                for item in page_recetas
            ]
        else:
            receta = self.get_queryset().filter(pk=receta_id).first()
            if not receta:
                raise Http404("No tienes acceso a esta receta de práctica.")
            respuesta_existente = RespuestaReceta.objects.filter(
                receta=receta, estudiante=request.user
            ).prefetch_related(
                "dispensacion__lotes_usados__lote", "dispensacion__lotes_usados__linea__medicamento",
            ).order_by("-intento").first()
            if form is None and (not respuesta_existente or respuesta_existente.reintento_disponible):
                form = RespuestaRecetaForm(
                    receta=receta, lotes=lotes_de_practica(receta),
                    initial={"intento": 2 if respuesta_existente else 1},
                )
        return render(request, self.template_name, {
            "casos": casos,
            "receta": receta,
            "respuesta": respuesta_existente,
            "form": form,
            "numero": numero,
            "today": timezone.localdate(),
        })

    def get(self, request, *args, **kwargs):
        return self.render_page(request, receta_id=kwargs.get("receta_id"))

    def post(self, request, receta_id, *args, **kwargs):
        receta = self.get_queryset().filter(pk=receta_id).first()
        if not receta:
            raise Http404("No tienes acceso a esta receta de práctica.")
        form = RespuestaRecetaForm(request.POST, receta=receta, lotes=lotes_de_practica(receta))
        if not form.is_valid():
            return self.render_page(request, receta_id=receta_id, form=form)
        try:
            responder_receta(
                receta_id,
                request.user,
                form.cleaned_data["decision"],
                form.cleaned_data["motivo_rechazo"],
                intento=form.cleaned_data["intento"] or 1,
                explicacion_otro_motivo=form.cleaned_data["explicacion_otro_motivo"],
                lotes_elegidos={
                    linea_id: form.cleaned_data[campo].pk
                    for linea_id, campo in form.campos_lotes.items()
                    if form.cleaned_data[campo]
                },
            )
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        return redirect("farmatef:practica_receta", receta_id=receta_id)
