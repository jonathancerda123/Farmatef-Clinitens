from django.urls import path

from . import views

app_name = "clinitensdocente"

urlpatterns = [
    path("resultados/<int:pk>/habilitar/", views.ResultadoHabilitarView.as_view(), name="resultado_habilitar"),
    path("", views.DashboardDocenteView.as_view(), name="dashboard"),
    path("casos/", views.CasoClinicoListCreateView.as_view(), name="casos"),
    path(
        "casos/<int:pk>/editar/",
        views.CasoClinicoUpdateView.as_view(),
        name="caso_editar",
    ),
    path(
        "casos/<int:pk>/eliminar/",
        views.CasoClinicoDeleteView.as_view(),
        name="caso_eliminar",
    ),
    path(
        "casos/<int:pk>/previsualizar/",
        views.CasoClinicoPreviewView.as_view(),
        name="caso_previsualizar",
    ),
    path("codigos/", views.CodigoListCreateView.as_view(), name="codigos"),
    path(
        "codigos/<int:pk>/cambiar-estado/",
        views.CodigoActividadToggleView.as_view(),
        name="codigo_cambiar_estado",
    ),
    path("pacientes/", views.PacienteListCreateView.as_view(), name="pacientes"),
    path(
        "pacientes/<int:pk>/editar/",
        views.PacienteUpdateView.as_view(),
        name="paciente_editar",
    ),
    path(
        "pacientes/<int:pk>/eliminar/",
        views.PacienteDeleteView.as_view(),
        name="paciente_eliminar",
    ),
    path(
        "pacientes/<int:pk>/detalle/",
        views.PacienteDetalleView.as_view(),
        name="paciente_detalle",
    ),
    path(
        "apoyo-diagnostico/",
        views.ResultadoListCreateView.as_view(),
        name="apoyo_diagnostico",
    ),
    path(
        "resultados/<int:pk>/eliminar/",
        views.ResultadoDeleteView.as_view(),
        name="resultado_eliminar",
    ),
    path(
        "estudiantes/",
        views.EstudiantesListView.as_view(),
        name="estudiantes",
    ),
    path(
        "estudiantes/ficha/<int:pk>/revisar/<slug:seccion>/",
        views.FichaEstudianteRevisionView.as_view(),
        name="ficha_revisar",
    ),
    path(
        "estudiantes/ficha/<int:pk>/pdf/",
        views.exportar_ficha_pdf,
        name="ficha_pdf",
    ),
    path(
        "estudiantes/ficha/<int:pk>/rubrica/",
        views.FichaRubricaView.as_view(),
        name="ficha_rubrica",
    ),
    path(
        "cursos/",
        views.CursoListCreateView.as_view(),
        name="cursos",
    ),
    path(
        "cursos/plantilla-excel/",
        views.CursoPlantillaExcelView.as_view(),
        name="curso_plantilla_excel",
    ),
    path(
        "cursos/<int:pk>/",
        views.CursoDetalleView.as_view(),
        name="curso_detalle",
    ),
    path(
        "cursos/<int:pk>/importar/",
        views.CursoImportarExcelView.as_view(),
        name="curso_importar_excel",
    ),
    path(
        "cursos/<int:pk>/credenciales/",
        views.CursoCredencialesExcelView.as_view(),
        name="curso_credenciales_excel",
    ),
    path(
        "cursos/<int:pk>/estudiantes/<int:usuario_pk>/agregar/",
        views.CursoAgregarEstudianteView.as_view(),
        name="curso_agregar_estudiante",
    ),
    path(
        "cursos/<int:pk>/estudiantes/<int:usuario_pk>/quitar/",
        views.CursoQuitarEstudianteView.as_view(),
        name="curso_quitar_estudiante",
    ),
    path(
        "cursos/<int:pk>/eliminar/",
        views.CursoDeleteView.as_view(),
        name="curso_eliminar",
    ),
    path(
        "en-vivo/",
        views.EnVivoView.as_view(),
        name="en_vivo",
    ),
]
