# Plan técnico — 032

La plantilla [docente_modulo.html](../../templates/pages/clinitens/simulacion/docente_modulo.html) añade un límite de 76 rem mediante dos clases de layout en [simulacion-docente.css](../../static/css/simulacion-docente.css). Eliminar esas clases de la vista docente para que la estructura compartida determine el ancho, como sucede en Estudiantes. Quitar el selector del editor si queda sin uso.

Conservar los tokens de color, la tipografía, la separación interna de las tarjetas y el ajuste móvil existente. El selector utilizado por la impresión de etiquetas de laboratorio mantiene su ancho. La reversión afecta únicamente dos líneas de presentación.

Comparar los bordes de las cuatro vistas con la tabla de Estudiantes en Chrome con datos ficticios. Comprobar el acceso directo autorizado y denegado con la configuración de pruebas.
