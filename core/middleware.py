from django.core.exceptions import PermissionDenied
from django.utils.deprecation import MiddlewareMixin

from .areas import area_de_ruta
from .permissions import cargo, es_docente_de_area


class AreaDocenteMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        area = area_de_ruta(request.resolver_match)
        if area and cargo(request.user) == "MANAGER" and not es_docente_de_area(request.user, area):
            raise PermissionDenied("Tu área docente no permite acceder a este módulo.")
        return None
