# Validación — 014 Simuladores clínicos

Fecha: 2026-11-04. Código local: trabajo posterior a `345dd32`; sin commit. Fase: implementación local. Entorno: `core.test_settings` aislado y base local respaldada. Estado: checks técnicos y migración de esquema correctos; interacción, permisos en ejecución, aceptación docente y visual aún pendientes.

| RF | Prueba / comando | Esperado | Obtenido | Estado / límite |
|---|---|---|---|---|
| 014-01/02 | `python manage.py check --settings=core.test_settings` | Sin errores de configuración | `System check identified no issues (0 silenced)` | Correcto; no prueba vistas ni roles |
| 014-02 | `python manage.py makemigrations --check --dry-run --settings=core.test_settings` | Sin cambios faltantes | `No changes detected` | Correcto; migración nueva generada, no aplicada |
| 014-01/03/04/05 | Carga de las cinco plantillas con Django template loader | Compilación de plantilla | Carga sin excepción | Correcto; no revisión en navegador |
| 014-01/02 | `reverse()` de docente, resultados, alumno, módulo laboratorio y Kardex | URLs resolubles | Cinco rutas resueltas | Correcto; no GET/POST probado |
| 014-03/06 | URL directa con alumno/no inscrito/otro curso/inactivo | Aislamiento por sesión/curso | No ejecutado | Aún se requiere fixture ficticia y verificación de respuestas HTTP |
| 014-05 | Repetición y corrección concurrente de evento | Historial íntegro | No ejecutado | La BD local no fue abierta ni modificada |
| 014-07 | Navegador/escritorio/móvil/teclado | Diseño e interacción accesibles | No ejecutado | `node_modules` no está instalado en `theme/static_src`; build omitido |

## Error de tabla ausente — 2026-11-04

La usuaria reportó `OperationalError: no such table: CliniTensSimulacionApp_casosimulacion` en la página de preparación docente. Se respaldó la base local (835584 bytes) en `.test-artifacts/backups/db.sqlite3.pre-simulaciones-20261104.bak`, sin inspeccionar sus registros. `manage.py migrate --plan` mostró únicamente las dos migraciones de esta app. Se aplicaron ambas con `manage.py migrate CliniTensSimulacionApp --noinput`; las dos quedaron `[X]` en `showmigrations`, y `manage.py check` pasó.

## Persistencia y límites

Se crearon migraciones aditivas `0001_initial.py` y `0002_eventokardex_sim_kardex_una_correccion_por_evento.py`. Se aplicaron primero a SQLite en memoria con `core.test_settings` y posteriormente a la base local respaldada para resolver el error. No se crearon casos/estudiantes de demostración ni se consultaron registros de `db.sqlite3` o `media/`. El formulario de resultados de laboratorio acepta líneas de texto para solicitud/resultado/unidad y no interpreta normalidad. El Kardex es un historial de eventos educativos, no un registro asistencial.

No se ejecutaron pruebas funcionales (la usuaria no solicitó pruebas), no se comprobó el acceso directo en cliente HTTP, no se hizo build de Tailwind y no se revisó visualmente. La usuaria debe validar contenido pedagógico ficticio con su docente antes de usarlo como práctica. Los módulos no están preparados para trabajo clínico ni producción.

## Aceptación y próximo paso

Aceptación de interfaz/recorrido de la usuaria y revisión académica pendientes. Antes de ejecutar la migración en una base persistente: respaldo, plan de aplicación y recuperación según `docs/ENTORNO_Y_VERIFICACION.md`.
