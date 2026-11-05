# Validación — 017 / Flujos DAU, laboratorio y CAD

Fecha: 2026-11-05. Fase: implementación local. Código/commit: sin commit. Entorno: `.venv/Scripts/python.exe`, Django 5.2.18, `core.test_settings`.

| RF | Prueba / pasos | Esperado | Obtenido | Estado / límite |
|---|---|---|---|---|
| RF-017-01 | `manage.py check`; carga de plantilla del módulo | Flujo DAU presente | `System check identified no issues`; template cargó | Técnico básico; sin POST ni navegación |
| RF-017-02 | Migración en memoria, `check`, carga de plantillas/reverse | Órdenes/tubos/etiquetas listos | Migración 0005 aplicada; `check` correcto; plantilla de etiquetas y rutas cargadas | No se ejecutó POST ni se midió escala física |
| RF-017-03 | Migración en memoria, `check`, carga de plantillas/reverse | Cuatro tipos y revisión individual disponibles | Migración 0005 aplicada; `check` correcto; plantillas docente/estudiante cargaron | No se ejecutó POST funcional |
| RF-017-04 | Carga de portada, reverses y búsqueda estática de rutas | Nombre CAD en accesos vigentes | Portada y ruta `docente_diagnostico` cargaron; alias Kardex conserva la ruta anterior | Sin revisión visual en navegador |
| RF-017-05 | `manage.py makemigrations --check --dry-run`; migrar en memoria | Modelo/migración alineados sin tocar DB habitual | `No changes detected`; migración 0005 OK en memoria | No aplicar a `db.sqlite3` sin respaldo |

## Ejecución

Comandos ejecutados:

- `python manage.py check --settings=core.test_settings` — correcto.
- `python manage.py makemigrations --check --dry-run --settings=core.test_settings` — `No changes detected`.
- `python manage.py migrate --noinput --settings=core.test_settings` — migraciones, incluida `CliniTensSimulacionApp.0005`, aplicadas en memoria.
- Carga de siete plantillas relevantes y reverse de siete rutas — correcto.
- `git -c core.whitespace=cr-at-eol diff --check` — correcto, respetando finales CRLF existentes.

No se ejecutó la suite funcional ni se inspeccionó o migró la base habitual.

## Límites y aceptación

Revisión visual de navegador, impresión física, interacción/permisos HTTP, revisión académica y aceptación humana quedan pendientes. Computer Use se detuvo porque no pudo determinar con suficiente confianza la URL actual del navegador; por ello no se operó la ventana.
