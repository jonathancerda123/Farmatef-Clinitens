from django.urls import path
from .views import (
    DAUHistorialView, DAUInicioView, DAURegistroView, DocenteCasosView,
    DocenteModuloView,
    DocenteResultadosView, EstudianteCasosView, EtapaView, PublicarCasoView,
    EtiquetasLaboratorioView, EtiquetasOrdenLaboratorioView, HistorialLaboratorioView,
    LaboratorioSolicitudView, OrdenLaboratorioPDFView, descargar_dau_pdf,
    EnfermeriaInicioView, EnfermeriaRegistroView, EnfermeriaHistorialView,
    PrepararCasoView,
)

app_name = "clinitens_simulacion"

urlpatterns = [
    path("docente/casos/<int:pk>/preparar/", PrepararCasoView.as_view(), name="preparar_caso"),
    path("docente/enfermeria/", DocenteModuloView.as_view(modulo="enfermeria"), name="docente_enfermeria"),
    path("enfermeria/", EnfermeriaInicioView.as_view(), name="enfermeria_inicio"),
    path("enfermeria/historial/", EnfermeriaHistorialView.as_view(), name="enfermeria_historial"),
    path("enfermeria/<int:pk>/", EnfermeriaRegistroView.as_view(), name="enfermeria_registro"),
    path("docente/casos/", DocenteCasosView.as_view(), name="docente_casos"),
    path("docente/dau/", DocenteModuloView.as_view(modulo="dau"), name="docente_dau"),
    path("docente/laboratorio/", DocenteModuloView.as_view(modulo="laboratorio"), name="docente_laboratorio"),
    path("docente/centro-diagnostico/", DocenteModuloView.as_view(modulo="diagnostico"), name="docente_diagnostico"),
    path("docente/kardex/", DocenteModuloView.as_view(modulo="diagnostico"), name="docente_kardex"),
    path("docente/resultados/", DocenteResultadosView.as_view(), name="docente_resultados"),
    path("docente/casos/<int:pk>/publicar/", PublicarCasoView.as_view(), name="publicar_caso"),
    path("dau/", DAUInicioView.as_view(), name="dau_inicio"),
    path("dau/historial/", DAUHistorialView.as_view(), name="dau_historial"),
    path("dau/<int:pk>/pdf/", descargar_dau_pdf, name="dau_pdf"),
    path("dau/<int:pk>/", DAURegistroView.as_view(), name="dau_registro"),
    path("practica/<int:pk>/laboratorio/etiquetas/", EtiquetasLaboratorioView.as_view(), name="etiquetas_laboratorio"),
    path("practica/laboratorio/historial/", HistorialLaboratorioView.as_view(), name="historial_laboratorio"),
    path("practica/laboratorio/orden/<int:pk>/pdf/", OrdenLaboratorioPDFView.as_view(), name="orden_laboratorio_pdf"),
    path("practica/laboratorio/orden/<int:pk>/etiquetas/", EtiquetasOrdenLaboratorioView.as_view(), name="etiquetas_orden_laboratorio"),
    path("practica/<int:pk>/laboratorio/", LaboratorioSolicitudView.as_view(), name="solicitud_laboratorio"),
    path("practica/", EstudianteCasosView.as_view(), name="estudiante_casos"),
    path("practica/<str:etapa>/", EstudianteCasosView.as_view(), name="modulo"),
    path("practica/<int:pk>/<str:etapa>/", EtapaView.as_view(), name="etapa"),
]
