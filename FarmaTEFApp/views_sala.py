from urllib.parse import urlencode

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View

from CliniTensDocenteApp.models import Curso
from core.mixins import PermitsPositionMixin
from core.permissions import es_administrador
from .models import Dispensacion, Medicamento, Receta
from .sala import asignar_ubicacion, autorizar_gestion, datos_sala, guardar_sala
from .views import EstudianteFarmaMixin


def seleccionar(queryset, valor):
    if valor is None:
        return queryset.first()
    try:
        identificador = int(valor)
        if not 0 < identificador < 2**63:
            raise ValueError
    except (ValueError, TypeError):
        raise Http404("Selección de sala no disponible.")
    return get_object_or_404(queryset, pk=identificador)


def pagina(request, contexto, *, estado=200):
    response = render(request, "pages/farmatef/sala.html", contexto, status=estado)
    response["Cache-Control"] = "private, no-store"
    return response


class ConfigurarSalaView(PermitsPositionMixin, View):
    def propietario(self, request):
        propietario = request.user
        if request.GET.get("docente") is not None:
            propietario = seleccionar(get_user_model().objects.filter(is_active=True), request.GET["docente"])
        autorizar_gestion(request.user, propietario)
        return propietario

    def contexto(self, request, propietario):
        propietarios = get_user_model().objects.filter(pk__in=Medicamento.objects.values("creado_por_id")).order_by("username") if es_administrador(request.user) else []
        datos = datos_sala(propietario, docente=True)
        return {"datos_sala": datos, "productos_sala": datos["productos"], "propietario": propietario,
                "propietarios": propietarios, "gestion_sala": True}

    def get(self, request):
        return pagina(request, self.contexto(request, self.propietario(request)))

    def post(self, request):
        propietario = self.propietario(request)
        try:
            if request.POST.get("accion") == "guardar_sala":
                guardar_sala(request.user, propietario, request.POST.get("configuracion"), request.POST.get("version"))
            elif request.POST.get("accion") == "asignar":
                try:
                    medicamento_id = int(request.POST.get("medicamento", ""))
                    mueble_id = int(request.POST["mueble"]) if request.POST.get("mueble") else None
                    if not 0 < medicamento_id < 2**63 or (mueble_id is not None and not 0 < mueble_id < 2**63):
                        raise ValueError
                except (ValueError, TypeError):
                    raise ValidationError("Selecciona un medicamento y un mueble válidos.")
                asignar_ubicacion(request.user, propietario, medicamento_id, mueble_id,
                                 request.POST.get("compartimento", ""), request.POST.get("version"))
            else:
                raise ValidationError("Operación de sala no reconocida.")
        except ValidationError as exc:
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return JsonResponse({"error": " ".join(exc.messages)}, status=400)
            for error in exc.messages:
                messages.error(request, error)
            contexto = self.contexto(request, propietario)
            contexto["error_sala"] = " ".join(exc.messages)
            return pagina(request, contexto, estado=400)
        messages.success(request, "Configuración de sala guardada." if request.POST["accion"] == "guardar_sala" else "Ubicación del medicamento guardada.")
        destino = f"{reverse('farmatef:configurar_sala')}?{urlencode({'docente': propietario.pk})}"
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return JsonResponse({"url": destino})
        return redirect(destino)


class SalaEstudianteView(EstudianteFarmaMixin, View):
    def get(self, request, dispensacion_id=None):
        contexto = {"gestion_sala": False}
        if dispensacion_id is not None:
            dispensacion = get_object_or_404(
                Dispensacion.objects.select_related("receta__curso", "receta__creado_por"),
                pk=dispensacion_id, es_simulada=True, respuesta__estudiante=request.user,
                respuesta__correcta=True, receta__curso__estudiantes=request.user,
            )
            receta = dispensacion.receta
            curso, propietario = receta.curso, receta.creado_por
            objetivos = list(dispensacion.lotes_usados.order_by("linea_id", "pk").values_list("lote__medicamento_id", flat=True).distinct())
            contexto.update(dispensacion=dispensacion, receta=receta, objetivos=objetivos,
                            volver=reverse("farmatef:practica_receta", args=[receta.pk]))
        else:
            cursos = Curso.objects.filter(estudiantes=request.user).order_by("nombre", "pk")
            curso = seleccionar(cursos, request.GET.get("curso"))
            docentes = get_user_model().objects.filter(pk__in=Receta.objects.filter(curso=curso).values("creado_por_id")).order_by("username", "pk") if curso else get_user_model().objects.none()
            propietario = seleccionar(docentes, request.GET.get("docente"))
            contexto.update(cursos=cursos, docentes=docentes, volver=reverse("farmatef:practica_recetas"))
            objetivos = []
        datos = datos_sala(propietario)
        datos["objetivos"] = list(dict.fromkeys(objetivos))
        contexto.update(curso=curso, propietario=propietario, datos_sala=datos, productos_sala=datos["productos"])
        return pagina(request, contexto)


class VitrinaAnteriorView(EstudianteFarmaMixin, View):
    def get(self, request):
        query = urlencode({k: request.GET[k] for k in ("curso", "docente") if k in request.GET})
        return redirect(reverse("farmatef:sala") + ("?" + query if query else ""))
