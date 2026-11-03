"""Entrega privada de archivos vinculados a objetos autorizados."""
from pathlib import PurePosixPath

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import FileResponse, Http404
from django.http import HttpResponseForbidden
from django.core.files.storage import default_storage
from django.views.decorators.http import require_GET

from core.permissions import es_administrador, es_docente, objetos_del_docente
from CliniTensDocenteApp.models import CasoMultimedia, PacienteMultimedia, ResultadoDiagnostico
from CliniTensFichaApp.models import FichaClinica
from UsuarioApp.models import Profile


def resultados_visibles(queryset):
    return queryset.filter(Q(publicacion="INICIO") | Q(publicacion="HABILITACION", habilitado=True))


def upload_editor_desactivado(request):
    return HttpResponseForbidden("Adjunta archivos mediante el formulario del caso clínico.")


def fichas_propias(user):
    return FichaClinica.objects.filter(estudiante=user).filter(
        Q(codigo_actividad__curso__isnull=True) | Q(codigo_actividad__curso__estudiantes=user)
    )


@login_required
@require_GET
def archivo_privado(request, nombre):
    path = PurePosixPath(nombre)
    if path.is_absolute() or ".." in path.parts or "\\" in nombre:
        raise Http404
    user = request.user
    authorized = nombre == "profile.webp"
    caso = CasoMultimedia.objects.filter(archivo=nombre).select_related("caso").first()
    paciente = PacienteMultimedia.objects.filter(archivo=nombre).select_related("paciente").first()
    resultado = ResultadoDiagnostico.objects.filter(archivo=nombre).first()
    if caso:
        authorized = objetos_del_docente(CasoMultimedia.objects.filter(pk=caso.pk), user, "caso__creado_por").exists()
        authorized |= fichas_propias(user).filter(codigo_actividad__caso_clinico=caso.caso).exists()
    elif paciente:
        authorized = objetos_del_docente(PacienteMultimedia.objects.filter(pk=paciente.pk), user, "paciente__creado_por").exists()
    elif resultado:
        authorized = objetos_del_docente(ResultadoDiagnostico.objects.filter(pk=resultado.pk), user).exists()
        authorized |= resultados_visibles(ResultadoDiagnostico.objects.filter(pk=resultado.pk)).exists() and fichas_propias(user).filter(codigo_actividad__caso_clinico_id=resultado.caso_clinico_id).exists()
    elif nombre != "profile.webp":
        profile = Profile.objects.filter(image=nombre).first()
        if profile:
            authorized = es_administrador(user) or profile.user_FK_id == user.pk
            if es_docente(user):
                authorized |= profile.user_FK.cursos_clinitens.filter(creado_por=user).exists() or FichaClinica.objects.filter(docente=user, estudiante_id=profile.user_FK_id).exists()
            authorized |= fichas_propias(user).filter(docente_id=profile.user_FK_id).exists()
    types = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp",
             ".pdf": "application/pdf", ".mp4": "video/mp4", ".mov": "video/quicktime", ".webm": "video/webm"}
    content_type = types.get(path.suffix.lower())
    if not authorized or not content_type:
        raise Http404
    try:
        response = FileResponse(default_storage.open(nombre, "rb"), content_type=content_type,
                                as_attachment=path.suffix.lower() == ".pdf", filename=path.name)
    except (FileNotFoundError, OSError):
        raise Http404
    response["Cache-Control"] = "private, no-store"
    response["X-Content-Type-Options"] = "nosniff"
    return response
