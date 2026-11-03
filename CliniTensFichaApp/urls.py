from django.urls import path

from . import views

app_name = "clinitensficha"

urlpatterns = [
    path("", views.IngresoFichaView.as_view(), name="ingreso"),
    path("ficha/<int:pk>/caso/", views.CasoAsignadoView.as_view(), name="caso"),
    path(
        "ficha/<int:pk>/seccion/<slug:seccion>/",
        views.FichaEditorView.as_view(),
        name="editor",
    ),
    path(
        "ficha/<int:pk>/resultado/",
        views.ResultadoFichaView.as_view(),
        name="resultado",
    ),
]
