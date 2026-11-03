# Trazabilidad de requisitos, tareas y pruebas

La trazabilidad relaciona cada requisito del producto con las tareas, el diseño o código que lo implementa y la evidencia disponible. «Implementado» indica que existe código; «verificado» indica que hay evidencia de comprobación; «aceptado» requiere revisión de las personas responsables del producto. No se debe inferir aceptación a partir de la existencia del código.

## Matriz

| Requisito | Tarea(s) | Diseño o código real | Prueba automatizada | Otra evidencia | Estado | Limitaciones |
|---|---|---|---|---|---|---|
| RF-002-01 — excluir base y medios del índice | T-002-07 | `.gitignore` y migraciones de las apps | Verificación de índice/esquema ficticio registrada en validación 002 | Archivos locales conservados; historia previa no purgada | Verificado en 002 | No implica limpieza de la historia Git |
| RF-002-02 — pruebas aisladas de datos reales | T-002-01, T-002-08 | `core/test_settings.py`, helpers y pruebas de cuatro apps | 47 pruebas Django registradas en la línea base | Configuración separada de `.env` y base real | Verificado en línea base | No equivale a cobertura total |
| RF-002-03 — permisos por rol y propiedad | T-002-02 | Permisos centrales, mixins, vistas, formularios y admin | Regresiones de permisos registradas en validación 002 | Revisión de accesos y URLs directas | Verificado en 002 | Sin certificación de operación productiva |
| RF-002-04 — validación de ficha y versiones | T-002-03 | `CliniTensFichaApp/validation.py`, modelos, vistas y editor | Regresiones de esquema, completitud y versiones registradas en 002 | Reglas de validación documentadas | Verificado en 002 | Requiere validación con usuarios del producto |
| RF-002-05 — publicación consistente de rúbrica | T-002-03 | Evaluación, rúbrica y modelos de ficha | Pruebas de publicación/borrador registradas en 002 | Reglas de publicación documentadas | Verificado en 002 | Aceptación funcional pendiente |
| RF-002-06 — archivos y resultados protegidos | T-002-04 | Validadores, sanitización HTML, medios privados y vistas de resultados | Casos de archivo/HTML/acceso registrados en 002 | Límites y acceso documentados | Verificado en 002 | SMTP y operación externa no verificados |
| RF-002-07 — importación y credenciales seguras | T-002-05 | Importación, credenciales, middleware y señales de usuario | Casos de rollback, tokens y expiración registrados en 002 | Reglas de identidad y contraseña documentadas | Verificado en 002 | Integraciones externas no verificadas |
| RF-002-08 — actividad y métricas | T-002-06 | Perfil, middleware, vistas y lista de usuarios | Regresiones de consultas/actividad registradas en 002 | Reglas de consulta y filtros documentadas | Verificado en 002 | No es prueba de carga |
| RF-002-09 — compilación y recursos frontend | T-002-06 | Configuración/build de Tailwind y recursos locales | Build y `build.test` registrados en 004 | Conservación de CSS ante fallo y revisión visual documentadas | Verificado en 004 | No valida todos los navegadores/dispositivos |
| RF-002-10 — sesión, contenido y medios | T-002-04, T-002-06 | URLs/settings, medios y `mensajes.js` | Casos de logout, medios y avisos registrados en 002 | Detalle en validación 002 | Verificado en 002 | SMTP y operación productiva pendientes |
| RF-002-11 — documentación y recuperación | T-002-08 | `docs/`, `AGENTS.md`, README, manual, prompts y specs | No aplica como prueba funcional | Documentación de estado, límites y recuperación | Documentado | Revisión y aceptación del producto pendientes |
| RF-003-01 — estructura visual compartida | T-003-01, T-003-02 | Layout, `app_shell`, bases y componentes | No aplica como prueba aislada | Revisión de portadas y navegación registrada en 003 | Implementado y revisado | Aceptación de usuarios pendiente |
| RF-003-02 — portadas y navegación por tarea | T-003-03 | Plantillas de inicio, CliniTENS y FarmaTEF | No aplica como prueba aislada | Capturas con datos ficticios registradas en 003 | Implementado y revisado | Funciones aún no implementadas se muestran como pendientes |
| RF-003-03 — formularios y errores | T-003-04 | Plantillas docente/usuarios/perfil y componentes de formulario | Regresiones de formularios registradas en 003 | Revisión de errores y valores preservados | Implementado y revisado | No cubre todos los navegadores |
| RF-003-04 — flujo de ficha y rúbrica | T-003-05 | Editor de ficha, casos/resultados y rúbrica | Regresiones y pruebas de línea base registradas en 003 | Revisión del flujo en navegador | Implementado y revisado | Aceptación de usuarios pendiente |
| RF-003-05, RF-003-06 — adaptación visual | T-003-06 | `styles.css`, `mensajes.css`, `design-system.js` | Controles automatizados según validación 003 | Revisión en anchos 1280/1440, 768 y 390 px | Implementado y revisado | No equivale a certificación exhaustiva de accesibilidad |
| RF-003-07 — sistema visual y guía | T-003-07 | Tokens, Tailwind y `PERSONALIZACION_VISUAL.md` | Build registrado en 003/004 | Guía visual documentada | Implementado y verificado | Aceptación de usuarios pendiente |
| RF-004-01 — inventario de dependencias | T-004-01 | Manifiestos Python/Node e inventario | Comandos de inventario/auditoría registrados en 004 | Dependencias directas, transitivas y bundles identificados | Verificado en 004 | Auditorías no cubren todos los riesgos operativos |
| RF-004-02 — Tailwind 4 y build reproducible | T-004-02 | CSS, configuración, CLI, clases y `build.test` | Build y cuatro pruebas JS registrados en 004 | Conservación de CSS ante error y revisión visual documentadas | Verificado en 004 | Alcance limitado al entorno registrado |
| RF-004-03 — Django y autenticación | T-004-03 | Settings normal/de prueba, apps y migraciones | 47 pruebas Django y controles registrados en 004 | Migraciones probadas con datos ficticios | Verificado en 004 | No se aplicó a la base recibida |
| RF-004-04 — auditoría de dependencias | T-004-04 | Inventario y artefactos de evidencia | pip/npm audit según validación 004 | Bundle CKEditor informado por separado | Verificado con límites | Resultados no cubren runtimes ni bundles excluidos |
| RF-004-05 — preparación operativa | T-004-05 | Informe preproducción, entorno y recuperación | No aplica como prueba funcional | Riesgos y condiciones operativas documentados | Documentado | Sin despliegue ni aceptación operativa |
| RF-005-01 — definición de alcance y documentación | T-005-01, T-005-08, T-005-09 | [Borrador de solución](borradores/PREINFORME_EVS2_FARMATEF_CLINITENS_2026.md), spec y plantilla de trabajo | No aplica todavía | Requisitos y procesos descritos en documentos | En elaboración | El borrador contiene estructura de una plantilla anterior; revisar antes de compartir externamente |
| RF-005-02 — paquete de documentación del producto | T-005-02, T-005-07, T-005-09 | Documento de arquitectura, procesos, datos, operación y anexos por completar | No aplica todavía | KPI/SLA y estándares figuran como propuestas | En elaboración | Las métricas deben acordarse y medirse; falta revisión de responsables |
| RF-005-03 — recorrido funcional de inventario y dispensación | T-005-04, T-005-05 | `FarmaTEFApp/` y recorrido de inventario docente | No se ejecutaron pruebas para 005 | Objetivo: demostración funcional revisable por usuarios del negocio | Parcialmente implementado, sin validar | Receta, dispensación y recorrido de usuario final pendientes |
| RF-005-04 — dispensación atómica | T-005-05 | Diseño por completar según reglas operativas | No ejecutada | Criterio definido en spec 005: validación y actualización de stock en una operación | Pendiente | Reglas de receta, cantidad y sustitución por acordar |
| RF-005-05 — inventario, lotes y alertas | T-005-03, T-005-04 | Modelos `Medicamento` y `LoteInventario`, formulario/listado docente | No se ejecutaron pruebas para 005 | Alertas diseñadas a partir de datos almacenados | Implementado, sin validar | Migración manual `0001_initial` requiere cotejo automático |
| RF-005-06 — contenido asistido y aprobación | T-005-06 | Flujo externo aún no integrado | No aplica todavía | La spec exige revisión y aprobación antes de publicar contenido generado | Pendiente | Proveedor, costo, privacidad y condiciones por definir |
| RF-005-07 — arquitectura, calidad e indicadores | T-005-02, T-005-07 | Borrador de solución y artefactos de spec 005 | No aplica todavía como prueba de código | BPMN/UML/KPI/SLA y estándares propuestos | En elaboración | Deben reflejar el producto real; indicadores aún no medidos |
| RF-005-08 — autorización en servidor | T-005-03, T-005-04 | Permisos centrales y vistas/formularios FarmaTEF | No se ejecutaron pruebas para 005 | Criterios de URL directa y propiedad descritos en spec | Implementado en código, sin validar | Falta ejecutar pruebas con usuarios ficticios y validar acceso denegado |

