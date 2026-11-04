# 013 — Etiquetado de lotes para FarmaTEF

Fecha: 2026-11-04. Estado: implementación local; revisión humana pendiente. Fuente: solicitud explícita de agregar «Etiquetado — Diseña e imprime etiquetas con tamaño real en milímetros». Área: FarmaTEF. Código autorizado: sí, por la solicitud. No autoriza commit, push, despliegue ni operaciones sobre la base recibida.

## Problema, actores y resultado

FarmaTEF no tiene una herramienta visible para preparar etiquetas de los lotes simulados. Docentes y administración necesitan previsualizar una etiqueta y llevarla a impresión con dimensiones configurables expresadas en mm.

## Alcance y exclusiones

Se agrega una página bajo FarmaTEF para seleccionar medicamento/lote, configurar ancho entre 40 y 150 mm, alto entre 30 y 150 mm, y copias entre 1 y 100. Cada copia ocupa una página física configurada con ese tamaño. La etiqueta solo identifica medicamento, concentración, forma farmacéutica, lote y vencimiento, incluye stock de referencia y marca «FarmaTEF · Simulación educativa».

No se guardan diseños, impresiones ni movimientos, no se modifica stock, no se crean modelos/migraciones/dependencias y no se incluyen datos de pacientes, recetas, indicaciones posológicas ni códigos que aparenten ser documentos reales. La impresión depende del navegador, controlador, impresora, papel y área no imprimible; CSS fija el tamaño solicitado, pero el usuario debe imprimir al 100%/tamaño real y comprobar una medición física.

## Permisos por acción/dato

| Acción | Anónimo | RESTRICTED | MANAGER | ADMIN / superusuario activo | Propiedad |
|---|---|---|---|---|---|
| Abrir, generar vista e imprimir | Sin acceso | Sin acceso | Permitido | Permitido | MANAGER limitado a medicamentos/lotes propios; admin global |

## Flujo, datos y reglas

1. Abrir Etiquetado desde la portada FarmaTEF.
2. Elegir medicamento y uno de sus lotes visibles; el servidor vuelve a comprobar ambos y su relación.
3. Ingresar dimensiones y número de copias dentro de los límites indicados.
4. Revisar la vista previa y usar la impresión del navegador.

El formulario no persiste. No altera unidades ni crea historial. Los lotes vencidos se identifican con su fecha, sin consejo clínico. La vista de impresión usa página CSS `size: ancho mm alto mm`, margen cero y una etiqueta por página. La impresión física a escala real no puede certificarse sin calibración local.

## Requisitos y aceptación

- RF-013-01: Docentes y administración pueden abrir la pantalla; anónimos y otros cargos no.
- RF-013-02: El catálogo y los lotes se limitan en servidor al ámbito autorizado y un lote de otro medicamento es rechazado.
- RF-013-03: Se validan ancho 40–150 mm, alto 30–150 mm y copias 1–100; un envío inválido no genera etiquetas.
- RF-013-04: Una solicitud válida muestra el número de etiquetas configurado, datos del lote y marca educativa, sin guardar datos ni modificar stock.
- RF-013-05: La vista de impresión define las medidas en mm y advierte imprimir al 100%, sin ajustar a página ni encabezados/pies; escala y tolerancias físicas quedan pendientes de verificación con impresora.

## Compatibilidad y no funcionales

Se reutiliza el shell visual existente y la política central de permisos. Formularios con etiquetas accesibles, CSRF y validación del servidor. Las dimensiones se expresan en enteros y se acotan antes de interpolarlas en CSS.

## Decisiones y revisión

Se adopta una etiqueta por página para conservar una medida clara sin asumir formato de pliego. Las copias se imprimen como páginas sucesivas. Revisión de UI e impresión real pendiente.

## Ajuste visual solicitado — 2026-11-04

La usuaria pide acercar la interfaz a dos capturas de referencia. Se adopta su distribución de dos columnas: datos/configuración a la izquierda y vista previa junto a controles de tamaño a la derecha. Se agregan presets 55×44, 40×30, 60×40 y 100×50 mm, con medidas editables y resumen de escala. El contenido seguirá derivándose del medicamento y lote del inventario simulado. No se agregan campos para identidad de pacientes, dosis, vías de administración ni afirmaciones regulatorias que el catálogo no suministra.

- RF-013-06: La página organiza la edición y vista previa en dos columnas adaptables, con una etiqueta física visible y panel de dimensiones.
- RF-013-07: Los presets llenan ancho/alto y estos valores permanecen editables; vista previa/impresión indican las medidas activas.
- RF-013-08: La experiencia visual conserva los controles de impresión y permite usar «Imprimir / Guardar como PDF» mediante el diálogo del navegador; no se promete descarga directa de PNG/PDF.
- RF-013-09: El selector identifica cada lote por su número, vencimiento y stock, sin confundirlo con el nombre del medicamento. Las dimensiones mínimas evitan previsualizaciones demasiado estrechas para el contenido de demostración.
- RF-013-10: Al elegir un medicamento, el selector de lote presenta solo lotes de ese medicamento; un envío manipulado con una relación distinta se rechaza en servidor.
