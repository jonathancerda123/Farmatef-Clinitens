# Plan técnico — 009

| RF | Cambio | Verificación |
|---|---|---|
| 009-01 | Lista histórica con estado/saldo/última entrega | `manage.py check` aislado; revisión de template |
| 009-02/04 | Saldo por línea y estado parcial | Migración aditiva, inspección de constraints |
| 009-03/05 | Varias dispensaciones por receta, detalle de lote por transacción y servicio atómico | Revisión estática |
| 009-06 | Marca persistida ficticia y etiquetas visibles | Revisión de modelo/plantillas |
| 009-07 | Casilla de selección por línea, validación de cantidad y servicio existente por FK de línea | Check aislado y revisión estática |
| 009-08 | Campo separado para sospecha de falsificación; bloquear entrega en servidor | Migración aditiva, check y revisión estática |
| 009-09 | Añadir líneas dinámicamente hasta el límite del formset | Revisión de plantilla/JS y sintaxis |

La migración debe preservar dispensaciones existentes convirtiendo la relación uno-a-uno a una relación uno-a-varios; registros existentes, si los hay, reciben cantidad entregada derivada del historial.
