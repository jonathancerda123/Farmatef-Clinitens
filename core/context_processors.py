from UsuarioApp.models import AreaDocente
from .permissions import cargo, es_docente, es_docente_de_area


def areas_docentes(request):
    estudiante = cargo(request.user) == "RESTRICTED"
    return {
        "acceso_farmacia": estudiante or es_docente_de_area(request.user, AreaDocente.FARMACIA),
        "acceso_enfermeria": estudiante or es_docente_de_area(request.user, AreaDocente.ENFERMERIA),
        "gestion_docente": es_docente(request.user),
    }
