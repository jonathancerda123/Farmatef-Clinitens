# Observaciones y correcciones — CliniTENS

Actualizado 2026-10-08. Usuario autorizó corregir todas las observaciones y confirmó propiedad por docente/ADMIN-superusuario global y envío de las 13 secciones completas o «No aplica». [Spec 002](../specs/002-correcciones-observaciones/spec.md), [verificación](VERIFICACION.md) y [recuperación](ENTORNO_Y_VERIFICACION.md).

**Implementada** describe la corrección local comprobada; no significa migración/despliegue ni aceptación clínica. El escaneo original se conserva al final como historia. No se leyeron .env, datos de SQLite ni medios recibidos; no se restauró el RAR.

## Estado actual por observación

| ID | Corrección / evidencia | Estado y límite |
|---|---|---|
| OBS-001 | Se retiró ignore de migraciones; originales/nuevas incluidas en índice. Creación de esquema ficticio y dry-run correctos | Implementada; aplicación respaldada a base real pendiente |
| OBS-002 | db.sqlite3/media ignorados y retirados del índice con --cached; git ls-files devuelve cero, archivos físicos existen | Implementada para árbol actual; historial/remotos no purgados |
| OBS-003 | core.test_settings independiente; 47 regresiones Django y 4 JS (004), todas correctas | Implementada; sin porcentaje de cobertura ni carga real |
| OBS-004 | Cuentas solo ADMIN/superusuario; cargos por permission_code, sin PK. ADMIN solo crea MANAGER/RESTRICTED; superusuario puede asignar ADMIN. Activar/desactivar superusuario devuelve 403. Django admin bloquea cambio de otro superusuario | Implementada; propietario puede editar su perfil. Cambios de privilegios por consola técnica reservados al superusuario |
| OBS-005 | Querysets/FK/CRUD/toggles por autor MANAGER, global ADMIN/superusuario. Cursos igual política | Implementada; vínculos heredados requieren revisión antes de operar con datos reales |
| OBS-006 | Permisos compartidos para fichas y PDF; login/GET/rol explícitos. Matriz anónimo/estudiante/propietario/ajeno/ADMIN/superusuario sin perfil | Implementada; estudiante sigue accediendo solo a ficha propia |
| OBS-007 | Esquema JSON/tipos/catálogos/límites, sección POST validada y completitud. Borrador guardado cuando envío incompleto | Implementada; identificación exige nombre/identificador/edad/sexo; las otras doce completas o No aplica |
| OBS-008 | Versión obligatoria y UPDATE condicional atómico; versión obsoleta 409 sin sobrescribir | Implementada; prueba de colisión lógica, no benchmark multicliente |
| OBS-009 | Puntajes estrictos, borrador separado, publicación completa/atómica y versión | Implementada; prueba de nota 7.0 y preservación de publicación previa |
| OBS-010 | Formularios y validadores para nuevos adjuntos: extensión/tamaño/firma, Pillow para imagen. Upload CKEditor directo 403 | Implementada; PDF/video solo firma, sin antivirus |
| OBS-011 | Token desde servidor, un uso/10 min, usuario/curso/sesión. Password fuera de HTML; inicial 24 h/cambio obligatorio. Excel celdas texto | Implementada; correo operativo requerido al caducar; caché compartida para varios workers |
| OBS-012 | Curso opcional en código; matrícula y docente responsable validados; sin reasignación libre | Implementada; códigos existentes sin curso siguen abiertos |
| OBS-013 | POST de habilitación propio/global y consumo estudiantil por caso; OCULTO no aparece ni se descarga | Implementada; resultado sin caso queda para gestión docente |
| OBS-014 | Actividad UPDATE sin procesar imagen; una actualización máximo cada 30 s. Imagen solo nueva/cambiada; borrado anterior tras commit | Implementada; timestamp probado sin resize |
| OBS-015 | XLSX corrupto acotado, identidad username/email coincidente, sin perfil parcial ni cambio de cargo. Transacción por fila/registro manual | Implementada; rollback de usuario/matrícula probado ante fallo de perfil |
| OBS-016 | Fuentes @source HTML/Python/JS acotadas; compilación temporal/reemplazo. Fallo o escaneo incompleto conserva CSS | Implementada; Tailwind 4 y regresiones de build en 004 |
| OBS-017 | Tarjetas sin ruta deshabilitadas «En desarrollo»; seguimiento recarga 30 s/pestaña visible/filtros URL | Implementada; sin WebSocket, navegación móvil mantiene tablas con scroll |
| OBS-018 | Logout POST, correo/HTTPS configurables; JS local/versionado, nh3 servidor, /media privado/nosniff/no-store | Implementada localmente; SMTP/proxy/cache externos pendientes; dependencias revisadas en 004, aviso del bundle editor documentado |
| OBS-019 | Lista con select_related/Exists; verificación corresponde a correo actual. Consulta única del queryset probada | Implementada; no benchmark de carga |
| OBS-020 | Count de estudiantes de fichas/actividad reciente; métricas usadas en UI | Implementada; total cuenta quienes iniciaron ficha, no toda matrícula |
| OBS-021 | es-cl, mensajes españoles/booleanos «Sí/No» en PDF; stub S3 eliminado | Implementada; no se implementó almacenamiento S3 |
| OBS-022 | Documentación adaptada; estado/spec/AGENTS/prompts actualizados al código actual | Implementada; spec 001 conserva escaneo histórico |
| OBS-023 | Toast variable como textContent, no interpretación HTML. Regresión con etiqueta img/onerror | Implementada; iconos son constantes del programa |
| OBS-024 | Lock anterior con 8 paquetes afectados (5 altos/3 moderados); Tailwind 4/CLI, retiradas y overrides en 004 | Resuelta en lock del proyecto: npm audit final 0; bundle CKEditor auditado por separado con un aviso pendiente |

