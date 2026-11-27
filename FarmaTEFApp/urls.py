from django.urls import path

from . import views, views_sala, views_movimientos

app_name = "farmatef"

urlpatterns = [
    path("inventario/movimientos/", views_movimientos.MovimientosView.as_view(), name="movimientos"),
    path("inventario/<int:medicamento_id>/precio/", views_movimientos.PrecioView.as_view(), name="precio"),
    path("etiquetado/", views.EtiquetadoView.as_view(), name="etiquetado"),
    path("inventario/", views.InventarioView.as_view(), name="inventario"),
    path("inventario/registro/", views.RegistroInventarioView.as_view(), name="registro_inventario"),
    path("recetas/", views.RecetasView.as_view(), name="recetas"),
    path("recetas/<int:receta_id>/intentos/", views.IntentosRecetaView.as_view(), name="intentos_receta"),
    path("recetas/<int:receta_id>/entregar/", views.EntregarRecetaView.as_view(), name="entregar_receta"),
    path("recetas/<int:receta_id>/eliminar/", views.EliminarRecetaView.as_view(), name="eliminar_receta"),
    path("practica/recetas/", views.PracticaRecetasView.as_view(), name="practica_recetas"),
    path("sala/configurar/", views_sala.ConfigurarSalaView.as_view(), name="configurar_sala"),
    path("practica/sala/", views_sala.SalaEstudianteView.as_view(), name="sala"),
    path("practica/dispensaciones/<int:dispensacion_id>/ubicaciones/", views_sala.SalaEstudianteView.as_view(), name="localizar_dispensacion"),
    path("practica/vitrina/", views_sala.VitrinaAnteriorView.as_view(), name="vitrina"),
    path("practica/recetas/<int:receta_id>/", views.PracticaRecetasView.as_view(), name="practica_receta"),
    path("practica/recetas/<int:receta_id>/responder/", views.PracticaRecetasView.as_view(), name="responder_receta"),
    path("practica/etiquetas/", views.MisEtiquetasView.as_view(), name="mis_etiquetas"),
    path("practica/etiquetas/<int:uso_id>/", views.EtiquetaDispensacionView.as_view(), name="etiqueta_dispensacion"),
    path("practica/dispensaciones/<int:dispensacion_id>/comprobante/", views.ComprobanteDispensacionView.as_view(), name="comprobante_dispensacion"),
]
