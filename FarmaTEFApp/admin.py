from django.contrib import admin

from .models import Dispensacion, LoteInventario, Medicamento, Receta, RecetaLinea, RespuestaReceta


@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "principio_activo", "clasificacion", "stock_minimo", "activo", "creado_por")
    search_fields = ("nombre", "principio_activo", "codigo_barras", "clasificacion", "observaciones")
    list_filter = ("activo",)
    readonly_fields = ("creado_por", "creado_en", "actualizado_en")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(LoteInventario)
class LoteInventarioAdmin(admin.ModelAdmin):
    list_display = ("medicamento", "numero_lote", "vence_el", "unidades", "es_simulado", "registrado_por")
    search_fields = ("medicamento__nombre", "numero_lote")
    list_filter = ("vence_el",)
    readonly_fields = ("registrado_por", "creado_en")

    def save_model(self, request, obj, form, change):
        if not change:
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)


class RecetaLineaInline(admin.TabularInline):
    model = RecetaLinea
    extra = 0


@admin.register(Receta)
class RecetaAdmin(admin.ModelAdmin):
    list_display = ("numero", "curso", "persona_ficticia", "vence_el", "estado", "motivo_rechazo_esperado", "creado_por", "entregado_en")
    search_fields = ("numero", "persona_ficticia")
    list_filter = ("estado", "vence_el", "curso", "motivo_rechazo_esperado")
    readonly_fields = ("creado_por", "creado_en", "entregado_por", "entregado_en")
    inlines = (RecetaLineaInline,)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Dispensacion)
class DispensacionAdmin(admin.ModelAdmin):
    list_display = ("receta", "respuesta", "entregado_por", "entregado_en", "es_simulada")
    readonly_fields = ("receta", "respuesta", "entregado_por", "entregado_en", "es_simulada")


@admin.register(RespuestaReceta)
class RespuestaRecetaAdmin(admin.ModelAdmin):
    list_display = ("receta", "estudiante", "decision", "motivo_rechazo", "correcta", "respondida_en")
    list_filter = ("correcta", "decision", "motivo_rechazo")
    readonly_fields = ("receta", "estudiante", "decision", "motivo_rechazo", "correcta", "explicacion", "respondida_en")
