from django.contrib import admin
from core.admin import SoloSuperusuarioAdmin

from .models import FichaClinica


@admin.register(FichaClinica)
class FichaClinicaAdmin(SoloSuperusuarioAdmin, admin.ModelAdmin):
    list_display = (
        "codigo_actividad",
        "estudiante",
        "docente",
        "estado",
        "actualizado_en",
    )
    list_filter = ("estado",)
    search_fields = (
        "codigo_actividad__codigo",
        "estudiante__username",
        "docente__username",
    )
    readonly_fields = tuple(field.name for field in FichaClinica._meta.fields)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
