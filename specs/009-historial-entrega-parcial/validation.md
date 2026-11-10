# Validación — 009

Implementación local completada. `manage.py check --settings=core.test_settings` y `makemigrations --check --dry-run --settings=core.test_settings` terminaron sin errores. Las migraciones 0004/0005 se aplicaron tras respaldar `.test-artifacts/recetas-009/`.

La conciliación preservó la entrega existente de `DEMO-APS-001`: 5 prescritas, 5 entregadas, estado ENTREGADA; las otras cuatro demostrativas siguen pendientes. Integridad SQLite: `ok`; una transacción histórica presente. No se ejecutaron pruebas funcionales ni revisión de navegador.

## Corrección de error al abrir el historial

La primera carga de `/farmatef/recetas/` produjo `AttributeError`: `Receta` ya usa la relación plural `dispensaciones`, pero el `prefetch_related` de la vista conservaba el nombre singular anterior. Se actualizó la precarga para las dispensaciones y sus lotes/líneas. Verificación ejecutada con `.venv/Scripts/python.exe` y `core.test_settings`:

| Comando | Resultado |
|---|---|
| `manage.py check --settings=core.test_settings` | Sin problemas |
| `manage.py makemigrations --check --dry-run --settings=core.test_settings` | No se detectaron cambios |

No se abrió el navegador ni se ejecutaron pruebas funcionales; la ruta debe recargarse en la sesión de la usuaria para confirmar la pantalla.

## Selección de líneas y sospecha de falsificación

Se añadieron casillas explícitas por medicamento. Cada selección se envía junto al identificador de `RecetaLinea`; el servicio valida que las líneas correspondan exactamente a la receta, descuenta del inventario asociado al medicamento y registra la auditoría en esa línea. Una línea desmarcada recibe cantidad cero; una marcada permite reducir la cantidad para una entrega parcial.

Se mantiene `es_ficticia` para identificar que los datos del entorno son de simulación y se añadió `sospecha_falsificacion` para representar que el documento que presenta el cliente se sospecha falso. La sospecha queda visible y el servicio bloquea la dispensación también en POST directo.

Migración aditiva `0006_receta_sospecha_falsificacion` aplicada a la base local el 2026-11-03. Respaldo previo: `.test-artifacts/recetas-010/db.sqlite3.before-20261103`; SHA-256 del original y copia coincide (`E73305E45FC2515913DDCA3B3A742747D0FDC576213D8A27AF62AB716710D358`).

| Comando | Resultado |
|---|---|
| `.venv/Scripts/python.exe manage.py migrate FarmaTEFApp --noinput` | `0006` aplicada |
| `.venv/Scripts/python.exe manage.py check --settings=core.test_settings` | Sin problemas |
| `.venv/Scripts/python.exe manage.py makemigrations --check --dry-run --settings=core.test_settings` | No se detectaron cambios |

No se ejecutaron pruebas funcionales ni revisión visual en navegador. La marca no representa una decisión legal ni reemplaza revisión humana; se usa solo en este flujo simulado.

## Recetas con varios medicamentos

El modelo y servicio ya guardaban varias líneas por receta. Para que el límite no dependiera de las tres filas iniciales, se añadió el botón «Añadir medicamento», que agrega filas hasta el máximo de 10 que valida Django. Las recetas existentes no se cambiaron; las demostrativas previas siguen con las líneas con que fueron creadas. `node --check static/js/recetas-formset.js` y `manage.py check --settings=core.test_settings` pasan. No se ejecutó una prueba funcional de navegador.

## Cinco demostraciones multimed

Con autorización de la usuaria, se consultaron solo el usuario `valita` y el catálogo activo con existencias. Tras crear un respaldo idéntico por SHA-256 en `.test-artifacts/recetas-011/db.sqlite3.before`, se añadieron cinco recetas `DEMO-MULTI-*` bajo esa cuenta, cada una con dos medicamentos distintos y una unidad de práctica por línea (10 líneas en total). Los alias indican «Caso técnico NO CLÍNICO»; no son combinaciones terapéuticas ni recomendaciones. Vencen el 2027-02-01. Ninguna dispensa ni stock fue modificada.
