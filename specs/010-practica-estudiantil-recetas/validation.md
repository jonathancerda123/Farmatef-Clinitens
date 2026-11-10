# Validación — 010

Fecha: 2026-11-04. Implementación local autorizada. Estado inicial: no ejecutada.

| Requisito | Verificación | Resultado |
|---|---|---|
| 010-01–010-10 | Check de configuración y cotejo de migraciones | Sin problemas de configuración; no se detectaron cambios de modelo pendientes |

## Datos y migración

Respaldo previo a aplicar 0007: `.test-artifacts/recetas-010/db.sqlite3.before-student-flow-20261104`, 798720 bytes, SHA-256 `404E3FCB322DF64596A9849E91789A6E320295B01DE1C28BA474D019919B57C8`. La copia y la base de origen coincidieron al respaldar. No se abrió `.env` ni medios.

El 2026-11-04 se agregaron cinco casos ficticios al curso 3 (`DTENS-26-4C`) usando solo los campos de curso autorizados, los medicamentos consultados del catálogo y la cuenta responsable asociada al curso. Cada caso contiene dos líneas con una unidad ficticia; no se descontó inventario al crearlos. Antes de insertarlos se consultó stock vigente únicamente para los dos medicamentos del caso válido. Respaldo previo: `.test-artifacts/recetas-010/db.sqlite3.before-examples-20261104` (823296 bytes). Verificación posterior limitada a los cinco números creados: cinco recetas, dos líneas cada una, todas asignadas al curso 3.

| Verificación | Resultado |
|---|---|
| `.venv/Scripts/python.exe manage.py check --settings=core.test_settings` | Sin problemas |
| `.venv/Scripts/python.exe manage.py makemigrations --check --dry-run --settings=core.test_settings` | No se detectaron cambios |
| Carga Django de las plantillas de práctica, gestión y navegación | Las tres plantillas cargaron sin error |
| `.venv/Scripts/python.exe manage.py migrate --plan` | Solo planificó FarmaTEFApp.0007 |
| `.venv/Scripts/python.exe manage.py migrate FarmaTEFApp --noinput` | Aplicó 0007 correctamente |
| `git diff --check` | Informó líneas con espacios finales en archivos editados y avisos LF/CRLF de Windows; revisión de diferencias realizada |
| Pruebas funcionales / suite | No ejecutadas |
| Plantillas en navegador | No revisadas; Computer Use se detuvo porque no pudo determinar con suficiente confianza la URL del navegador para aplicar su política |

## Límites y aceptación

No declarar aceptación funcional o visual sin revisar el flujo como docente y alumno. La ausencia de suite/prueba de navegador se documentará explícitamente. No commit/push/despliegue.
