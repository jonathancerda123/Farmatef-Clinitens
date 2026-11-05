from django.urls import path

from . import views

app_name = "farmatef"

urlpatterns = [
    path("etiquetado/", views.EtiquetadoView.as_view(), name="etiquetado"),
    path("inventario/", views.InventarioView.as_view(), name="inventario"),
    path("recetas/", views.RecetasView.as_view(), name="recetas"),
    path("recetas/<int:receta_id>/entregar/", views.EntregarRecetaView.as_view(), name="entregar_receta"),
    path("recetas/<int:receta_id>/eliminar/", views.EliminarRecetaView.as_view(), name="eliminar_receta"),
    path("practica/recetas/", views.PracticaRecetasView.as_view(), name="practica_recetas"),
    path("practica/recetas/<int:receta_id>/", views.PracticaRecetasView.as_view(), name="practica_receta"),
    path("practica/recetas/<int:receta_id>/responder/", views.PracticaRecetasView.as_view(), name="responder_receta"),
]
