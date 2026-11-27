# Tareas — 037

[Spec](spec.md) · [Plan](plan.md). Implementación autorizada el 2026-11-26 mediante «autorizo».

- [x] T-037-01 — Inspección y documentación del alcance, aceptación y plan. Evidencia: validation.md.
- [x] T-037-02 — Revisar propuesta y autorizar implementación; precio CLP pendiente de revisión. Tipo aclarado por la usuaria: clasificación del arsenal adjunto; no equivale a autorización de código.
- [x] T-037-03 — RF-01/02: candado persistente, CAS, controles de geometría y regresiones. Depende de 02. Hecho cuando recarga conserva estado y POST bloqueado/obsoleto no cambia geometría.
- [x] T-037-04 — RF-03/04: precio alta/edición/listado y filtro por tipo. Depende de 02. Hecho cuando validaciones y filtros pasan con aislamiento por propietario.
- [x] T-037-05 — RF-05/06: servicio/formulario/historial, motivos, idempotencia y protección admin. Depende de 02. Hecho cuando saldo e historia coinciden y no hay edición manual sin motivo.
- [x] T-037-06 — RF-07: integrar altas/consumos existentes. Depende de 05. Hecho cuando fallo revierte todo y reenvío no duplica movimientos.
- [x] T-037-07 — Generar/revisar/ensayar migraciones y recuperación en fixture. Depende de 03/04/05. No aplicar a base habitual.
- [ ] T-037-08 — Checks, regresiones, URL directa permitida/denegada, navegador y build pertinente; actualizar evidencia/trazabilidad/estado. Depende de 03–07. Aceptación humana posterior.

## Reanudación

Implementación y pruebas automáticas completadas; T-037-08 parcial por navegador local inaccesible. Próximo: revisar visualmente, después activar 0012/0013 en base habitual con respaldo y autorización específica. Sin cambios en datos habituales, dependencias, commit/push o despliegue.
