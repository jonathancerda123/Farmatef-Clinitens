# Validación — 013 / Etiquetado de lotes para FarmaTEF

Fecha: 2026-11-04. Fase: implementación local autorizada. Sin commit. Entorno: `core.test_settings`; no se leyó la base recibida, `.env`, medios ni credenciales.

| RF | Prueba | Esperado | Obtenido | Estado / límite |
|---|---|---|---|---|
| RF-013-01–05 | `manage.py check --settings=core.test_settings` | Sin problemas de configuración y rutas importables | `System check identified no issues (0 silenced)` | Check básico correcto; no prueba permisos funcionales |
| RF-013-01/04 | `manage.py shell ... get_template(...)` y `resolve('/farmatef/etiquetado/')` | Plantilla cargable y URL resuelta | Plantilla `pages/farmatef/etiquetado.html`; `url_name=etiquetado` | Correcto; no demuestra interacción en navegador |
| RF-013-03/04 | `makemigrations --check --dry-run --settings=core.test_settings` | No se requieren cambios de esquema | `No changes detected` | Correcto; función no persistente |
| RF-013-05 | Revisión estática del template | `@page` y etiqueta en mm; aviso escala 100% | Medidas interpoladas desde enteros acotados; una página por copia | Revisión estática; calibración con impresión real pendiente |
| RF-013-06/07/08 | Inspección estática de la plantilla actualizada | Dos columnas adaptables, cuatro presets, medidas editables, acción imprimir/guardar PDF | Implementado en `etiquetado.html`; cambios de configuración invalidan la vista previa para exigir actualización | Estructura verificada por lectura; no se hizo revisión de navegador |
| RF-013-03/09 | Revisión de la captura aportada y el selector | Distinguir nombre del producto y número de partida; evitar etiquetas excesivamente estrechas | El selector ahora presenta solo número de lote, vencimiento y stock; ancho mínimo 40 mm/alto 30 mm y texto con ajuste de línea | Implementado; revisión visual posterior pendiente |
| RF-013-03/09 | Inspección técnica posterior | Configuración válida, texto del selector y carga de página | `check` sin problemas; cotejo de migraciones limpio; etiqueta de lote muestra código, vencimiento y stock; plantilla cargada y ruta resuelta | Check técnico; no equivale a revisar la página en navegador |
| RF-013-10 | Inspección de controles | Opciones del lote acotadas visualmente al medicamento activo y relación comprobada en servidor | JS oculta las opciones incompatibles y reinicia una selección cruzada; `clean()` conserva la validación por FK | Implementado; falta revisión de navegador/solicitud funcional |
| RF-013-10 | `manage.py check`, `makemigrations --check --dry-run` y comprobación del widget con objeto simulado | Importaciones/configuración correctas, sin migración, atributos de opción disponibles | Check sin problemas; `No changes detected`; opción produjo `data-medicamento-id`, `data-vence` y `data-stock`; template y ruta cargaron | Comprobación técnica, no prueba funcional de filtrado en navegador |
| RF-013-10 | Inspección del vínculo campo/widget tras reporte de lista vacía | Ambos selectores reciben sus opciones y atributos dependientes | Aserciones del widget enlazado al campo correctas para medicamento y lote; metadatos `data-*` producidos; check/migraciones/plantilla/ruta pasan | No se consultaron los registros de inventario; sin prueba de interacción en navegador |
| RF-013-01–08 | Repetición de comprobaciones tras el ajuste visual | Django sin errores, sin migraciones y plantilla/ruta cargables | `check` correcto; `No changes detected`; template cargada y `url_name=etiquetado` resuelto | Correcto en entorno de configuración independiente |

## Regresión y permisos

Se inspeccionó que la vista use `PermitsPositionMixin`, que el queryset utilice `objetos_del_docente` y que el lote esté ligado al medicamento seleccionado. No se ejecutaron tests automatizados, conforme a la instrucción vigente. No se enviaron solicitudes funcionales ni se comprobó acceso ajeno con cuentas de prueba.

## Interfaz e impresión

La distribución de dos columnas, los presets y la etiqueta física en vista previa se implementaron en plantilla. Se intentó iniciar la revisión visual, pero la herramienta de navegador no pudo determinar con suficiente confianza la URL activa y detuvo la automatización; no se interactuó con páginas. Pendiente inspección visual y calibración física. Los navegadores/controladores pueden limitar dimensiones y respetar áreas no imprimibles; no se afirma precisión física hasta medir una copia. No se probó con impresora.

## Datos y aplicación

El POST solo vuelve a renderizar la selección validada; no persiste datos ni modifica stock. No se hizo lectura manual de la base recibida. No requiere migración.

## Límites y aceptación

Pendientes navegador, impresora real, precisión medida, matriz funcional de roles y revisión de la usuaria. No se agregaron pruebas ni se ejecutó la suite automatizada.
