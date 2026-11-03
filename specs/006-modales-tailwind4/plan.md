# Plan técnico — 006 / Modales con Tailwind 4

Spec: [spec.md](spec.md). Fecha: 2026-10-21. Plan documental revisado por el usuario y posteriormente autorizado. Implementación local realizada; evidencia y límites en [validation.md](validation.md). Las secciones de propuesta conservan el plan previo como antecedente.

## Base inspeccionada

Leídos AGENTS, constitution, README, proyecto, estado, arquitectura, observaciones, índice, decisiones, trazabilidad, guía visual y entorno. Specs relacionadas: 003 (interfaz), 004 (migración Tailwind) y 005 (FarmaTEF vigente, sin ampliar su alcance). Guías aplicadas: `06-cambios`, seguida de `01-especificar`, `02-planificar` y `03-tareas` solo para los documentos. No se ejecutan 04/05.

Sin `.git`: no hay comparación fiable con commits anteriores; conservar archivos presentes. Se registraron hashes de 254 archivos de implementación/reglas/recursos antes de editar documentación para cotejo al cierre. No se leyeron secretos, base ni medios.

## Integración propuesta, no implementada

Ampliar presentación existente, sin apps ni componentes obligatorios nuevos. Primero reproducir en una instancia aislada con fixtures y CSS servido real; comprobar posición, estilos computados, consola y controles de apertura/cierre. Si el problema es el margen de `dialog.account-dialog`, preferir una corrección de centrado acotada al selector existente. La regla base global sugerida por Tailwind es alternativa, solo si se demuestra necesaria y no altera otros diálogos.

No desactivar Preflight ni elevar `z-index` globalmente como sustituto del diagnóstico. Conservar el diálogo nativo de cuentas. Para pacientes, mantener su implementación si satisface aceptación; si no, corregir el defecto observado con el menor cambio necesario. No imponer una migración general a `dialog` sin justificación registrada.

| RF | Archivo existente / condición | Cambio propuesto | Verificación prevista |
|---|---|---|---|
| RF-006-01/02 | `static/css/styles.css` (`.account-dialog`) y, si hace falta, `templates/pages/usuarios/usuarios_lista.html` | Centrado/máximos de altura/scroll explícitos sin sobrescribir display de estado cerrado; conservar `showModal`/`close` | Cuentas antes/después, escritorio/tablet/móvil, zoom, teclado, cierre y reapertura |
| RF-006-02/03 | `templates/pages/clinitens/docente/pacientes.html` | Revisar nombre/foco/fondo/scroll y lectura asíncrona; editar solo incompatibilidades reproducidas | Carga, error/red, Escape/exterior, Tab, aperturas sucesivas con respuesta tardía |
| RF-006-02 | `templates/components/modal/modal.html`, `static/js/modal.js`, solo con consumidor confirmado | Resolver coherencia `hidden`/Alpine/API nativa y asociación de título si se demuestra uso afectado; H2/H3 al tocar título | Incluir ruta/activador real en inventario; si no aparece, registrar «sin cambio» y motivo |
| RF-006-04 | `UsuarioApp/views.py`, `CliniTensDocenteApp/views.py`, `core/mixins.py`, `core/permissions.py`, URLs | Referencia para regresión; no se prevén cambios de backend | GET/POST permitidos/denegados y ausencia de escrituras al cancelar |
| RF-006-05 | `theme/static_src/src/styles.css`, `build.cjs`, `build.test.cjs`, salida `theme/static/css/dist/styles.css` | Fuente CSS solo si lo requiere el diagnóstico; mantener fuentes acotadas y reemplazo temporal; salida únicamente por build | Reglas esperadas presentes y fallo/incompletitud conserva CSS anterior |

No se propone editar `base.html` ni cargar el helper dormido para fabricar un consumidor. Si una solución requiere tocar otro archivo, registrar necesidad y relación con RF antes de editar. Usar tokens, botones y H1 de `page_title` actuales.

## Datos, contratos y permisos

