from django.contrib import admin

from .models import LoteInventario, Medicamento


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
