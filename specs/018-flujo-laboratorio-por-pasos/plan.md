# Plan técnico — 018 / Flujo de laboratorio por pasos

Spec: [spec.md](spec.md). Implementación local autorizada por solicitud explícita el 2026-11-05.

## Integración

| RF | Archivos | Cambio | Verificación |
|---|---|---|---|
| 01/02 | `views.py`, `urls.py`, templates, CSS/JS | Wizard estudiante con selección y validación servidor | `check`, rutas y templates aislados |
| 03/05 | `models.py`, migración, `views.py` | Registro de orden, código único, propiedad y listado historial | Migración solo en memoria, modelo/cotejo |
| 04 | `views.py`, templates | PDF/impresión de orden y etiquetas por tubo | Carga/reverse/estructura técnica; revisión visual pendiente |
| 06 | docs y validación | Registrar recuperación y límites | No tocar base habitual |

No sustituir ni borrar los campos JSON históricos de tubos. La selección se valida contra `CasoSimulacion.ordenes_laboratorio`, luego se guarda como snapshot. Las rutas de recursos siempre filtran por usuario dueño y caso matriculado.

## Migración y recuperación

Añadir modelo `SolicitudLaboratorioSimulada`, sin alterar modelos/datos existentes. Ensayar migraciones en memoria con `core.test_settings`. Antes de aplicación futura en base local, crear copia consistente verificada, revisar `migrate --plan`, aplicar y comprobar registros. Si hay fallo, detener escrituras y recuperar conjuntamente código y respaldo.

## Verificación y límites

Ejecutar `manage.py check`, `makemigrations --check --dry-run`, migración en memoria y carga/reverse de vistas/plantillas. No ejecutar suite de tests conforme a instrucción del proyecto. No declarar verificada interacción, permisos HTTP ni impresión física. No usar la DB habitual ni leer datos existentes.
