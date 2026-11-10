# Validación — 012

Fecha: 2026-11-04. Código autorizado localmente. Migración aplicada a base local de desarrollo tras respaldo consistente; no producción.

| RF | Verificación | Resultado |
|---|---|---|
| RF-012-01/02 | Gestión owner/admin y validación MANAGER activo | Implementado; `manage.py check` sin problemas. No se ejercitó con usuarios |
| RF-012-03/05 | Consultas de historial, intentos y creación desde cursos compartidos | Implementado; check y carga de plantillas/rutas sin errores. Sin prueba funcional |
| RF-012-06/07 | Aislamiento de roster, clínica, catálogo ajeno, inactivos y URL directa | Límites visibles en consultas/formularios; no se ejecutaron pruebas de permisos |
| RF-012-08 | Migración y reversión | `CliniTensDocenteApp.0008_curso_docentes_colaboradores` aplicada. Respaldo previo: `.test-artifacts/recetas-012/db.sqlite3.before` (823296 bytes). La relación estaba vacía antes de su uso; no se aplicó a producción |
| — | Navegador | Pendiente; sin revisión visual |
| — | Commit/push | No realizado |

La migración se ejecutó con `.venv/Scripts/python.exe manage.py migrate CliniTensDocenteApp --noinput --settings=work.local_db_settings`; esta configuración temporal heredaba la configuración aislada sin cargar `.env`, apuntaba a la base local y se eliminó al terminar. La suite no se ejecutó. La aceptación funcional docente queda pendiente.
