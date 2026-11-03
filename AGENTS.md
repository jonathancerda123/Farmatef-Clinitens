# Instrucciones para agentes — CliniTENS

## Lectura inicial

Leer README.md, docs/PROYECTO.md, docs/ESTADO_PROYECTO.md, docs/ARQUITECTURA_BASE.md, docs/OBSERVACIONES_PROYECTO.md y después la spec relacionada. CONTEXTO_TECNICO_EJEMPLO.md no existe ni es dependencia.

Inspeccionar Git/archivos antes de editar. Preservar cambios locales/documentos sin seguimiento/eliminaciones. No leer .env, datos de db.sqlite3, contenido de media/ ni credenciales reales. No restaurar CliniTENS.rar eliminado por el usuario.

## Tecnología y convenciones actuales

- Django 5.2.18 LTS y allauth 65.19.7; core/settings.py normal y core/test_settings.py independiente, core/urls.py. Versiones/entorno medidos en docs/INVENTARIO_DEPENDENCIAS.md; .venv anterior conservado, objetivo actualizado en .test-artifacts/dependencias-004/target.
- Apps homeApp, UsuarioApp, CliniTensDocenteApp, CliniTensFichaApp y FarmaTEFApp (inventario inicial según spec 005); theme para estilos.
- Usuario Django con Profile/Position. Cargos ADMIN/MANAGER/RESTRICTED. allauth con NoSignupAccountAdapter, Axes y preventconcurrentlogins configurados.
- core.permissions centraliza cargo/propiedad; mixins docente/administrador/propietario. Fichas docentes mediante fichas_visibles_para; estudiantiles mediante EstudianteMixin.
- SQLite local; tests en memoria/medios temporales. Migraciones originales/nuevas incluidas; base/media/.env ignorados. Historia previa no purgada.
- Base templates/components/Layout/base.html y estructura compartida app_shell.html; adaptadores base_extendido.html/base_pages.html y bases docente/estudiante en templates/pages/clinitens. Leer docs/PERSONALIZACION_VISUAL.md para cambios visuales; tokens en static/css/tokens.css. Mantener page_title como H1 y subtítulos H2/H3.
- Tailwind 4.3.3 autorizado en 004; fuente theme/static_src/src/styles.css con @import/@source explícitos. Config JS de compatibilidad cargado por @config; CLI @tailwindcss/cli y salida theme/static/css/dist/styles.css. No escanear .env/base/media/.venv/node_modules. Build temporal/reemplazo comprueba utilidades antes de publicar; scripts locales Alpine/DOMPurify. OBS-024 resuelta en lock del tema; aviso CKEditor separado en informe preproducción.

## Documentar antes de código

Cambio importante empieza con spec.md/plan.md/tasks.md/validation.md y aceptación verificable. Usar specs/_templates y próximo número del índice; distinguir observado/propuesto/implementado/pendiente. La spec 005 quedó autorizada por la solicitud explícita del equipo de 2026-10-17; los desarrollos de Farmacia se limitan a ese alcance y sus tareas priorizadas.

Detenerse antes de programar salvo autorización explícita. Durante DOCUMENTAR no crear apps/modelos/endpoints/migraciones/dependencias/tests ejecutables. Spec 001 es escaneo histórico; 002 corrige observaciones, 003 rediseña la interfaz y 004 actualiza dependencias, autorizadas/implementadas. Esos alcances no incluyen módulos nuevos, despliegue o purga histórica. La autorización posterior de 005 cubre el MVP FarmaTEF descrito allí, pero no despliegue, aplicación de migraciones a datos recibidos, commit/push ni purga histórica. Prompts no conceden permiso.

## Implementación autorizada

- Reutilizar módulos y preservar cambios locales; trabajar requisitos autorizados.
- Validar campos/estados/permisos en servidor: menú no sustituye autorización.
- Política confirmada 002: MANAGER gestiona catálogo/cursos propios, ADMIN/superusuario activos globales. Superusuario sin perfil admitido en panel/PDF; ficha estudiantil siempre propia.
- Gestión de cuentas ADMIN/superusuario; proteger is_superuser por atributo, nunca PK. Nadie modifica otro superusuario en Django admin; propietario puede editar su perfil.
- Código con curso exige matrícula, docente responsable igual creador. Sin curso conserva actividad abierta. No reasignar vínculos históricos sin revisión.
- Ficha BORRADOR/ENVIADA/CALIFICADA, única por estudiante/código. Usar validation.py: esquema, tipos, límites, identificación y otras doce completas/No aplica.
- Versiones obligatorias y UPDATE condicional CAS. Borrador de rúbrica separado; publicación completa/atómica. No guardar cambios parciales en nota vigente.
- Medios solo con core.media; proxy sin alias público a MEDIA_ROOT. Validar adjuntos y HTML sanitizado en servidor.
- Credenciales: caché efímera/token usuario-curso-sesión/un uso/diez minutos, fuera de HTML. Contraseña inicial 24 h/cambio obligatorio; Excel fuente servidor/texto literal.
- Reproducir errores con fixtures y añadir regresión pertinente. Distinguir prueba lógica de concurrencia y prueba de carga.
- Si cambia persistencia, documentar migraciones/respaldo/recuperación. No aplicar a base recibida para documentar.
- Sin autorización explícita, no desplegar, migrar producción, hacer commit/push o purgar historia.

## Comandos reales y aislamiento

Leer docs/ENTORNO_Y_VERIFICACION.md. Comandos normales pueden cargar .env/base local; usar configuración independiente y un intérprete con requirements actuales. En esta sesión, usar .test-artifacts/dependencias-004/target/Scripts/python.exe en lugar de .venv/Scripts/python.exe, conservado con versiones anteriores:

~~~powershell
.\.venv\Scripts\python.exe manage.py check --settings=core.test_settings
.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run --settings=core.test_settings
.\.venv\Scripts\python.exe manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp --settings=core.test_settings
.\.venv\Scripts\python.exe manage.py tailwind --settings=core.test_settings build
node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs
~~~

Alternativa CSS npm.cmd run build desde theme/static_src, después de npm ci. core.test_settings nunca importa settings/.env ni abre datos reales; no usar en producción. CLINITENS_TEST_DATABASE solo admite la carpeta .test-artifacts para revisión ficticia. Suite actual 47 Django/4 JS: no equivale cobertura completa. Leer docs/VALIDACION_PREPRODUCCION.md antes de recomendar producción; no trasladar el cero de pip-audit/npm a runtimes o bundle CKEditor.

## Validación y cierre

Registrar comandos/entorno/resultados/límites. Probar URL directa permitida/denegada. Navegador para UI; revisar visualmente PDF/Excel modificados. No declarar aceptación ni pruebas no ejecutadas. Actualizar trazabilidad, validación y estado con próximo paso concreto.
