# Plan — 002

Implementación autorizada 2026-10-08. [Spec](spec.md).

1. Settings de pruebas independientes, sin importar settings normal ni leer .env; test_settings ficticio con DB en memoria/medios temporales. Tests de regresión antes de cambios pertinentes.
2. core/permissions y mixins centralizan cargos/propiedad. UsuarioApp/admin/forms/views protegen cuentas administrativas y superusuarios. Gestionar perfil ausente sin error 500.
3. Catálogos/cursos filtran querysets y opciones de FK. Código admite curso opcional; ingreso valida matrícula y autor docente. PDF/medios usan mismas reglas en servidor.
4. Validación declarativa de ficha según data-campo real del editor; límite de JSON/tipos/campos, No aplica por sección, optimistic concurrency con versión y UPDATE condicional para SQLite; evaluar envío y rúbrica en transacción.
5. Campos separados de borrador/publicación de rúbrica. Validar enteros y claves exactas; publicar todo o nada; guardar borrador deja publicación vigente.
6. Validar extensiones, tamaño y firma/contenido de archivos. Sanitizar HTML con parser y allowlist; proteger descargas, publicación diagnóstica y endpoint docente de habilitación.
7. Importación tolera XLSX inválido, verifica identidad coincidente, límites/duplicados y atomicidad por fila. Download de credenciales mediante token aleatorio server-side en caché, ligado a usuario/curso/sesión, un uso/10 minutos; password inicial obliga cambio. Nunca aceptar passwords por POST; neutralizar fórmulas Excel.
8. Actividad UPDATE directo; anotaciones Exists/Count; seguimiento con recarga cada 30 segundos, pausa con pestaña oculta/foco en formulario. Portadas deshabilitadas etiquetadas En desarrollo.
9. Tailwind scan Python/JS/HTML acotado, build a temporal seguido de reemplazo; idioma es-cl, quitar stub S3. Notificaciones textContent.
10. Migraciones disponibles en Git; .gitignore base/media/.env; retiro del índice conservando archivos físicos. Sin commit, push ni historia purgada.

## Validación y recuperación

Suite con core.test_settings, check, makemigrations dry-run, build CSS, navegador sobre servidor y DB temporales, PDF/Excel ficticios renderizados/inspeccionados. Datos recibidos intactos. Migraciones nuevas no se aplican localmente sobre db.sqlite3. Antes de aplicar en otro entorno: respaldo de DB/media, revisión de usuarios/cursos afectados, migrate, checks y smoke tests. Revertir código y migraciones aditivas solo tras respaldo; no eliminar historial de evaluación/publicación ni datos sin revisión.

Hosting/SMTP y purga histórica de datos siguen decisiones operativas: se prepara configuración y se documentan los pasos, sin inventar despliegue. Ausencia de servidor externo no impide corregir código local.