## Implementación local — 006 / Modales con Tailwind 4

Relación con RF-004-02 y RF-003-03/05/06: corrección de compatibilidad e interacción existente; no sustituye su evidencia histórica. Código autorizado tras revisión; tareas técnicas realizadas salvo verificación visual parcial T-006-06.

| Requisito | Tarea(s) previstas | Archivos existentes afectados / referencia | Evidencia disponible | Estado / límite |
|---|---|---|---|---|
| RF-006-01 — centrado y adaptación | T-006-02/03/06 | `usuarios_lista.html`, `static/css/styles.css`, CSS compilado | Antes (0,0) y después centrado; capturas/medidas a 1440/768/390 | Implementado/comprobado; zoom 200% pendiente |
| RF-006-02 — apertura, cierre y teclado | T-006-02/03/04/06 | Cuentas/pacientes con dialog nativo; helper compartido intacto | Foco, Escape/clic exterior, reapertura y fondo bloqueado en IAB; prueba de clic exterior | Implementado/comprobado con límites; movimiento reducido no emulado ni otros motores revisados |
| RF-006-03 — carga y errores de pacientes | T-006-02/04/06 | `pacientes.html`, `static/js/paciente-modal.test.cjs` | Cuatro fallos antes, cinco regresiones correctas después; éxito/carga/cambio paciente en navegador | Implementado; red/error verificados en controlador, no inducidos en UI integrada |
| RF-006-04 — permisos y contratos preservados | T-006-05 | Backend existente intacto, nueve hashes de referencias coincidentes | 35 pruebas Django, 21 GET y cuatro POST sobre fixtures; matriz JSON | Verificado en alcance 006; no es suite completa ni validación 005 |
| RF-006-05 — build y regresión transversal | T-006-06/07 | Build/controles existentes, portadas/ingreso ficha/FarmaTEF | Build 4.3.3 correcto y nueve JS; regresión móvil sin desbordamiento | Comprobado con límites; no prueba todos los flujos ni aceptación humana |

