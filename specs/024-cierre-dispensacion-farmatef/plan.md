# Plan técnico 024

Reutilizar ReportLab y los permisos de la práctica. Generar el PDF a partir de Dispensacion y DispensacionLote. Ampliar RecetaLinea con textos opcionales de dosis e indicaciones. Extender el índice de búsqueda del selector a los códigos de barras del inventario permitido.

Registrar intentos numerados con restricción por receta, estudiante y número. Validar el número enviado para rechazar el reenvío de un formulario anterior. Conservar la transacción del descuento y el registro de dispensación. La migración deja cerrados los resultados previos y conserva sus relaciones. Ensayar en bases ficticias. Antes de aplicar a otra copia de trabajo, respaldar SQLite. En caso de recuperación, parar el servidor y restaurar la copia compatible.
