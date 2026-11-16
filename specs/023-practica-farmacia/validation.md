# Validación 023

2026-11-10. Rama `jonathan`, Python 3.12, Django 5.2.18 y `core.test_settings`.

- 75 pruebas Django correctas. Las cinco nuevas cubren búsqueda y matrícula, lotes ajenos y alternativos, descuento del lote elegido, repetición, etiqueta propia, falta de stock y receta con dos líneas sin descuento parcial.
- Cuatro regresiones JavaScript correctas y build Tailwind 4.3.3 correcto. Cotejo de migraciones sin cambios pendientes de generar.
- Chrome a 390 px con datos ficticios. Búsqueda de receta, opciones de productos, selección por teclado, dispensación y vista previa correctas. PDF de 55 × 44 mm con tamaño verificado en el archivo; capturas inspeccionadas. Impresora física y carga concurrente pendientes.
- FarmaTEF 0008 agrega una opción al motivo de rechazo y no genera SQL de modificación de tablas en SQLite. Se aplicó en memoria y en la base ficticia de navegador. Para sincronizar el historial de migraciones de la copia de trabajo, ejecutar la migración con los settings de esa copia después de respaldarla. El respaldo previo permite restaurar el estado si falla la actualización.

El inventario de un docente se comparte entre sus prácticas. Esta versión requiere que un lote cubra toda la cantidad de cada línea. Se conservan respuestas y etiquetas de lotes dispensados previamente. La verificación usó exclusivamente datos ficticios.

RF-023-04: 75 pruebas Django correctas y nueve de FarmaTEF repetidas tras retirar el aviso de confirmación redundante. Chrome con datos ficticios comprobó búsqueda y selección por teclado, concentración separada de los datos del lote, visibilidad del motivo al alternar la decisión, etiqueta visible al inicio del resultado y vista previa en 55 × 44 mm. Verificación a 390 y 1280 px sin desbordamiento. También se comprobaron los campos nativos con JavaScript deshabilitado.
## Ajuste de información para elegir el lote

RF-023-05. En la rama `jonathan`, Chrome a 1440 y 390 px confirmó la indicación junto al selector y la presentación, el vencimiento y el stock del lote en sus opciones y al elegirlo. Las pruebas Django comprobaron la asociación con la línea, la visibilidad de la pista en el reintento y el aislamiento de inventarios. 84 pruebas aprobadas y una omitida por requerir PostgreSQL. Se usaron datos ficticios.

RF-023-06. Chrome a 390 px confirmó el recuadro condicional, el error al dejarlo vacío y la consulta del texto en el historial docente. Django comprobó espacios, longitud máxima, persistencia y descarte del texto con motivos predefinidos. 86 pruebas aprobadas y una omitida por requerir PostgreSQL. Cotejo de migraciones sin cambios pendientes.

Se ensayó `0010_explicacion_otro_motivo` en SQLite de pruebas y luego se aplicó a `.test-artifacts/farmacia-025-fixture.sqlite3` con `core.test_settings`. Respaldo anterior con `quick_check=ok` en `.test-artifacts/qa-farmacia-025/demo-antes-0010-20261116T023949941375Z.sqlite3`. La base habitual quedó fuera de la operación.
