# Plan — 037

[Spec](spec.md). Propuesta documental; implementación pendiente de autorización.

## Integración propuesta

Árbol inicialmente limpio. Reutilizar FarmaTEF, permisos centrales por área/propiedad y layout/tokens de la guía visual.

| RF | Archivos existentes / propuestos | Cambio y verificación prevista |
|---|---|---|
| 01/02 | models_sala.py, sala.py, views_sala.py, sala.html, sala-farmacia.js/CSS, tests_sala.py | Estado persistente y POST separado con CAS. Guardar geometría condicionado atómicamente por versión y desbloqueo. Desactivar controles/arrastre/teclado de geometría; preservar selección/asignación. Pruebas directas y dos pestañas. |
| 03 | models.py, forms.py, views.py, admin.py, registro_inventario.html, inventario.html | Precio exacto con validación/restricción, edición acotada autorizada y moneda visible. Sin reasignar autor. Pruebas de cero/null/límites. |
| 04 | inventario.py, InventarioView, inventario.html, data/arsenal_aps_2024_2026.json | Etiqueta Tipo de medicamento; usar valores importados de CLASIFICACIÓN del arsenal aportado, sin inferir grupos terapéuticos. Conservar valores combinados, opción sin clasificar, combinación de filtros y opciones autorizadas. |
| 05/06/07 | models.py, services.py, views.py, forms.py, admin.py, urls.py; movimientos.py y plantillas de historial/ajuste propuestos | Servicio único transaccional de modificación de unidades y movimiento. Integrar altas, ajustes y consumos existentes. Historial paginado por propietario. Admin deriva operaciones al servicio con motivo o impide edición directa. |

## Datos y concurrencia

Actor/saldos se obtienen en servidor; validar propiedad, sentido/motivo, cantidades y relaciones. Actualización condicional de stock y transacción conjunta con historial; orden consistente de lotes. Identificador estable de operación con unicidad por operación/lote; formulario de ajuste con token asociado al usuario para evitar reenvíos. Candado y geometría comparten versión; campo de bloqueo solo cambia mediante su operación dedicada. Revisar comandos de importación/carga que escriban stock y documentar integración o restricción, sin ejecutarlos sobre datos habituales.

## Migraciones, UI y verificación

Generar migraciones solo tras autorización. Ensayar instalación/actualización en base ficticia; bloqueo false, precio previo null y sin reconstrucción de movimientos. Respaldo compatible antes de cualquier operación habitual autorizada; no eliminar historia para revertir código.

Mantener page_title H1, etiquetas/foco y controles compartidos; filtros GET, escrituras POST/CSRF. Navegador docente/alumno a 1440/768/390, teclado, errores y estado al recargar. Build si cambian fuentes de estilos. Regresiones Django de permisos, idempotencia y rollback; JS pertinente al candado. Registrar runtime/comandos reales con core.test_settings independiente; usar target indicado por AGENTS y documentar cualquier imposibilidad. No extrapolar prueba lógica a carga real.
