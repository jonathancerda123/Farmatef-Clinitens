# Plan técnico — 012 / docentes colaboradores FarmaTEF

Spec: [spec.md](spec.md). Implementación local autorizada; migración aplicada localmente después de respaldo.

## Base inspeccionada

Se revisaron `Curso`, `CursoDetalleView`, formularios/rutas de cursos, `core.permissions`, modelos/vistas/formularios/servicios de FarmaTEF y los templates de detalle e historial. Se preservan las modificaciones locales anteriores.

## Integración propuesta

| RF | Archivos | Cambio | Verificación prevista |
|---|---|---|---|
| 012-01/02 | `CliniTensDocenteApp/models.py`, `forms.py`, `views.py`, `urls.py`, `curso_detalle.html` | M2M de docentes y controles owner/admin para agregar/quitar MANAGER activo | Check, migración generada, plantillas/rutas cargadas; sin prueba funcional |
| 012-03/04 | `core/permissions.py`, `FarmaTEFApp/views.py`, `services.py` | Helpers de cursos/recetas visibles para owner, colaborador actual y admin; revocación inmediata | Revisión estática de consultas/servicio y check |
| 012-05/06 | `FarmaTEFApp/forms.py` y vistas | Permitir asignar recetas a cursos compartidos; conservar filtros de catálogo y rutas no FarmaTEF | Check y carga de plantilla; pruebas funcionales pendientes |
| 012-07/08 | Spec, migración, trazabilidad, estado y validación | Reglas de no elevación/compartición parcial y recuperación | Revisión documental |

## Datos, migración y recuperación

Agregar una relación M2M vacía `Curso.docentes_colaboradores`; no realizar backfill, cambio de propietarios ni matrícula. La migración se aplicó solo a la base local de desarrollo después de un respaldo consistente. Antes de aplicarla en otro entorno, respaldar esa base, comprobar el plan y acordar restauración/reversión.

## Riesgos y límites

La colaboración expone a los participantes únicamente los intentos y recetas FarmaTEF de ese curso. Debe comprobarse rol, estado y pertenencia en cada POST. No se ejecutan pruebas funcionales ni revisión visual de navegador en esta entrega.
