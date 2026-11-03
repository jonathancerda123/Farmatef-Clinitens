from django.contrib import admin
from core.admin import SoloSuperusuarioAdmin

from .models import (
    CasoClinico,
    CasoMultimedia,
    CodigoActividad,
    Paciente,
    PacienteMultimedia,
    ResultadoDiagnostico,
)


class CasoMultimediaInline(admin.TabularInline):
    model = CasoMultimedia
    extra = 0


@admin.register(CasoClinico)
class CasoClinicoAdmin(SoloSuperusuarioAdmin, admin.ModelAdmin):
    list_display = ("titulo", "creado_por", "actualizado_en")
    search_fields = ("titulo",)
    inlines = [CasoMultimediaInline]


@admin.register(CodigoActividad)
class CodigoActividadAdmin(SoloSuperusuarioAdmin, admin.ModelAdmin):
    list_display = ("codigo", "caso_clinico", "activo", "creado_en")
    list_filter = ("activo",)
    search_fields = ("codigo", "caso_clinico__titulo")


class PacienteMultimediaInline(admin.TabularInline):
    model = PacienteMultimedia
    extra = 0


@admin.register(Paciente)
class PacienteAdmin(SoloSuperusuarioAdmin, admin.ModelAdmin):
    list_display = ("rut", "nombre_completo", "sexo", "centro_atencion")
    search_fields = ("rut", "nombre_completo")
    inlines = [PacienteMultimediaInline]


@admin.register(ResultadoDiagnostico)
class ResultadoDiagnosticoAdmin(SoloSuperusuarioAdmin, admin.ModelAdmin):
    list_display = ("nombre_examen", "paciente", "categoria", "fecha", "publicacion")
    list_filter = ("categoria", "publicacion")
