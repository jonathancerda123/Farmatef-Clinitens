"""Clasificación de rutas por área; los cursos sirven a ambas especialidades."""
from UsuarioApp.models import AreaDocente


RUTAS_CURSOS_COMPARTIDOS = {
    "cursos", "curso_detalle", "curso_plantilla_excel", "curso_importar_excel",
    "curso_credenciales_excel", "curso_agregar_estudiante",
    "curso_quitar_estudiante", "curso_eliminar",
}


def area_de_ruta(resolver_match):
    namespace = resolver_match.namespace
    nombre = resolver_match.url_name
    if namespace == "farmatef" or (not namespace and nombre == "farmatef"):
        return AreaDocente.FARMACIA
    if namespace == "clinitensdocente":
        if nombre in RUTAS_CURSOS_COMPARTIDOS:
            return None
        if nombre in {"curso_agregar_colaborador", "curso_quitar_colaborador"}:
            return AreaDocente.FARMACIA
        return AreaDocente.ENFERMERIA
    if namespace in {"clinitensficha", "clinitens_simulacion"} or (not namespace and nombre == "clinitens"):
        return AreaDocente.ENFERMERIA
    return None
