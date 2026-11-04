# 009 — Historial y entrega parcial de recetas

Fecha: 2026-11-04. Estado: implementación local autorizada. Fuente: solicitud de la usuaria para ver historial, permitir entrega completa o parcial y marcar cada receta como ficticia.

## Alcance

- Historial ordenado por fecha de creación, con estado, persona ficticia, número y resumen de entregas.
- Permitir una entrega por cantidades seleccionadas de cada línea, acumulable en varias transacciones; cero para no entregar una línea en esa transacción.
- Una transacción puede completar la receta; si queda saldo, la receta pasa a estado PARCIAL; al completar todo, pasa a ENTREGADA.
- Toda receta y transacción se marca explícitamente como ficticia/simulada.
- Separar la naturaleza sintética del registro (`es_ficticia`) de una sospecha de falsificación del documento presentado (`sospecha_falsificacion`). Una receta sospechosa no puede dispensarse y queda identificada en la consulta y el historial.
- Seleccionar explícitamente cada medicamento a entregar con casilla por línea; las líneas desmarcadas no generan movimientos ni descuentan existencias. Una línea marcada permite indicar una cantidad menor al saldo para una entrega parcial.
- Mantener propiedad por gestor y ámbito global de ADMIN/superusuario activo.
- Mantener el descuento transaccional FEFO por lotes vigentes; si una cantidad solicitada no tiene stock suficiente, no se guarda ninguna línea de esa transacción.

## Requisitos y aceptación

- RF-009-01: Historial muestra recetas pendientes, parciales, entregadas y vencidas sin perder las cerradas.
- RF-009-02: Cantidad por entregar de cada línea debe estar entre cero y su saldo; al menos una debe ser mayor que cero.
- RF-009-03: Las entregas parciales se auditan separadamente por fecha, usuario y lotes consumidos.
- RF-009-04: Receta pasa a PARCIAL o ENTREGADA según saldo total acumulado.
- RF-009-05: Stock insuficiente no deja descuento parcial dentro de la transacción solicitada.
- RF-009-06: Interfaz identifica receta y entregas como ficticias/simuladas.
- RF-009-07: La casilla por medicamento controla si esa línea participa en la entrega; cantidades y lotes quedan vinculados a la línea seleccionada.
- RF-009-08: La sospecha de falsificación es un atributo distinto de la simulación; bloquear despacho de recetas marcadas sospechosas.
- RF-009-09: El formulario permite añadir líneas de medicamento hasta el máximo de 10 definido por el servidor; una receta nueva puede incluir varios medicamentos.
