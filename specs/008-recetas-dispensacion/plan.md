# Plan técnico — 008

## Integración

| RF | Área | Cambio | Verificación |
|---|---|---|---|
| 008-01/04 | Modelos FarmaTEF | Receta, líneas, dispensación y detalle por lote; unicidad/estados | migración, inspección de restricciones |
| 008-02 | Vistas y formularios | CRUD mínimo docente, búsqueda por número, filtrado de propiedad | configuración aislada |
| 008-03/05 | Servicio | transacción, lotes vigentes FEFO, fallo total ante stock insuficiente | revisión estática y check |
| 008-06 | Plantillas | nueva pantalla, estados y etiqueta simulada | revisión del HTML |

## Reversión

La migración crea tablas nuevas y permite reversión estructural. No se alteran recetas o movimientos previos. No aplicar a entornos compartidos sin revisar y respaldar la base.
