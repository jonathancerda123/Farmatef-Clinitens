# Plan — 029

1. Cotejar las tres fichas, sus actividades, la matrícula y los casos ya publicados en la demo.
2. Crear respaldo SQLite consistente y ensayar sobre una copia con `core.test_settings`. Validar el JSON con `validar_datos` y comprobar los recuentos con `pendientes`.
3. Aplicar en una transacción acotada a la demo. Actualizar contenido y versión de las fichas elegidas con control de versión. Comparar el estado, autoría y evaluaciones antes y después.
4. Verificar la revisión docente, la edición del alumno, el bloqueo de la ficha enviada, el avance en Seguimiento en vivo y la denegación a otro alumno. Verificar en Chrome los valores visibles.

Si se requiere recuperar la demo anterior, detener 8025 y restaurar en `.test-artifacts/farmacia-025-fixture.sqlite3` el respaldo anotado en la validación. Operación sobre datos ficticios y sin migraciones.
