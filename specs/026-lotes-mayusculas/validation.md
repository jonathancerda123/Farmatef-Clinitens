# Validación 026

Fecha 2026-11-16. Pruebas con `core.test_settings` y SQLite en memoria. El target de 004 estaba ausente. Se usó `.test-artifacts/clinica-019-env/Scripts/python.exe`, Python 3.12.0 y Django 5.2.18.

| Requisito | Prueba | Estado |
|---|---|---|
| RF-026-01 | POST en Registro de inventario como MANAGER, ADMIN y superusuario. POST en Django admin. | Antes se persistían minúsculas. Ahora el número persistido queda en mayúsculas. |
| RF-026-02 | POST por el inventario y Django admin con otra escritura del mismo número. Alta contra un lote histórico en minúsculas. | Se muestra el error en el campo. Se conservan los lotes y el saldo. Antes se aceptaba el alta contra el lote histórico. |
| Regresión | POST directo como estudiante y edición de unidades del lote histórico en Django admin. | Estudiante recibe 403. La edición autorizada de unidades conserva el número histórico. |

- `manage.py test --settings=core.test_settings` ejecutó 94 pruebas. Pasaron 93 y se omitió la prueba de bloqueo por fila que requiere PostgreSQL. Las cinco regresiones de `NumeroLoteTests` pasaron.
- `manage.py check --settings=core.test_settings` pasó. `manage.py makemigrations --check --dry-run --settings=core.test_settings` confirmó que el esquema no cambia.
- Verificación por cliente de Django. La demo y los datos persistentes quedan pendientes de revisión por el usuario. Cualquier corrección de los duplicados históricos requiere identificar el saldo, el vencimiento y las dispensaciones de cada registro en una copia respaldada.
