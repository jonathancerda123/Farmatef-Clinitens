from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import Http404
from django.db import transaction
from django.db.models import Exists, OuterRef, Prefetch
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import TemplateView
from urllib.parse import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin

from core.mixins import PermitsPositionMixin
from core.permissions import cargo, objetos_del_docente, recetas_visibles_para_docente
from .forms import (
    EntregaLineaFormSet,
    EtiquetaLoteForm,
    LoteInventarioForm,
    MedicamentoForm,
    RecetaForm,
    RecetaLineaFormSet,
    RespuestaRecetaForm,
)
from .models import Dispensacion, LoteInventario, Medicamento, Receta, RecetaLinea, RespuestaReceta
from .services import eliminar_receta, entregar_receta, responder_receta


class EtiquetadoView(PermitsPositionMixin, View):
    template_name = "pages/farmatef/etiquetado.html"

    def render_page(self, request, form=None, etiqueta=None):
        return render(
            request,
            self.template_name,
            {
                "form": form or EtiquetaLoteForm(actor=request.user),
                "etiqueta": etiqueta,
                "copias": range(1, etiqueta["copias"] + 1) if etiqueta else (),
            },
        )

    def get(self, request, *args, **kwargs):
        return self.render_page(request)

    def post(self, request, *args, **kwargs):
        form = EtiquetaLoteForm(request.POST, actor=request.user)
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
            },
        )


class InventarioView(PermitsPositionMixin, TemplateView):
    template_name = "pages/farmatef/inventario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        medicamentos = objetos_del_docente(
            Medicamento.objects.all(), self.request.user, campo="creado_por"
        ).prefetch_related(
            Prefetch("lotes", queryset=LoteInventario.objects.select_related("medicamento"))
        )
        context.update(
            {
                "medicamentos": medicamentos,
                "form_medicamento": MedicamentoForm(
                    prefix="medicamento", actor=self.request.user
                ),
                "form_lote": LoteInventarioForm(
                    prefix="lote", actor=self.request.user
                ),
            }
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
        return redirect("farmatef:inventario")


class RecetasView(PermitsPositionMixin, View):
    template_name = "pages/farmatef/recetas.html"

    def get_queryset(self):
        return recetas_visibles_para_docente(
            Receta.objects.prefetch_related(
                "lineas__medicamento",
                "dispensaciones__lotes_usados__lote",
                "dispensaciones__lotes_usados__linea__medicamento",
                "respuestas_estudiantiles__estudiante",
            ),
            self.request.user,
        )

    def render_page(self, request, *, receta_form=None, lineas_formset=None, receta=None):
        if receta is None:
            numero = request.GET.get("numero", "").strip().upper()
            if numero:
                receta = self.get_queryset().filter(numero=numero).first()
                if not receta:
                    messages.error(request, "No se encontró una receta con ese número en tu ámbito de acceso.")
        context = {
            "receta_form": receta_form or RecetaForm(actor=request.user),
            "lineas_formset": lineas_formset or RecetaLineaFormSet(form_kwargs={"actor": request.user}),
            "intentos": receta.respuestas_estudiantiles.select_related("estudiante").order_by("-respondida_en") if receta else [],
            "receta": receta,
            "today": timezone.localdate(),
            "historial": self.get_queryset().prefetch_related(
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
                )
                for form in lineas_formset.forms
                if form.cleaned_data.get("medicamento")
            ])
        messages.success(request, "Receta registrada para la simulación.")
        return redirect(f"{reverse('farmatef:recetas')}?{urlencode({'numero': receta.numero})}")


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


class PracticaRecetasView(EstudianteFarmaMixin, View):
    template_name = "pages/farmatef/practica_recetas.html"

    def get_queryset(self):
        return (
            Receta.objects.filter(curso__estudiantes=self.request.user)
            .select_related("curso")
            .prefetch_related("lineas__medicamento")
            .defer("sospecha_falsificacion", "motivo_rechazo_esperado")
            .order_by("-creado_en")
        )

    def render_page(self, request, *, receta_id=None, form=None):
        receta = None
        respuesta_existente = None
        casos = []
        if receta_id is None:
            page_recetas = self.get_queryset()[:50]
            page_recetas = list(page_recetas.prefetch_related(
                Prefetch(
                    "respuestas_estudiantiles",
                    queryset=RespuestaReceta.objects.filter(estudiante=request.user),
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
            ).first()
        return render(request, self.template_name, {
            "casos": casos,
            "receta": receta,
            "respuesta": respuesta_existente,
            "form": form or (RespuestaRecetaForm() if receta and not respuesta_existente else None),
            "today": timezone.localdate(),
        })

    def get(self, request, *args, **kwargs):
        return self.render_page(request, receta_id=kwargs.get("receta_id"))

    def post(self, request, receta_id, *args, **kwargs):
        receta = self.get_queryset().filter(pk=receta_id).first()
        if not receta:
            raise Http404("No tienes acceso a esta receta de práctica.")
        form = RespuestaRecetaForm(request.POST)
        if not form.is_valid():
            return self.render_page(request, receta_id=receta_id, form=form)
        try:
            respuesta = responder_receta(
                receta_id,
                request.user,
                form.cleaned_data["decision"],
                form.cleaned_data["motivo_rechazo"],
            )
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        else:
            if respuesta.correcta:
                messages.success(request, "Respuesta registrada. Revisa la explicación del caso.")
            else:
                messages.info(request, "Respuesta registrada. Revisa la explicación del caso.")
        return redirect("farmatef:practica_receta", receta_id=receta_id)
