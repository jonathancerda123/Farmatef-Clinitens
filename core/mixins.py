from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
from .permissions import es_docente, es_administrador, objetos_del_docente


class PermitsPositionMixin(LoginRequiredMixin):
    """
    Permite acceso al módulo solo a usuarios activos
    con cargo ADMIN o MANAGER.
    """

    login_url = "account_login"
    redirect_url = reverse_lazy("Home")

    permisos_docente = ("ADMIN", "MANAGER")

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return self.handle_no_permission()

        if not es_docente(user):
            raise PermissionDenied("No tienes permiso para acceder a esta sección.")

        return super().dispatch(request, *args, **kwargs)


class AdministradorMixin(LoginRequiredMixin):
    login_url = "account_login"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if not es_administrador(request.user):
            raise PermissionDenied("La gestión de cuentas requiere administración.")
        return super().dispatch(request, *args, **kwargs)


class PropietarioMixin:
    def get_queryset(self):
        return objetos_del_docente(super().get_queryset(), self.request.user)


class FormularioDocenteMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["actor"] = self.request.user
        return kwargs
