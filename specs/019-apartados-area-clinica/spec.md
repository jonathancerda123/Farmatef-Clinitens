# 019 — Apartados del área clínica sin duplicar módulos

Fecha: 2026-11-09. Fuente: petición explícita de implementar los apartados de diez capturas, reutilizando lo existente y conservando el estilo actual. Implementación de navegación autorizada por esa petición; aceptación humana pendiente. Rama inspeccionada: `jonathan`, upstream `origin/jonathan`, árbol inicialmente limpio en `df23932`. No se autoriza commit/push ni migración de datos.

## Observado y resultado solicitado

Ya existen ficha clínica electrónica (`CliniTensFichaApp`), DAU, laboratorio y CAD (`CliniTensSimulacionApp`), panel docente (`CliniTensDocenteApp`) y administración de cuentas (`UsuarioApp`). Las capturas son referencia de apartados y orden, no instrucciones para sustituir autenticación o permisos.

La portada actual separa herramientas en dos grupos, omite RAE y no ofrece un acceso de administrador equivalente al existente en la navegación. No se encontró un registro RAE independiente. El Kardex legado contiene eventos, pero no equivale automáticamente al RAE solicitado.

## Alcance y decisiones pendientes

Reorganizar la portada en este orden: Ficha Clínica Electrónica; Registro de Atención de Urgencia; Registro de Atención de Enfermería; Laboratorio Clínico; Centro de Apoyo Diagnóstico; Perfil Docente; Perfil Administrador. Reutilizar destinos, sesión, permisos y cursos. Mantener layout, tokens y componentes actuales.

RAE: el usuario confirmó «Sí, hagamos esa primera versión» a la propuesta de paciente simulado, cuidados realizados, observaciones, borrador, finalización e historial. Es una propuesta propia autorizada, no una reconstrucción comprobada del interior de la referencia. Se conserva el acceso actual y se explicó al usuario en lenguaje simple; no se sustituye autenticación por nombre/RUT libre.

No se crean accesos paralelos ni dependencias. Se añade un modelo RAE independiente en la app de simulación, sin reutilizar registros DAU/Kardex como registros de enfermería. No se consultan `.env`, base habitual, medios ni credenciales. No se copian identificadores personales de las capturas.

## Permisos y aceptación

| Apartado | Estudiante activo RESTRICTED | MANAGER | ADMIN/superusuario activo |
|---|---|---|---|
| Ficha | Ingreso existente con código/matrícula cuando corresponde | Ingreso existente para demostración | Ingreso existente para demostración |
| DAU, laboratorio, CAD | Práctica existente con matrícula/publicación | Preparación docente existente | Preparación docente existente |
| RAE | Registro e historial propios de casos publicados de cursos matriculados | Preparación del paciente de cursos visibles | Preparación del paciente de cursos visibles |
| Perfil Docente | Informativo, sin acceso | Panel existente | Panel existente |
| Perfil Administrador | Informativo, sin acceso | Informativo, sin acceso | Gestión de usuarios existente |

Anónimo redirigido al login en portada; usuario sin cargo no recibe enlaces a práctica/gestión; superusuario activo sin perfil usa funciones docentes/administrativas. Las vistas destino siguen comprobando autorización en servidor.

- RF-019-01: los siete apartados aparecen en el orden de las referencias, sin reconstruir capacidades existentes.
- RF-019-02: cada enlace disponible lleva a su ruta real según el cargo; las opciones restringidas explican el perfil requerido.
- RF-019-03: la portada conserva identidad visual y H1 único, funciona en escritorio/tablet/móvil y por teclado.
- RF-019-04: RAE busca pacientes SIM publicados en cursos del estudiante; abre o continúa un borrador propio. Cuidados (hasta 5000 caracteres) y observaciones (hasta 2000) se guardan como texto; finalizar exige cuidados, registra hora/autor de sesión y bloquea cambios. Historial paginado propio; otro ejercicio tras finalizar crea atención nueva. Versión obligatoria y UPDATE condicional evitan sobrescribir guardados obsoletos. Un borrador abierto como máximo por estudiante/caso.
- RF-019-05: cambios locales permanecen en `jonathan`, sin commit/push, sin tocar base habitual.
- RF-019-06: una guía explica cómo preparar pacientes/casos con los accesos docentes existentes. RAE comparte el paciente SIM y la publicación del caso; no crea un catálogo duplicado. La preparación de paciente en RAE conserva los demás bloques del caso y no permite editar casos publicados.

Casos negativos RAE: no inscrito, caso borrador, usuario ajeno, docente en práctica de estudiante, inactivo o sin cargo no pueden leer/escribir. Versión ausente/inválida, acción desconocida, texto sobre límite o finalización sin cuidados no persisten; versión obsoleta/cierre concurrente responden 409 sin sobrescribir. Se conserva contenido enviado ante error.

## Migración y recuperación RAE

Migración aditiva `0007_atencionenfermeria`, probada únicamente en base ficticia; relación protegida con caso/estudiante, campos de texto, estado/fechas y versión. No se aplica a la base habitual. Antes de usarlo en una instalación con datos, respaldar y comprobar recuperación, revisar el plan y autorizar allí la migración. Revertir código conservando la tabla aditiva es preferible a borrar atenciones; cualquier reversión de esquema requiere respaldo y revisión de los registros creados.

## Compatibilidad

Se conservan contratos POST, versiones, archivos e historial de módulos existentes. RAE incorpora sus propios POST y control de versión. Reversión de presentación: retirar solo cambios de 019 y recompilar CSS. No se modificó la base habitual; la reversión de una futura instalación debe conservar registros RAE y respaldo compatible.
