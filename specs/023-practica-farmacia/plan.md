# Plan técnico 023

Ampliar la práctica existente, conservando el inventario por propietario y las entregas docentes. Los lotes ofrecidos y evaluados se restringen al autor de la receta. La corrección considera el stock vigente en la transacción y bloquea la emisión sin dispensación válida. Reutilizar la etiqueta existente con producto y lote fijados por el historial. El motivo estudiantil de falta de stock añade una opción de campo; revisar la migración en memoria.

Para RF-023-04, reutilizar los componentes de formulario y el selector existente. La receta tendrá tres pasos. El selector destacará nombre y concentración, con datos de lote debajo. El resultado quedará arriba con acceso directo a las etiquetas, reutilizando la validación actual.
# Explicación de «Otro motivo»

El formulario controla la visibilidad del recuadro. El servidor exige y conserva texto solamente con Rechazar receta y Otro motivo. Se añade un campo vacío por defecto en `RespuestaReceta`, independiente de la retroalimentación docente. El historial de intentos usa sus permisos actuales.

La migración es aditiva. Se ensaya en bases ficticias. Para la demo local, respaldar primero su SQLite y usar `core.test_settings` con la ruta de la fixture. Para recuperar esa demo, detener su servidor y restaurar el respaldo junto al código compatible. La calificación sigue evaluando el motivo seleccionado.
