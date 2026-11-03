from django.apps import AppConfig


class PreventConcurrentLoginsConfig(AppConfig):
    """Conserva la PK AutoField de la migración original del proveedor."""

    name = "preventconcurrentlogins"
    default_auto_field = "django.db.models.AutoField"