OBS-024: fuentes principales del reporte npm, [braces](https://github.com/advisories/GHSA-vfj7-8cjw-p6xm) y [selector parser](https://github.com/advisories/GHSA-rj75-hqrm-r3gf). Son dependencias de herramientas de build; no se afirmó exposición de datos ni explotación del servidor. Avisos reales, sin prometer eliminación mediante audit fix --force.

## Próximo paso concreto

Revisar diff y aprobar operación sobre copia respaldada según [entorno](ENTORNO_Y_VERIFICACION.md). Preparar SMTP, proxy privado para media y caché compartida si hay múltiples workers. Revisar historia Git y los hallazgos PRE-005 a PRE-009 de [preproducción](VALIDACION_PREPRODUCCION.md): runtime parcheado, bundle editor, semillas MFA y operación. No ejecutar producción ni commit/push automáticamente.

---

# Escaneo histórico — 2026-10-07

Escaneo del 2026-10-07 sobre `main`, commit `4126cc7`. Sustituye `OBSERVACIONES_BASE.md`. No se abrió la base, `.env`, medios ni credenciales reales. No es auditoría exhaustiva ni prueba de explotación. **Comprobado estáticamente** significa que la condición aparece en código; su impacto puede necesitar reproducción. Correcciones pendientes de especificación y autorización.

Prioridad sugerida: alta para integridad/acceso/reproducibilidad; media para inconsistencias funcionales; baja para mantenimiento. No constituye trabajo aprobado.

| ID / prioridad | Hallazgo y evidencia | Consecuencia / acción sugerida | Estado |
|---|---|---|---|
| OBS-001 Alta | `.gitignore` ignora `migrations/`; `git check-ignore` lo confirma. Localmente: 1 migración de UsuarioApp, 5 de DocenteApp y 2 de FichaApp, fuera de seguimiento | Un clon pierde el historial de esquema. Revisar/versionar migraciones compatibles; no recrearlas automáticamente sobre la base recibida | Comprobado; sin corrección |
| OBS-002 Alta | `git ls-files` incluye `db.sqlite3` y archivos de `media/` | Riesgo de distribuir datos personales. Contenido/sensibilidad no inspeccionados; definir datos ficticios, respaldos y retiro del seguimiento/historial si procede | Versionado comprobado; contenido desconocido |
| OBS-003 Alta | Cuatro `tests.py` vacíos. Runner aislado: 0 tests | Sin evidencia automatizada de reglas/permisos/importaciones/estados. Preparar entorno ficticio y regresiones del alcance autorizado | Ejecución comprobada |
| OBS-004 Alta | Lista de usuarios usa solo login; crear/activar/desactivar admite MANAGER. `ProfileCreateForm` excluye cargo por `pk=1` | Lista global para autenticados y control de cargo dependiente del ID. Confirmar quién administra cuentas/roles; probar acceso directo y asignación | Código comprobado; política pendiente |
| OBS-005 Alta | Cursos filtran por creador; casos/códigos/pacientes/resultados no. Toggle de código busca solo por PK | Cargos docentes operan catálogos de otros autores. Puede ser biblioteca compartida, pero no hay decisión confirmada | Código comprobado; regla pendiente |
| OBS-006 Alta | Mixin docente admite superusuario; helper de fichas exige perfil/cargo y solo ADMIN ve todas. PDF es función sin mixin/decorador login/rol; estudiante exige perfil incluso a superusuario | Acceso inconsistente entre pantallas y exportación. Definir matriz y probar anónimo, inactivo, sin perfil, roles y superusuario. No se afirmó exposición pública | Código comprobado; solicitudes no probadas |
| OBS-007 Alta | `FichaEditorView.post` acepta cualquier diccionario; sección solo se valida en GET; finalizar no valida campos requeridos | POST directo puede guardar claves/tipos no previstos o enviar ficha incompleta. Definir esquema, límites, secciones y completitud | Código comprobado; reproducción pendiente |
| OBS-008 Alta | Ficha/rúbrica hacen lectura-modificación-save sin bloqueo de fila o versión | Riesgo de perder actualizaciones y competir entre guardado/envío/evaluación. Definir concurrencia y regresión | Riesgo estático; no probado |
| OBS-009 Alta | Rúbrica convierte puntajes inválidos a 0. Editar CALIFICADA y guardar borrador cambia puntaje/porcentaje/feedback sin retirar estado/nota; publicar incompleta también guarda cambios parciales | Nota publicada puede desalinearse de rúbrica/porcentaje. Definir borrador separado, validación estricta y publicación consistente | Código comprobado; reproducción pendiente |
| OBS-010 Alta | `clean_archivos` de casos/pacientes comprueba tamaño, no extensión; vistas crean multimedia con objects.create; extensión solo en validador del modelo | save/create no ejecuta full_clean automáticamente; accept del navegador no protege servidor. Añadir validación efectiva de formato/contenido | Ruta estática comprobada; upload no probado |
| OBS-011 Alta | Importación entrega contraseñas temporales en HTML/JSON; exportación confía en JSON del POST y usa hoja.append | No se encontró cambio obligatorio de contraseña ni validación de veracidad/pertenencia del JSON exportado. Riesgo de fórmulas Excel en entradas manipuladas. Definir entrega/caducidad y neutralización | Código comprobado; no generado |
| OBS-012 Media | Ingreso ofrece códigos/docentes activos globalmente sin relación docente/código/curso; borrador permite reasignar docente | Selección fuera del curso si se esperaba aislamiento. Definir política académica antes de restringir | Código comprobado; decisión pendiente |
| OBS-013 Media | ResultadoDiagnostico tiene INICIO/OCULTO/HABILITACION; no se encontró consumo de resultados en ficha ni ruta específica de habilitación | Disponibilidad declarada no integrada al flujo estudiantil examinado. Definir alcance, relación caso/paciente y permisos | Búsqueda estática; flujo pendiente |
| OBS-014 Media | Middleware actualiza actividad mediante Profile.save, que procesa imagen existente; EstudianteMixin también actualiza actividad | Disco/consultas repetidos por navegación; errores si imagen/ruta falla. Separar timestamp de tratamiento de imagen | Código comprobado; desempeño no medido |
| OBS-015 Media | Importación captura InvalidFileException al abrir; XLSX corrupto puede lanzar otras excepciones. Email o username elige cuenta sin exigir ambos coincidentes; perfil se crea antes de rechazar algunas filas | Probar corruptos, identidad discordante y efectos parciales de filas rechazadas. Registro manual usuario/perfil tampoco es transacción conjunta | Riesgos estáticos; reproducción pendiente |
| OBS-016 Media | Tailwind content activa HTML; clases de formularios viven en Python; npm build elimina salida antes de recompilar | Verificar CSS requerido y build reproducible; no compilar durante DOCUMENTAR | Config comprobada; build pendiente |
| OBS-017 Media | Portada CliniTENS: 4 enlaces #; FarmaTEF: accesos #. En vivo sin polling/refresh/WebSocket identificado | Pantallas anunciadas no equivalen a módulos listos; seguimiento requiere nueva petición/recarga. Definir presentación y alcance futuro | Plantillas/rutas comprobadas; navegador pendiente |
| OBS-018 Media | Logout por GET activo, correo consola, verificación none, sesión 1800 s. Alpine 3.x/DOMPurify por CDN; caso renderiza contenido con safe | Confirmar logout/correo/dependencias antes de publicar. Revisar sanitización servidor y acceso a medios; cargar DOMPurify no asegura sanitización del caso | Config/código comprobados; despliegue desconocido |
| OBS-019 Baja | Lista de usuarios consulta EmailAddress por usuario; actividad incluye procesamiento adicional | Posibles consultas N+1; medir con volumen ficticio antes de optimizar | Código comprobado; no medido |
| OBS-020 Baja | Código anota total_estudiantes=Count('id'), no fichas_estudiantes; plantilla no utiliza anotación | Métrica mal nombrada y sin uso visible. Aclarar/eliminar si se autoriza mantenimiento | Código comprobado |
| OBS-021 Baja | LANGUAGE_CODE es-us; textos mezclan inglés/español. utils.upload_to_s3 solo imprime | Revisar localización; no documentar S3 como almacenamiento implementado | Inspección estática |
| OBS-022 Media | Kit original refería a CONTEXTO_TECNICO_EJEMPLO ausente, Tailwind 4 y settings inexistentes | Referencias sustituidas por estructura y comandos reales | Resuelto documentalmente |
| OBS-023 Alta | `static/js/mensajes.js` inserta text con innerHTML. `templates/components/mensajes.html` usa escapejs, que protege la cadena JS, pero no la posterior interpretación HTML. Mensajes de curso/código incluyen valores editables en views.py | Riesgo de inyección HTML/XSS en notificaciones. Usar nodos de texto o sanitización explícita y probar con datos ficticios. DOMPurify se usa en modal.js, pero no en este flujo de toast | Ruta estática comprobada; explotación no probada |

## Trabajo recibido y límites

Antes de editar: `CliniTENS.rar` eliminado; Markdown de raíz, docs, prompts y specs sin seguimiento. Se preservó esa eliminación. No se modificó implementación, configuración, dependencias, base ni medios. Las observaciones no se cierran con check o sintaxis; resultados en [VERIFICACION.md](VERIFICACION.md).

## Próximo paso

Revisar prioridades y políticas de permisos/publicación con el responsable. Crear specs de corrección con casos reproducibles y aceptación antes de autorizar código.

## Revisión visual posterior — spec 003

El rediseño solicitado unifica inicio, docente, estudiante, cuentas y acceso. Durante la revisión se corrigieron navegaciones divergentes, labels/errores poco accesibles, scroll horizontal del documento en móvil y caracteres dañados en el selector de actividades. Hallazgos, efectos, correcciones y evidencia están en la [auditoría de 003](../specs/003-redisenio-integral/validation.md); la [guía visual](PERSONALIZACION_VISUAL.md) fija la estructura para nuevos módulos.

Los estados de OBS-001 a OBS-023 y las políticas confirmadas de 002 se conservan. En aquel cierre, OBS-024 seguía pendiente porque 003 no actualizó dependencias; se resuelve posteriormente en 004 para el lock del tema. El cierre técnico del rediseño no sustituye aceptación visual/pedagógica ni preparación operativa.
