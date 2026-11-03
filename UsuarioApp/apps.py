from django.apps import AppConfig


class UsuarioappConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "UsuarioApp"

    def ready(self):
        from . import signals  # noqa: F401
