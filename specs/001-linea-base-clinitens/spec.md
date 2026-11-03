# 001 — Línea base y adaptación SDD de CliniTENS

Fecha: 2026-10-07. Estado: entrega documental para revisión. Fuente: petición del usuario de escanear el proyecto, adaptar los Markdown genéricos y dejar observaciones/problemas en docs. Edición documental autorizada; implementación funcional NO autorizada. Aceptación del usuario pendiente.

## Problema y resultado

El kit SDD recibido describe ejemplos genéricos y no identifica la aplicación existente. Se necesita documentación útil para continuar CliniTENS, con estructura, reglas observadas, comandos comprobados y hallazgos localizables, preservando implementación y datos.

## Actores

Solicitante revisa prioridades y acepta la documentación. Agente inspecciona fuentes y adapta Markdown. Actores de la aplicación: estudiante RESTRICTED, docente MANAGER, administrador ADMIN y superusuario Django; no se cambia su acceso en esta entrega.

## Alcance y exclusiones

Incluye README, AGENTS, presentación de constitution, manual, docs, prompts, índice/plantillas SDD y esta spec con plan/tareas/validación. Incluye revisión estática y comprobaciones en memoria para sustentar el inventario. Se permite renombrar el informe de observaciones.

Excluye correcciones, nuevos módulos, código ejecutable persistente, migraciones, dependencias, cambios de datos, build, deploy, commit/push y lectura de secretos/datos reales. No convierte hallazgos en tareas de código aprobadas ni da por aceptadas las reglas heredadas.

## Requisitos documentales

- RF-001-01: Documentar tecnologías, módulos, rutas, datos, permisos y flujos a partir de fuentes reales, separando inferencias y desconocidos.
- RF-001-02: Sustituir referencias genéricas incompatibles y adaptar guías/plantillas al contexto CliniTENS, manteniendo explícita la fase de trabajo.
- RF-001-03: Registrar observaciones y problemas con ID, prioridad sugerida, fuente, impacto/acción y estado de comprobación.
- RF-001-04: Mantener spec, plan, tareas e índice con alcance verificable y sin autorización implícita de código.
- RF-001-05: Registrar resultados reales y límites de verificación, conservar código/datos/cambios previos y dejar trazabilidad/punto de reanudación.

## Línea base funcional observada

La siguiente tabla describe código, no requisitos normativos aprobados ni funcionalidad probada.

| Área | Comportamiento / fuente | Asuntos abiertos |
|---|---|---|
| Identidad | User estándar, Profile/Position, allauth y registro público cerrado; UsuarioApp/core | Quién administra cuentas/cargos; lista global; superusuario inconsistente |
| Gestión docente | CRUD casos, códigos, pacientes/resultados; CliniTensDocenteApp | Compartir catálogo, validación de uploads, publicación de resultados |
| Cursos | Nombre único; matrícula, XLSX, cuentas temporales; consultas por creador | Historial de esquema, identidad/importación y credenciales |
| Ficha | Código activo/docente, JSON de 13 secciones, guardar/enviar; CliniTensFichaApp | Completitud, esquema JSON, curso/docente y concurrencia |
| Evaluación | 15 indicadores; nota 1,0–7,0 con exigencia 60%; revisión/PDF | Borrador/publicación coherentes y permisos de exportación |
| Presentación | Portadas, layouts, Tailwind 3, Alpine; seguimiento por petición | Enlaces sin destino, build y navegador pendientes |

## Datos y permisos

Modelos: Position/Profile, CasoClinico/CasoMultimedia, CodigoActividad, Paciente/PacienteMultimedia, ResultadoDiagnostico, Curso y FichaClinica. Curso enlaza estudiantes; ficha enlaza estudiante/docente/código y es única por estudiante/código. Estados BORRADOR/ENVIADA/CALIFICADA. No hay relación directa código–curso ni caso–paciente.

Mixin docente permite ADMIN/MANAGER activos y superusuario; estudiante exige perfil con RESTRICTED/MANAGER/ADMIN y propiedad de ficha. Cursos se filtran por creador; catálogos clínicos no. Helper de fichas da acceso global a ADMIN y asignado a otros perfiles. Matriz completa en [arquitectura](../../docs/ARQUITECTURA_BASE.md); inconsistencias en OBS-004 a OBS-006.

Para el escaneo no se consultan registros ni secretos. Usar configuración ficticia, base en memoria y medios temporales. No documentar contenido de db.sqlite3/media como demostrativo sin comprobarlo.

## Criterios de aceptación

| RF | Dado / cuando | Resultado observable |
|---|---|---|
| 01 | Se consulta contexto/arquitectura | Coinciden con apps/settings/rutas/modelos existentes; inferencias y desconocidos identificados |
| 02 | Se leen instrucciones/plantillas | Tailwind 3 y rutas reales; ningún enlace obliga a contexto ausente ni a settings de pruebas inexistentes |
| 03 | Se abre observaciones | Hallazgos identificados con evidencia/estado; propuestas distinguidas de arreglos |
| 04 | Se consulta spec e índice | Plan/tareas/validación enlazados; no hay tareas funcionales autorizadas |
| 05 | Se revisa cierre/Git | Resultados reales, cero tests explicitado, referencias locales válidas y código/datos preservados |

## Compatibilidad y pendientes

Preservar nombres de apps/rutas y eliminación previa del RAR. Mantener principios generales de constitution; solo adaptar presentación, sin flexibilizar autorización. No inventar hosting, responsables institucionales, certificaciones o reglas pedagógicas. Revisión de la documentación y priorización de correcciones pendientes del usuario.
