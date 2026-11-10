# Validación — 018 / Flujo de laboratorio por pasos

Fecha: 2026-11-05. Estado: pendiente de ejecución. Entorno previsto: `.venv/Scripts/python.exe` con `core.test_settings`.

| Requisito | Evidencia planeada | Resultado | Límite |
|---|---|---|---|
| RF-018-01/02 | `check`, carga de plantillas, lectura de wizard y filtro de búsqueda | Correcto técnicamente | No reemplaza interacción del navegador |
| RF-018-03/05 | Cotejo de migraciones, migración en memoria, inspección de filtros y rutas | Correcto técnicamente | No se ejecuta matriz HTTP ni suite Django |
| RF-018-04 | Carga de plantilla de etiquetas, reverses y código PDF | Correcto técnicamente | Sin impresión física ni revisión visual |
| RF-018-06 | `check`, `makemigrations --check --dry-run`, `migrate` aislado | Correcto; migración 0006 aplicada en memoria | Base habitual intacta |

## Registro

Comandos ejecutados con `.venv/Scripts/python.exe`, Django 5.2.18 y `core.test_settings`:

- `manage.py check`: `System check identified no issues`.
- `manage.py makemigrations --check --dry-run`: `No changes detected`.
- `manage.py migrate --noinput`: migraciones aplicadas en base temporal en memoria, incluida `CliniTensSimulacionApp.0006`.
- Carga de las tres plantillas de laboratorio y reverse de cuatro rutas: correcto.

No se abrió ni migró la base habitual. No se ejecutaron tests, navegador, matriz HTTP ni impresión real. La implementación está localmente completa; aceptación visual/docente pendiente.

## Aplicación solicitada a la base local

2026-11-05: la usuaria pidió aplicar la migración. Se creó antes el respaldo SQLite consistente `.test-artifacts/lab-018/db.sqlite3.before-20261105` (942080 bytes; `PRAGMA quick_check` devolvió `ok`). `manage.py migrate --plan` mostró solo `CliniTensSimulacionApp.0006_solicitudlaboratoriosimulada`. Luego `manage.py migrate CliniTensSimulacionApp 0006 --noinput` terminó en `OK`; `showmigrations` muestra 0001–0006 aplicadas. No se consultaron filas ni contenidos de la base.
