# Plan técnico — 010

Spec: [spec.md](spec.md). Autorización local recibida el 2026-11-04: «me gusta, hazlo».

## Integración propuesta

| RF | Archivo | Cambio | Verificación |
|---|---|---|---|
| 010-01/03/06 | `FarmaTEFApp/models.py`, `forms.py`, `views.py` | Curso, pista visible y clave/feedback docente; formularios limitados por propiedad | check, migración, revisión de contexto/templates |
| 010-02/04/05/09 | `models.py`, `views.py`, `urls.py`, plantillas | Modelo de respuesta única por estudiante y vistas GET/POST inscritas | check y revisión de filtros directos |
| 010-07/08 | `services.py` | Calificar respuesta; compartir servicio atómico FEFO para una entrega completa correcta | revisión estática y check |
| 010-01/02 | `templates/components/Layout/app_shell.html` | Enlace de práctica para estudiante; gestión sigue docente | revisión de plantilla |
| 010-10 | Migración 0007 | Campos nuevos aditivos y respuesta; backfill de sospechas previas; conservar recetas sin curso | respaldo local, migración y `makemigrations --check` |

## Datos y recuperación

Antes de aplicar la migración local se respaldará `db.sqlite3` dentro de `.test-artifacts/recetas-010/` y se verificará el hash. La migración mantiene las recetas existentes, no las asigna a cursos y traduce cualquier sospecha persistida a la clave correspondiente. No se toca `.env`, medios ni credenciales.

## Validación

Ejecutar `manage.py check` y cotejo de migraciones con `core.test_settings`; registrar límites. No se afirma cobertura funcional ni revisión visual no ejecutada. No ejecutar la suite sin solicitud expresa. No hacer commit, push o despliegue.
