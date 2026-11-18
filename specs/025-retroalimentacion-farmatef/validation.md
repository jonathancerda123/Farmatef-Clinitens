# Validación 025

2026-11-15. Rama `jonathan`, con cambios locales previos de las specs 023 y 024. Python 3.12.0 y Django 5.2.18 desde `.test-artifacts/clinica-019-env`, con `core.test_settings`. Se usaron SQLite en memoria y una fixture para Chrome por Playwright con solicitudes a Django mediante un puente local. Sin acceso a la base habitual.

| Requisito | Prueba | Resultado |
|---|---|---|
| RF-025-01 | `test_alertas_coinciden_con_resultados_y_permisos` y recorrido Chrome del enlace de stock bajo | Tarjetas y destinos coherentes por docente y administración. |
| RF-025-02 | `test_filtrar_y_registrar_son_recorridos_separados` y filtro combinado en Chrome | Alta válida, duplicado con error, lote ajeno rechazado y compatibilidad del POST previo. Búsqueda «solucion» encuentra «Solución». Comprobado en Chrome que la columna Lotes presenta el código, la cantidad y el vencimiento en tres líneas separadas por lote. |
| RF-025-03 | `test_codigo_largo_requiere_ancho_suficiente`, Code 128 extraído del PNG y de PDFs de Chrome, código introducido en el selector | Código y checksum recuperados del bitmap y de tres páginas rasterizadas. Dos copias docentes generan dos páginas de 55 × 44 mm. La copia estudiantil genera una página de 55 × 55 mm. Introducir el código muestra el lote y Enter no envía el formulario. Lector e impresora físicos pendientes. |
| RF-025-04 | `test_dispensacion_correcta_imprime_solo_el_lote_usado` y recorrido Chrome desde «Mis etiquetas» | Vista propia inmediata, segundo alumno matriculado sin enlace y detalle 404. |
| RF-025-05 | Chrome a 1440, 1280, 768 y 390 px con fixture de FarmaTEF | Avisos apilados y diferenciados por color. Columna derecha en escritorio y avisos sobre los módulos en pantallas angostas. Acciones alineadas por fila, cuatro destinos conservados y ambos filtros accesibles con Enter. |
| RF-025-06 | `test_busqueda_docente_parcial_y_detalle_conservan_el_ambito` y Chrome a 1440, 1280, 768 y 390 px | Registro más ancho y buscador compacto en escritorio. El fragmento devuelve coincidencias autorizadas sin distinguir mayúsculas. Se mantiene la lista al abrir un detalle, que se puede cerrar y abrir con teclado. Las recetas ajenas quedan fuera de la búsqueda y su URL directa no muestra el detalle. |
| RF-025-07 | Chrome con fixture docente y estudiantil, y POST parcial de `test_codigo_largo_requiere_ancho_suficiente` | Selección y cambios de lote, medidas y copias actualizan sin recargar. Se retira la vista anterior y un ancho inválido muestra el error de servidor sin botón de impresión. La solicitud parcial rechaza un lote ajeno y la vista estudiantil conserva la dosis del caso. El POST manual funciona con JavaScript desactivado. Dos copias produjeron dos páginas de 55 × 55 mm, inspeccionadas en el PDF. |
| RNF-025-01 | Pruebas directas de registro e inventario sin sesión/con estudiante y alertas con MANAGER, ADMIN y superusuario | Anónimo redirigido. Estudiante recibe 403 en gestión. Docente aislado por propietario. Administración global. |
| RNF-025-02 | `test_alertas_coinciden_con_resultados_y_permisos` con lotes agotados, vencidos y fechas límite | Los vencidos no incrementan el stock disponible. Hoy y el último día de aviso se incluyen. Stock igual al mínimo no alerta. Producto inactivo queda fuera de las dos alertas. |
| RNF-025-03 | `DispensacionConcurrenteTests` y comandos pgbench de [QA](../../qa/postgres/README.md) | YAML de Compose leído y puerto local comprobado. Docker y PostgreSQL no estaban disponibles en este equipo. Test concurrente omitido en SQLite. Sin datos de latencia, TPS ni capacidad HTTP. |
| RNF-025-04 | Compilación de celdas y ejecución local con tres imágenes ficticias y API de modelos simulada | Resuelve rutas `../train/images`, `../valid/images` y `../test/images` y escribe dos filas en el CSV. Pendientes exportación anotada y entrenamiento real. |

## Verificación general

- RF-025-08, 2026-11-16. `manage.py test FarmaTEFApp --settings=core.test_settings` ejecutado con el intérprete aislado. 19 pruebas aprobadas y una omitida por requerir PostgreSQL. El registro incluye únicamente los códigos de los medicamentos autorizados para el docente. `node.exe --check static/js/medicamento-select.js` correcto. Chrome con una fixture aislada simuló la entrada por teclado con Enter y comprobó que no se envía el formulario, que una coincidencia permite seleccionar el medicamento y enfocar el número de lote, que el selector admite el código y que un código nuevo conserva los ceros iniciales. Falta la prueba con un lector físico.

- En Etiquetado, Chrome confirmó que «Imprimir / Guardar como PDF» aparece debajo de Cantidad de copias y antes del aviso. Un formato inválido oculta el botón y dos copias válidas generan dos páginas.

- `manage.py check --settings=core.test_settings` correcto. `manage.py makemigrations --check --dry-run --settings=core.test_settings` sin cambios.
- `manage.py test --settings=core.test_settings` con 85 pruebas descubiertas, 84 aprobadas y una omitida porque requiere PostgreSQL.
- `node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs` con cuatro pruebas correctas. `node.exe theme/static_src/build.cjs` compiló con Tailwind 4.3.3.
- Chrome a 1440, 768 y 390 px en portada, inventario, registro y etiqueta de estudiante. Un H1 por página, sin desbordamiento horizontal del documento y tabla desplazable. PDF docente y estudiantil inspeccionados visualmente.
- La spec no añade migraciones. Las migraciones anteriores del árbol de trabajo se ejecutaron solo en bases de prueba. Aceptación del usuario pendiente.
