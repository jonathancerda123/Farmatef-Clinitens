# Plan documental — 001

Spec: [spec.md](spec.md). Trabajo autorizado: inspección y Markdown. No hay diseño ni implementación de cambio funcional aprobado.

## Base inspeccionada

Raíz, Git, requirements, core, cuatro apps, theme, utils, plantillas, recursos y Markdown. Settings se inspeccionó selectivamente omitiendo valores sensibles. No se abrió .env, SQLite ni medios. Antes de editar: eliminación de CliniTENS.rar y Markdown sin seguimiento.

## Integración documental

| RF | Archivos | Acción y evidencia |
|---|---|---|
| 01 | README, docs/PROYECTO, ARQUITECTURA, ENTORNO | Inventario y fuentes reales; versiones, modelos/rutas/settings |
| 02 | AGENTS, MANUAL_SDD, constitution, prompts, specs/_templates | Sustituir contexto genérico; conservar principios/fases y campos reutilizables |
| 03 | docs/OBSERVACIONES_BASE → OBSERVACIONES_PROYECTO | Renombrar y completar hallazgos; actualizar referencias |
| 04 | specs/001-linea-base-clinitens y specs/README | Registrar alcance documental y comportamiento observado; no aprobación retrospectiva |
| 05 | VERIFICACION, VALIDACION_SDD, TRAZABILIDAD, ESTADO, validation | Evidencia aislada, enlaces y preservación de implementación |

Se conserva ARQUITECTURA_BASE como nombre de archivo para evitar renombrados innecesarios. El informe de observaciones se renombra con autorización del pedido. Las plantillas mantienen placeholders deliberados para cambios futuros; los documentos de contexto dejan de ser plantillas vacías.

## Comprobaciones

Inspección estática y Git; pip check; AST Python; compilación de plantillas HTML; Django check/dry-run/test usando settings importados sin read_env, clave ficticia, SQLite en memoria, medios temporales, caché/correo en memoria. Verificar enlaces locales Markdown y coherencia de RF/tareas/estado. Comparar estado de archivos de implementación con Git inicial.

No aplicar migraciones ni crear fixtures, pruebas persistentes, settings, scripts, endpoints o dependencias. No usar navegador sobre datos recibidos. Validación funcional propuesta para futura spec, no ejecutada aquí.

## Riesgos y reversión

Riesgo: convertir código defectuoso en requisito deseado. Mitigación: separar RF documentales, comportamiento observado y hallazgos. Otro riesgo: afirmar instalación reproducible con migraciones ignoradas; registrarlo como límite.

No hay cambios de esquema/contratos ni recuperación de datos que ejecutar. Reversión consiste en editar/restaurar únicamente Markdown; estos archivos eran locales sin seguimiento, por lo que Git no contiene su versión inicial. No usar reset/clean general ni restaurar el RAR. El renombrado de observaciones exige restaurar sus enlaces si se revierte.

## Decisiones posteriores

Prioridad de arreglos, política de permisos, publicación y datos requieren revisión humana y specs de corrección independientes. Registrar temas en roadmap no permite implementarlos.
