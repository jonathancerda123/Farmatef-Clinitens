# Validación — 002

2026-10-08. Implementación autorizada de OBS-001 a OBS-023, con las dos reglas confirmadas por el usuario. Referencia inicial main/4126cc7; documentos locales y eliminación previa del RAR preservados. [Spec](spec.md), [tareas](tasks.md) y [trazabilidad](../../docs/TRAZABILIDAD.md).

## Entorno y reproducción

PowerShell, Python 3.12 de .venv, Django 5.1.2. Todos los comandos Django usaron core.test_settings: configuración independiente sin importar core.settings ni cargar .env. Suite en SQLite de memoria/media temporales; navegador en .test-artifacts/revision.sqlite3 con usuarios, casos y archivos ficticios. Las migraciones se aplicaron únicamente a ese esquema de revisión. El servidor temporal se detuvo al cierre.

Las primeras regresiones evidenciaron fallos de permisos, aceptación de JSON no previsto y publicación incompleta; se ampliaron al corregir código. No se reprodujeron todos los 23 hallazgos antes de cada cambio: algunos eran defectos estructurales/documentales. La suite final comprueba resultados y regresiones; no equivale a auditoría exhaustiva ni a cobertura porcentual.

## Ejecuciones y evidencia

| Método / comando ejecutado | Resultado | Alcance / límite |
|---|---|---|
| manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp --settings=core.test_settings --verbosity=1 | 47 tests correctos | Permisos por URL directa, propietario/ajeno/ADMIN/superusuario sin perfil; protección root; matrícula; estados/JSON/versiones; rúbrica; adjuntos/media; importación/tokens/Excel; actividad/métricas/correo actual |
| node --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs | 3 tests correctos | Texto malicioso literal, ausencia de contenedor y conservación de CSS ante fallo de compilación |
| manage.py check --settings=core.test_settings | 0 incidencias | No es check de despliegue real |
| manage.py makemigrations --check --dry-run --settings=core.test_settings | No changes detected | Modelos concuerdan con migraciones; no compara esquema recibido |
| python -m pip check | No broken requirements found | Consistencia de paquetes, no auditoría de vulnerabilidades Python |
| npm run build --prefix theme/static_src | Build correcto de Tailwind 3 y copia de JS local | Aviso Browserslist/caniuse-lite antiguo; CSS reemplazado tras éxito |
| AST Python y get_template aislados | 77 Python y 85 plantillas sin errores | Sintaxis/compilación, no prueba de todos los includes dinámicos |
| Comprobador Markdown/enlaces/fences | 36 Markdown y 130 referencias locales sin errores | Enlaces externos y presentación Markdown sin auditoría completa |
| git diff --check y git diff --cached --check | Sin errores | Avisos de normalización LF/CRLF en dos archivos |
| git ls-files db.sqlite3 media; Test-Path local; migraciones en índice | Cero base/medios seguidos, archivos físicos conservados; migraciones incluidas | Historial Git anterior aún contiene datos; sin commit/push ni purga |
| npm audit fix compatible y reporte audit | 16 avisos iniciales reducidos a 8: 5 altos/3 moderados de build | OBS-024 pendiente; solución sugerida implica cambios incompatibles con Tailwind 3 |

## Comportamiento comprobado

- RF-002-01/02: esquema ficticio desde migraciones, settings independiente, suite y retiro del índice sin borrado local.
- RF-002-03: administración de cuentas por ADMIN/superusuario, bloqueo de modificar otros superusuarios, acceso docente por autor y acceso global administrativo. Formulario e ingreso validan relaciones/matrícula; descarga PDF usa mismos permisos.
- RF-002-04/05: JSON mal formado/tipos/claves/catálogos/límites rechazados; borrador incompleto preservado; identificación y 13 secciones completas o No aplica permiten envío. Conflicto 409 no sobrescribe. Rúbrica exige 15 criterios válidos para publicar; guardar borrador conserva publicación previa.
- RF-002-06/10: sanitización HTML en servidor, uploads validados, subida directa de editor desactivada y medios privados. Publicación/habilitación del resultado determina acceso estudiantil. Logout por POST, mensajes como texto y bibliotecas JS locales.
- RF-002-07: XLSX corrupto/identidad incompatible y fallo al crear perfil no dejan cambios parciales; token vinculado a sesión/usuario/curso, un uso y caducidad. Password temporal ausente de HTML, cambio obligatorio/expiración y celdas Excel literales.
- RF-002-08/09/11: timestamp sin reprocesar avatar, lista optimizada, conteos reales, build seguro, portadas pendientes explícitas, documentación actualizada.

Navegador sobre localhost ficticio: ingreso, guardado de identificación, persistencia de No aplica, revisión docente de ficha enviada con controles bloqueados, rúbrica sin publicación incompleta y seguimiento con filtros. Logs registraron recargas de En Vivo cada 30 s. Revisión visual de escritorio y ventana estrecha; tablas mantienen desplazamiento horizontal. Último ajuste muestra No aplica también al docente en modo lectura. Evidencia local ignorada: .test-artifacts/revision-docente-final.jpg. No se afirma auditoría de accesibilidad completa.

Exportaciones generadas por la aplicación con datos ficticios: PDF de dos páginas renderizado y revisado visualmente, con encabezados unidos al contenido y booleanos Sí/No; Excel de credenciales renderizado y revisado con cabeceras/datos legibles. Se verificaron texto literal y formato. Artefactos ignorados en .test-artifacts; no contienen datos del usuario.

## Límites y cierre

No se leyeron ni modificaron datos de db.sqlite3/media recibidos o .env; no se restauró CliniTENS.rar. No se aplicaron migraciones reales, desplegó, hizo commit/push ni purgó historia. Axes está desactivado en settings ficticios; no se valida topología productiva de Axes/sesiones/proxy. Concurrencia probada por versiones obsoletas, sin carga multicliente. PDF/video se validan por firma, tamaño y extensión, sin antivirus.

Implementación local y verificación terminadas; aceptación humana/clínica pendiente. Antes de operar sobre datos recibidos: seguir respaldo, revisión de esquema y vínculos heredados, migración autorizada y recuperación descritos en [entorno](../../docs/ENTORNO_Y_VERIFICACION.md). SMTP, HTTPS/media privado y caché compartida deben verificarse en destino. Nueva OBS-024 documentada para revisar dependencias sin imponer Tailwind 4.
