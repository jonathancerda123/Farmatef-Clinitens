# Plan técnico 025

- Reutilizar `objetos_del_docente`, lotes y reglas del inventario en la portada y la consulta. Usar dos bloques de alertas con texto y enlaces completos, contraste semántico y los tokens y la tipografía existentes.
- Ajustar solo la portada docente con una cuadrícula adaptable. Los avisos se leen en una columna y la cuadrícula de herramientas conserva las tarjetas y sus acciones.
- Reutilizar el queryset autorizado de Recetas para buscar por fragmento del número. Mantener el enlace por número exacto desde el historial y los retornos tras registrar o entregar. Renderizar el detalle seleccionado en un desplegable bajo los resultados.
- Separar la vista de registro de la consulta. Mantener el POST histórico del inventario en la misma implementación de altas y conservar el alcance de los selectores.
- Compartir el código que se imprime con el selector de práctica. Usar ReportLab y Pillow ya instalados. La lista y el detalle estudiantiles comparten el mismo queryset de dispensaciones autorizadas.
- Reutilizar el POST de etiquetado y actualizar su vista previa en la página con la respuesta validada. Invalidar la vista anterior al cambiar la selección o el tamaño y conservar el botón para uso sin JavaScript.
- Reutilizar el campo de código y las opciones autorizadas del selector de medicamentos para la lectura en Registro. El navegador procesa la entrada del lector y el usuario confirma cada registro. Se conservan las validaciones de propiedad y duplicados en el servidor.
- Añadir configuración PostgreSQL aislada de `core.settings` y un Compose solo para el laboratorio local. Probar concurrencia y medir transacciones sintéticas por separado.
- Añadir un notebook independiente de la aplicación. Trabajar con una exportación local YOLO de Roboflow, métricas comparables y rutas de resultados ignoradas por Git.
- Verificar con datos ficticios, URLs, navegador y pruebas de etiquetas. El cambio de plataforma no requiere migraciones nuevas.