Paquete: [spec](../specs/006-modales-tailwind4/spec.md), [plan](../specs/006-modales-tailwind4/plan.md), [tareas](../specs/006-modales-tailwind4/tasks.md) y [validación](../specs/006-modales-tailwind4/validation.md). Implementación autorizada y realizada; aceptación final pendiente. Evidencias de permisos/interfaz/regresión y capturas en `docs/evidencias/006-modales/`.

## Reglas de lectura

- Durante el diseño, marcar rutas y pruebas como propuestas o no ejecutadas.
- Tras implementar, registrar archivos y pruebas reales; incluir comando, entorno, resultado y límites en `validation.md`.
- No reutilizar resultados de otra spec como evidencia de un requisito nuevo.
- Una prueba puede respaldar más de un requisito; esta matriz no representa porcentaje de cobertura.
- Una prueba de backend no demuestra por sí sola interacción JavaScript, diseño adaptable, accesibilidad ni legibilidad de documentos.
- Diferenciar código implementado, validación técnica y aceptación de usuarios responsables.
- No presentar KPI, SLA o fechas como compromisos hasta que las partes responsables los acuerden.

## Referencias

- [Spec 001 — línea base histórica](../specs/001-linea-base-clinitens/spec.md)
- [Spec 002 — correcciones](../specs/002-correcciones-observaciones/spec.md) y [validación](../specs/002-correcciones-observaciones/validation.md)
- [Spec 003 — rediseño](../specs/003-redisenio-integral/spec.md) y [validación](../specs/003-redisenio-integral/validation.md)
- [Spec 004 — dependencias](../specs/004-actualizacion-dependencias/spec.md) y [validación](../specs/004-actualizacion-dependencias/validation.md)
- [Spec 005 — FarmaTEF](../specs/005-farmatef-mvp-informe2/spec.md), [plan](../specs/005-farmatef-mvp-informe2/plan.md), [tareas](../specs/005-farmatef-mvp-informe2/tasks.md) y [validación](../specs/005-farmatef-mvp-informe2/validation.md)
- [Spec 006 — modales con Tailwind 4](../specs/006-modales-tailwind4/spec.md), [plan](../specs/006-modales-tailwind4/plan.md), [tareas](../specs/006-modales-tailwind4/tasks.md) y [validación](../specs/006-modales-tailwind4/validation.md)


## Datos de catálogo autorizados — 2026-10-31

RF-005-05 / inventario existente: 109 medicamentos del Vademécum 2023 cargados en base habitual bajo valita tras aprobación de tabla. Sin cambios de código/esquema; sin lotes ni stock cargado. Cantidades ficticias preparadas aparte. Evidencia, límites y recuperación en la sección de carga de `specs/005-farmatef-mvp-informe2/validation.md` y `output/farmatef/vademecum-2023-carga.json`. Los 11 suplementos siguen pendientes. No valida dispensación ni pruebas futuras.
