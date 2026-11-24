# Plan — 034

Base inspeccionada en `valentina`. Preservar el trabajo local de vitrina 033, los diagramas y `work/`. El cargo actual está en `Position`, el perfil en `Profile`, las autorizaciones comunes en `core.permissions` y los cursos sirven a ambas áreas.

| RF | Integración |
|---|---|
| 01 | Campo `Profile.area_docente`, choices y restricción de valores. Migración aditiva y actualización de MANAGER existentes a Ambos. |
| 02 | Formulario de creación, formulario de área para administración, ruta protegida de edición y presentación en listado/perfil. El formulario personal conserva sus campos permitidos. |
| 03/04 | Helpers centrales, middleware por ruta resuelta y context processor para inicio/navegación. Protección adicional de medios clínicos y consultas de recetas/fichas. |
| 05 | Lista explícita de rutas de cursos compartidos. Colaboradores FarmaTEF filtrados por área. Se conservan vínculos históricos y propiedad. |

La restricción de área complementa los mixins existentes. El middleware revisa la categoría en cada petición antes de invocar la vista, incluso funciones PDF y rutas POST. El contexto de plantillas usa la misma política y el formulario administrativo actualiza solo el campo de área.

Validar matriz de categorías/perfiles, accesos directos, denegación de escrituras, cambio de categoría en sesión, cuenta propia, superusuarios y migración de datos anteriores. Probar navegación y formularios con datos ficticios. Usar `core.test_settings` y el intérprete verificado con dependencias actuales.

Recuperación: respaldar SQLite antes de aplicar la migración habitual. La migración añade una columna y asigna categoría a MANAGER existentes. Revertir elimina la clasificación, por lo que se debe exportar o respaldar antes. Restaurar código y base de forma coordinada. No aplicar ni revertir sobre datos recibidos durante la verificación aislada.

Ejecución local autorizada después de las verificaciones: respaldo consistente e íntegro en `.test-artifacts/areas034`, plan limitado a UsuarioApp.0004, migración aplicada y confirmada con showmigrations/check. Véase validation.md y el registro de recuperación en docs/ENTORNO_Y_VERIFICACION.md.
