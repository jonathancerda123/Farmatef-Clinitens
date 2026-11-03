import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponse
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from core.permissions import es_administrador
from .validation import validar_datos, pendientes
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import FormView, TemplateView

from .ficha_config import SECCIONES, HENDERSON, MASLOW, GCS, DOWNTON, BRADEN
from .forms import IngresoFichaForm
from .models import FichaClinica
from UsuarioApp.models import Profile


def fusionar_diccionarios(base, nuevo):
    """Conserva las secciones previas al guardar solo la sección abierta."""
    resultado = dict(base or {})
    for clave, valor in nuevo.items():
        if isinstance(valor, dict) and isinstance(resultado.get(clave), dict):
            resultado[clave] = fusionar_diccionarios(resultado[clave], valor)
        else:
            resultado[clave] = valor
    return resultado


class EstudianteMixin(LoginRequiredMixin):
    """
    Protege las vistas de ficha clínica para estudiantes.

    RESTRICTED: estudiante normal.
    MANAGER y ADMIN: permitidos solo para pruebas o demostraciones.
    """

    login_url = "account_login"

    permisos_permitidos = ("RESTRICTED", "MANAGER", "ADMIN")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_active:
            raise Http404("Tu cuenta está desactivada.")

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        try:
            perfil = request.user.profile
        except Profile.DoesNotExist:
            raise Http404("Tu usuario no posee un perfil asociado.")

        permiso = perfil.position_FK.permission_code if perfil.position_FK else None

        if permiso not in self.permisos_permitidos:
            raise Http404("No tienes permiso para acceder a la ficha clínica.")

        return super().dispatch(request, *args, **kwargs)

    def ficha_actual(self):
        ficha = (
            FichaClinica.objects.select_related(
                "codigo_actividad__caso_clinico",
                "docente",
                "estudiante",
            )
            .prefetch_related("codigo_actividad__caso_clinico__archivos")
            .filter(
                pk=self.kwargs["pk"],
                estudiante=self.request.user,
            )
            .first()
        )

        if not ficha:
            raise Http404("No tienes acceso a esta ficha clínica.")

        curso = ficha.codigo_actividad.curso
        if curso and not es_administrador(self.request.user) and not curso.estudiantes.filter(pk=self.request.user.pk).exists():
            raise Http404("Ya no perteneces al curso de esta actividad.")
        return ficha


class IngresoFichaView(EstudianteMixin, FormView):
    template_name = "pages/clinitens/ficha/ingreso.html"
    form_class = IngresoFichaForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["actor"] = self.request.user
        return kwargs

    def form_valid(self, form):
        codigo = form.cleaned_data["codigo_actividad"]
        perfil_docente = form.cleaned_data["docente"]
        ficha, creada = FichaClinica.objects.get_or_create(
            codigo_actividad=codigo,
            estudiante=self.request.user,
            defaults={"docente": perfil_docente},
        )
        return redirect("clinitensficha:caso", pk=ficha.pk)


class CasoAsignadoView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/ficha/caso.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ficha"] = self.ficha_actual()
        from core.media import resultados_visibles
        context["resultados"] = resultados_visibles(context["ficha"].codigo_actividad.caso_clinico.resultados.all())
        return context


class FichaEditorView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/ficha/editor.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ficha = self.ficha_actual()
        clave = self.kwargs.get("seccion", "identidad")
        secciones_dict = {item[0]: item for item in SECCIONES}
        if clave not in secciones_dict:
            raise Http404("Sección no encontrada.")
        context.update(
            {
                "ficha": ficha,
                "secciones": SECCIONES,
                "seccion_actual": clave,
                "titulo_seccion": secciones_dict[clave][2],
                "datos_json": json.dumps(ficha.datos or {}),
                "henderson": HENDERSON,
                "maslow": MASLOW,
                "glasgow": GCS,
                "downton": DOWNTON,
                "braden": BRADEN,
                "aislamientos": [
                    "Precauciones estándar",
                    "Contacto",
                    "Gotas",
                    "Aéreo",
                ],
                "epp": [
                    "Mascarilla quirúrgica",
                    "Mascarilla N95",
                    "Pechera",
                    "Guantes",
                    "Antiparras / escudo facial",
                    "Cofia",
                    "Botas",
                ],
                "habitaciones": [
                    "Individual",
                    "Compartida",
                    "Aislamiento",
                    "UCI / UTI",
                ],
                "base_template": "pages/clinitens/ficha/base_estudiante.html",
                "ruta_editor": "clinitensficha:editor",
                "modo_revision": False,
            }
        )
        return context

    def post(self, request, *args, **kwargs):
        if self.kwargs["seccion"] not in {s[0] for s in SECCIONES}:
            raise Http404("Sección no encontrada.")
        ficha = self.ficha_actual()
        if ficha.bloqueada:
            messages.error(
                request, "Esta ficha ya fue enviada y no puede ser modificada."
            )
            return redirect("clinitensficha:resultado", pk=ficha.pk)
        try:
            raw = request.POST.get("datos_json", "{}")
            if len(raw.encode("utf-8")) > 250_000:
                raise ValidationError("La ficha supera el tamaño permitido.")
            datos = validar_datos(json.loads(raw))
            if set(datos) - {self.kwargs["seccion"]}:
                raise ValidationError("Guarda únicamente la sección abierta.")
            version = int(request.POST["version"])
        except (json.JSONDecodeError, ValueError, KeyError, RecursionError, ValidationError) as error:
            return HttpResponse("Datos de ficha no válidos: " + str(error), status=400, content_type="text/plain; charset=utf-8")

        ficha.datos = fusionar_diccionarios(ficha.datos, datos)
        if len(json.dumps(ficha.datos).encode("utf-8")) > 250_000:
            return HttpResponse("La ficha supera el tamaño permitido.", status=400)
        accion = request.POST.get("accion", "guardar")
        if accion not in {"guardar", "finalizar"}:
            return HttpResponse("Acción no válida.", status=400)
        if accion == "finalizar":
            faltantes = pendientes(ficha.datos)
            if faltantes:
                messages.error(request, "Completa o marca No aplica: " + "; ".join(faltantes))
            else:
                try:
                    validar_datos(ficha.datos)
                except ValidationError as error:
                    return HttpResponse(str(error), status=400)
                ficha.estado = FichaClinica.Estado.ENVIADA
                ficha.enviada_en = timezone.now()
        else:
            messages.success(request, "Avance de ficha guardado correctamente.")
        with transaction.atomic():
            updated = FichaClinica.objects.filter(pk=ficha.pk, estudiante=request.user,
                estado=FichaClinica.Estado.BORRADOR, version=version).update(
                    datos=ficha.datos, estado=ficha.estado, enviada_en=ficha.enviada_en,
                    version=F("version") + 1, actualizado_en=timezone.now())
        if not updated:
            context = self.get_context_data(**kwargs)
            current = context["ficha"]
            current.datos = fusionar_diccionarios(current.datos, datos)
            context["conflicto"] = True
            return self.render_to_response(context, status=409)
        if ficha.bloqueada:
            messages.success(request, "Ficha enviada correctamente. Quedó pendiente de calificación.")
            return redirect("clinitensficha:resultado", pk=ficha.pk)
        return redirect(
            "clinitensficha:editor", pk=ficha.pk, seccion=self.kwargs["seccion"]
        )


class ResultadoFichaView(EstudianteMixin, TemplateView):
    template_name = "pages/clinitens/ficha/resultado.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ficha"] = self.ficha_actual()
        return context
