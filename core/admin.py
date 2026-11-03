class SoloSuperusuarioAdmin:
    """La consola técnica no permite eludir las reglas de las vistas funcionales."""
    def has_view_permission(self, request, obj=None):
        return request.user.is_active and request.user.is_superuser

    has_add_permission = has_view_permission
    has_change_permission = has_view_permission
    has_delete_permission = has_view_permission
