# Tareas documentales — 001

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Petición del 2026-10-07 autoriza documentación; implementación funcional NO autorizada.

- [x] T-001-01 — Escanear estructura, tecnología, Git y comportamiento.
  - RF: RF-001-01. Dependencia: ninguna.
  - Fuentes: core, apps, theme, templates, utils, requirements y Git.
  - Hecho: inventario real con permisos/datos y límites en docs.
- [x] T-001-02 — Adaptar instrucciones, contexto y guías SDD.
  - RF: RF-001-02. Depende de T-001-01.
  - Archivos: README, AGENTS, constitution, manual, docs, prompts, specs/_templates.
  - Hecho: referencias de proyecto reales y fases explícitas; placeholders solo para futuras solicitudes.
- [x] T-001-03 — Registrar problemas/observaciones.
  - RF: RF-001-03. Depende de T-001-01.
  - Archivo: docs/OBSERVACIONES_PROYECTO.md, renombrado desde OBSERVACIONES_BASE.
  - Hecho: 23 entradas con fuente/estado y acciones sugeridas no autorizadas.
- [x] T-001-04 — Crear paquete SDD de esta entrega y actualizar índice.
  - RF: RF-001-04. Depende de T-001-01 a 03.
  - Archivos: esta carpeta y specs/README.
  - Hecho: spec/plan/tareas/validación coherentes, sin tareas de código aprobadas.
- [x] T-001-05 — Verificar documentación y registrar cierre.
  - RF: RF-001-05. Depende de T-001-02 a 04.
  - Archivos: validation, VERIFICACION, VALIDACION_SDD, TRAZABILIDAD y ESTADO.
  - Hecho: checks reales, límites, enlaces y preservación registrados.

## Evidencia y reanudación

2026-10-07: revisión y comandos en [validation.md](validation.md) y [VERIFICACION.md](../../docs/VERIFICACION.md). No hay tarea funcional autorizada. Próximo paso: revisión humana y elección de corrección para nueva spec. Aceptación del usuario pendiente; no marcarla por tener checks exitosos.
