# 026 — Número de lote en mayúsculas

Fecha 2026-11-16. Corrección autorizada por la solicitud directa sobre el inventario FarmaTEF.

En la captura se observan dos registros de un medicamento cuyo número de lote solo difiere por mayúsculas. Tienen distintas cantidades y fechas de vencimiento.

| Requisito | Criterio de aceptación |
|---|---|
| RF-026-01 | Al registrar un lote en FarmaTEF o Django admin, cualquier usuario autorizado guarda `AMOx-001` como `AMOX-001`. |
| RF-026-02 | Si el medicamento ya tiene ese número en cualquier combinación de mayúsculas y minúsculas, se informa el duplicado en el campo y el inventario conserva su saldo. |

Los permisos y la unicidad por medicamento se mantienen. Los registros históricos requieren revisión de su vencimiento, saldo e historial antes de corregirlos.
