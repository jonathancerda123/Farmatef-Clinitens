# 024 — Comprobante, escaneo y reintento de FarmaTEF

Fecha: 2026-11-11. Implementación solicitada para el prototipo en jonathan. Origen: alcance de Farmacia del Informe 1, RF-02 y RF-07 a RF-09, y BP-03 del Informe 2.

- RF-024-01: el alumno inscrito descarga un comprobante PDF de su dispensación válida. Incluye receta, fecha, producto, lote y unidades de la entrega. Sin acceso a comprobantes ajenos ni descuento al descargar.
- RF-024-02: la receta admite dosis e indicaciones ficticias por medicamento. La etiqueta de dispensación recupera esos datos de la línea registrada. Las recetas previas admiten campos vacíos.
- RF-024-03: el buscador estudiantil reconoce un código de barras de los productos disponibles en su práctica. Buscar no confirma el producto ni descuenta existencias.
- RF-024-04: el primer intento incorrecto habilita una corrección sin revelar la explicación. El segundo intento incorrecto muestra la explicación y permite abrir la respuesta esperada. Se conservan ambos intentos. Las respuestas anteriores permanecen cerradas.
- RF-024-05: el historial abre una página dedicada a los intentos de la receta. El servidor aplica los mismos permisos de consulta que en Recetas.
- RF-024-06: los enlaces de regreso de FarmaTEF usan el botón verde compartido y mantienen su destino.
