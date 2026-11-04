# Especificaciones SDD — CliniTENS

## Índice real

| Número | Alcance | Ruta | Estado | Código autorizado |
|---|---|---|---|---|
| 001 | Escaneo, línea base y adaptación documental | [001-linea-base-clinitens](001-linea-base-clinitens/spec.md) | Escaneo histórico 2026-10-07 | No |
| 002 | Correcciones OBS-001 a OBS-023 | [002-correcciones-observaciones](002-correcciones-observaciones/spec.md) | Implementada/verificada; revisión humana pendiente | Sí, 2026-10-08 |
| 003 | Rediseño integral y coherencia visual | [003-redisenio-integral](003-redisenio-integral/spec.md) | Implementada/verificada; revisión humana pendiente | Sí, 2026-10-08 |
| 004 | Actualización de dependencias y revisión preproducción | [004-actualizacion-dependencias](004-actualizacion-dependencias/spec.md) | Implementada/verificada; pendientes operativos documentados | Sí, 2026-10-08 |
| 005 | MVP FarmaTEF y preparación del Informe 2 | [005-farmatef-mvp-informe2](005-farmatef-mvp-informe2/spec.md) | Borrador de trabajo; alcance en desarrollo | Sí, solicitud explícita del equipo 2026-10-17; aceptación académica pendiente |
| 006 | Compatibilidad de modales con Tailwind 4, transversal | [006-modales-tailwind4](006-modales-tailwind4/spec.md) | Implementada localmente; pruebas/build/navegador con límites; zoom/movimiento reducido y aceptación pendientes | Sí, después de revisión: «ya revisé, puedes implementar», 2026-10-21 |
| 007 | Actualización de arsenal APS 2024–2026 | [007-arsenal-aps-2024-2026](007-arsenal-aps-2024-2026/spec.md) | Implementación y carga local autorizadas; revisión pendiente | Sí, confirmación de la usuaria |
| 008 | Recetas y dispensación simulada | [008-recetas-dispensacion](008-recetas-dispensacion/spec.md) | Implementación local | Sí, solicitud explícita de la usuaria |
| 009 | Historial y entrega parcial de recetas | [009-historial-entrega-parcial](009-historial-entrega-parcial/spec.md) | Implementación local | Sí, solicitud explícita de la usuaria |
| 010 | Práctica estudiantil de validación y dispensación | [010-practica-estudiantil-recetas](010-practica-estudiantil-recetas/spec.md) | Implementada localmente; checks básicos; navegador y aceptación pendientes | Sí, «me gusta, hazlo», 2026-11-04 |
| 011 | Eliminar recetas sin actividad desde el historial | [011-eliminar-recetas-sin-actividad](011-eliminar-recetas-sin-actividad/spec.md) | Implementación local; revisión navegador pendiente | Sí, petición explícita, 2026-11-04 |
| 012 | Docentes colaboradores para recetas FarmaTEF | [012-docentes-colaboradores-farmatef](012-docentes-colaboradores-farmatef/spec.md) | Implementado localmente; migración aplicada con respaldo; revisión funcional pendiente | Sí, «sí», 2026-11-04 |
| 013 | Etiquetado de lotes con impresión en milímetros | [013-etiquetado-farmatef](013-etiquetado-farmatef/spec.md) | Implementación local; revisión de impresión física pendiente | Sí, solicitud explícita, 2026-11-04 |

La 001 describe la petición documental y el comportamiento observado, sin aprobar retrospectivamente reglas de negocio. Hallazgos en [observaciones](../docs/OBSERVACIONES_PROYECTO.md) e [informe preproducción](../docs/VALIDACION_PREPRODUCCION.md). 005 conserva su alcance y autorización; 007–013 amplían FarmaTEF conforme a solicitudes posteriores. Siguiente número libre observado: 014.

## Organización

Cada alcance concreto contiene spec.md, plan.md, tasks.md y validation.md. Una spec puede afectar varias apps o ampliar una existente. Las plantillas de [_templates](_templates/spec.md) están adaptadas a CliniTENS, pero sus campos `<...>` deben completarse; no son requisitos aprobados.

Identificadores RF-NNN-XX y T-NNN-XX permanecen estables. Requisitos → archivos/tareas → evidencia se relacionan en [TRAZABILIDAD](../docs/TRAZABILIDAD.md).

Flujo: documento → revisión → autorización explícita de tareas de código → implementación → verificación → aceptación humana. Para una petición solo documental no se inicia implementación. Un checklist terminado no sustituye la aceptación del usuario ni permite desplegar.
