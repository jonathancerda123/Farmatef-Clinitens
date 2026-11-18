# Plan técnico 026

- Compartir entre Inventario y Django admin la normalización y la detección de duplicados al validar el formulario. Comparar con la misma conversión en los lotes históricos del medicamento.
- Mantener la restricción de unicidad existente para el valor canónico. La corrección se aplica al escribir desde los formularios y no requiere migración ni intervención sobre los datos históricos.
- Probar altas y duplicados por POST con datos ficticios, incluido un lote histórico con minúsculas y una ruta directa denegada.
