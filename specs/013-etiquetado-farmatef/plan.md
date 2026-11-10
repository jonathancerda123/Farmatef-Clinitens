# Plan técnico — 013 / Etiquetado de lotes para FarmaTEF

Spec: [spec.md](spec.md). Autorizado por la solicitud explícita de la usuaria el 2026-11-04.

## Base inspeccionada

FarmaTEF ya incluye `Medicamento`, `LoteInventario`, `PermitsPositionMixin`, `objetos_del_docente` y portada `templates/pages/farmatef/farmatef.html`. Se conservarán los cambios locales existentes. Shell general en `base_extendido.html`; UI según `docs/PERSONALIZACION_VISUAL.md`.

## Integración

| RF | Archivo | Cambio | Verificación |
|---|---|---|---|
| RF-013-01/02/03/09/10 | `FarmaTEFApp/forms.py` | Formulario acotado por actor, relación medicamento-lote, etiqueta legible y opciones de lotes vinculadas al medicamento | Carga de rutas/plantillas y `check` |
| RF-013-01/02/04 | `FarmaTEFApp/views.py`, `urls.py` | Vista protegida, validación y render no persistente | `check`, revisión estática de scope |
| RF-013-04/05/06/07/08 | `templates/pages/farmatef/etiquetado.html` | Distribución dos columnas, presets, previsualización y CSS de impresión mm | Inspección de plantilla/CSS; impresión real pendiente |
| RF-013-01 | `templates/pages/farmatef/farmatef.html` | Acceso desde lista de módulos | Compilación/render estructural |
| RF-013-01–05 | docs y trazabilidad | Evidencia, límites y estado | Coherencia documental |

## Datos, contratos y permisos

POST CSRF con `ModelChoiceField` limitado a objetos del actor. JavaScript filtra los lotes visibles al seleccionar el medicamento; el servidor mantiene la validación de la relación lote/medicamento. Sin escritura persistente ni cambio del inventario. Acceso exclusivamente por `PermitsPositionMixin`.

## Interfaz y estilos

Usar el layout general, una distribución adaptable en dos columnas, datos/formulario a la izquierda y vista previa/configuración de tamaño en la columna auxiliar. Incluir cuatro presets editables, dimensiones en mm (ancho 40–150, alto 30–150), una copia por página, texto educativo y controles de pantalla ocultos al imprimir. El selector de lote comunica número, vencimiento y stock. El diálogo del navegador permite imprimir o guardar como PDF. Avisar sobre escala 100%, ajuste desactivado y encabezados/pies. La impresión debe calibrarse localmente.

## Migraciones, compatibilidad y reversión

No se cambia esquema, base de datos, migraciones ni dependencias. Reversión limitada a los archivos de 013, preservando otros cambios preexistentes.

## Pruebas y riesgos

Se harán comprobaciones técnicas básicas no destructivas. No se agregan ni ejecutan pruebas funcionales automatizadas en este pedido. Navegador, impresora física, precisión medida, motores alternativos y aceptación quedan pendientes.

## Documentos y decisiones

Actualizar índice, trazabilidad, estado y validation.md con evidencia real. No leer `.env`, base, medios ni credenciales.
