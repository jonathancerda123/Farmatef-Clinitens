# Tareas — 014

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Código autorizado por la solicitud de implementar DAU, laboratorio y Kardex del 2026-11-04; solo simulación ficticia. No incluye migrar bases persistentes, commit/push ni despliegue.

- [x] T-014-01 — Añadir app, modelos de caso/etapas/intentos y migración aditiva.
  - RF: 014-02/03. Hecho cuando: relaciones con curso/estudiante e invariantes quedan en servidor.
- [x] T-014-02 — Implementar permisos de docente/estudiante y publicación de casos.
  - RF: 014-02/03/06. Depende de T-014-01. Hecho cuando: propiedad, colaborador, matrícula y estado se verifican en toda ruta.
- [x] T-014-03 — Crear flujo DAU educativo.
  - RF: 014-03/07. Depende de T-014-02. Hecho cuando: el estudiante registra datos del caso y cierre simulado.
- [x] T-014-04 — Crear flujo de laboratorio ficticio.
  - RF: 014-03/04/07. Depende de T-014-02. Hecho cuando: solicitudes/resultados guardan valores sin interpretación automática.
- [x] T-014-05 — Crear flujo Kardex ficticio con eventos protegidos.
  - RF: 014-03/05/07. Depende de T-014-02. Hecho cuando: acciones/omisiones/correcciones quedan atribuibles y sin edición silenciosa.
- [x] T-014-06 — Añadir navegación/portadas para tres módulos y conservar pendiente administración.
  - RF: 014-01. Depende de T-014-03/04/05.
- [ ] T-014-07 — Revisar autorización directa, curso y pantalla; documentar verificación.
  - RF: 014-01–08. Depende de tareas previas. Hecho cuando: se anotan solo resultados reales y límites.

## Autorización / ejecución

| Fecha | Tarea | Archivo / comando / entorno | Resultado y límite |
|---|---|---|---|
| 2026-11-04 | DOCUMENTAR | `specs/014-simuladores-clinicos/` | Alcance, criterios, integración y riesgos escritos; revisión académica pendiente. |
| 2026-11-04 | IMPLEMENTAR | `CliniTensSimulacionApp/`, plantillas, URLs, settings y portada | Primera versión local de los tres recorridos; check/migración/template-URL básicos correctos. Interacción navegador/roles y aceptación docente pendientes. |
| 2026-11-04 | CORREGIR ESQUEMA LOCAL | Respaldo en `.test-artifacts/backups/`; `manage.py migrate CliniTensSimulacionApp --noinput` | Error de tabla ausente resuelto aplicando únicamente las dos migraciones de la app; `showmigrations` las confirma y `manage.py check` pasa. No se inspeccionaron los registros. |

## Reanudación y aceptación

La usuaria pidió realizar los tres módulos; se limita el trabajo a simulación ficticia. Comenzar por modelos/permisos tras completar esta documentación. Conservar `docs/diagramas/` y `work/` sin seguimiento. Aceptación académica y de usuaria pendiente.
