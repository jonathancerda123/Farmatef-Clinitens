from django.urls import path

from . import views

app_name = "farmatef"

urlpatterns = [
    path("inventario/", views.InventarioView.as_view(), name="inventario"),
]
