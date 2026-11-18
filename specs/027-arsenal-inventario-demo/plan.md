# Plan técnico — 027

- Cotejar todas las filas numeradas del PDF con el JSON existente de la spec 007. Identificar el destino mediante los medicamentos y números de lote de la captura.
- Ensayar con el ORM y `core.test_settings` sobre un respaldo SQLite consistente de la demo. Usar las formas y clasificaciones del PDF, el formato de nombre de la spec 007 cuando haga falta distinguir presentaciones y las reglas actuales de la vista. Validar la unicidad y las relaciones antes de confirmar una transacción.
- Confirmar la misma conciliación en la demo respaldada. Comparar filas del inventario, lotes y referencias de dispensación. Repetir la planificación para comprobar que la segunda ejecución queda sin cambios.
- Consultar la URL directa con docente y estudiante ficticios y revisar la tabla en Chrome.

## Recuperación

El respaldo se crea con la API de SQLite y se comprueba con `quick_check`. Si se requiere volver al estado previo, detener la demo antes de restaurar ese archivo. La carga usa las tablas y restricciones ya presentes; el destino no necesita migraciones.