No cambia persistencia: ninguna migración, respaldo de datos reales ni transacción nueva. Preservar URLs, `method`, CSRF, filtros/search/inactive, sanitización DOMPurify del helper si llega a tocarse, escape de Django y `x-text` de paciente. No usar datos reales para reproducir.

Regresiones de cuentas incluyen POST autorizado, propia cuenta sin modificación, superusuario protegido y rechazo de MANAGER/RESTRICTED/inactivo/sin cargo. Pacientes incluye MANAGER propio/ajeno y ADMIN/superusuario global; anónimo redirigido a acceso. Superusuario activo sin perfil conserva las excepciones existentes. La API de detalle conserva su JSON; no incorporar datos ni historial nuevo.

## Secuencia y validación futura

1. Tras instrucción del usuario, comprobar disponibilidad del intérprete actual y recursos Node, sin sustituir `.venv`. Si el target sigue roto, registrar bloqueo; su reparación es tarea separada y no se presenta como realizada.
2. Reproducir con `core.test_settings`, base/medios ficticios y estáticos locales. Confirmar ruta y CSS realmente servido antes de decidir la corrección.
3. Corregir consumidores confirmados; los demás son regresión. Añadir prueba del fallo reproducido si requiere lógica; no crear pruebas que solo repitan clases o CSS de implementación.
4. Ejecutar build y controles JS existentes. Ejecutar pruebas de permisos/formularios afectadas y controles Django apropiados con intérprete válido. Registrar comandos reales; ver [validation.md](validation.md).
5. Revisar navegador a 1440/768/390 px, zoom 200%, teclado, contenido largo y movimiento reducido. Comprobar portadas, ficha y FarmaTEF como regresión de estilos, sin activar funciones pendientes.
6. Actualizar evidencia, trazabilidad y pendientes; solicitar aceptación humana solo sobre resultado comprobado.

No hay cambios de PDF/Excel previstos. No se requiere revisarlos si no se modifican sus flujos/recursos. Los resultados históricos de 004 no acreditan 006.

## Riesgos, reversión y pendientes

Riesgos: confundir margen con ciclo de apertura; parche global que mueva otros overlays; helper sin uso; fallos de foco o peticiones tardías previos a la migración; CSS servido distinto de la fuente. Registrar cada caso con evidencia y no ampliar a una limpieza general.

Reversión futura: guardar copia de los archivos concretos antes del cambio, preservar modificaciones ajenas y restaurar solo el parche identificado. Si cambia la fuente compilada, restaurarla y regenerar CSS con el mismo lock; si build falla, conservar salida anterior. Sin `.git`, no citar commits históricos como mecanismo disponible. No restaurar base/media ni ejecutar operaciones Git destructivas.

P-006-01/02/03 describían los pendientes documentales iniciales; su resolución está registrada en spec/validation. La entrega documental no ejecutó código; la autorización posterior permitió las comprobaciones de esta implementación.

## Integración finalmente implementada

Se corrigieron `static/css/styles.css` y `templates/pages/clinitens/docente/pacientes.html`; la salida de Tailwind fue regenerada por el build existente. Se añadió `static/js/paciente-modal.test.cjs` para ejecutar el controlador real con respuestas diferidas y comprobar el fallo antes/después. Este archivo adicional concreta la regresión prevista, no introduce un controlador nuevo ni una dependencia.

El defecto de foco del overlay quedó reproducido en navegador: Tab alcanzaba «Editar paciente» detrás. Se justificó cambiar solo ese overlay a `dialog.showModal()/close()`, aprovechando foco/fondo inerte del navegador sin implementar una trampa artesanal ni un framework. Conserva lectura JSON, cierre exterior y acciones existentes; el error ahora se muestra dentro con cierre siempre disponible. Un contador invalida respuestas y errores de consultas anteriores.

Validación con Python instalado 3.12.0 + paquetes existentes del target, importando exclusivamente `core.test_settings`, sin reparar `.venv`/target. Arnés temporal en `.test-artifacts/modales-006/review.py`, base ficticia `.test-artifacts/modales-006-review.sqlite3`; no se añaden endpoints del producto. Pendientes: zoom 200%, emulación de movimiento reducido y aceptación funcional humana.
