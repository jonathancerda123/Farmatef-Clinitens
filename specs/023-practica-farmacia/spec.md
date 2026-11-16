# 023 — Práctica de farmacia con inventario docente

Fecha: 2026-11-10. Alcance autorizado para el prototipo en jonathan.

- RF-023-01: El docente prepara su inventario, incluidos productos alternativos, y asigna recetas. La interfaz explica ese requisito. La práctica consulta el inventario simulado del autor de la receta, únicamente para inscritos.
- RF-023-02: El estudiante busca una receta por número y, por cada línea, busca el producto y elige un lote sin selección inicial. En esta versión el lote debe cubrir toda la línea. Receta incorrecta, lote incorrecto o falta de stock no emiten etiqueta ni descuentan stock. Se registra la respuesta para el docente.
- RF-023-03: La dispensación confirmada permite imprimir el lote consumido en el etiquetador existente. Solo su estudiante inscrito accede desde su resultado; medidas y copias se validan en servidor.
- RF-023-04: La pantalla de práctica ordena la lectura, búsqueda y decisión. El motivo se muestra al rechazar con JavaScript y queda disponible en el formulario nativo sin JavaScript. El resultado aparece antes del detalle de la receta y ofrece un botón de etiqueta por lote dispensado.
- RF-023-05: El selector de cada línea muestra al lado el producto prescrito, su presentación y las unidades solicitadas. Las opciones del inventario muestran su presentación, lote, vencimiento y unidades disponibles. La pista configurada permanece visible mientras se pueda responder, incluido el reintento.
- RF-023-06: Al elegir Rechazar receta y Otro motivo aparece una explicación obligatoria de hasta 300 caracteres. Se guarda junto al intento y el docente autorizado puede verla. Los motivos predefinidos conservan su flujo.
