# 034 — Áreas docentes

2026-11-19. Implementación autorizada por la solicitud de clasificar docentes como Farmacia, Enfermería o Ambos y limitar los módulos visibles y accesibles. La usuaria confirmó que los docentes existentes comienzan en Ambos hasta que un administrador los clasifique.

| Requisito | Aceptación |
|---|---|
| RF-034-01 | El perfil docente dispone de Farmacia, Enfermería y Ambos. Las cuentas docentes nuevas exigen selección explícita. La migración asigna Ambos a los docentes existentes. |
| RF-034-02 | ADMIN/superusuario crean y cambian la categoría desde gestión de cuentas. El docente ve su categoría y no puede modificarla desde su perfil ni mediante POST manipulado. Se protegen las cuentas superusuario por atributo. |
| RF-034-03 | Farmacia muestra FarmaTEF y oculta CliniTENS. Enfermería muestra CliniTENS y oculta FarmaTEF. Ambos muestra las dos áreas. Menú e inicio usan la misma política. |
| RF-034-04 | El servidor deniega GET/POST, rutas de detalle, PDF y medios clínicos fuera del área docente. La categoría nueva se aplica en la siguiente petición sin depender de la navegación previa. |
| RF-034-05 | Cursos, matrículas e importación siguen siendo gestión compartida, con propiedad existente. La colaboración de recetas solo admite docentes con Farmacia o Ambos. El área no concede propiedad ni matrícula, ni reasigna registros históricos. |

ADMIN y superusuario activos conservan acceso global. Estudiantes conservan los permisos actuales de matrícula y propiedad. Cuentas inactivas o sin perfil no obtienen autorización docente. Un docente sin categoría válida no accede a módulos de área.

La gestión compartida de cursos reside actualmente bajo `clinitensdocente`; se permite a Farmacia para preparar sus prácticas sin habilitar casos, pacientes, fichas ni resultados clínicos. No se introduce clasificación de estudiantes o cursos en esta spec.

Implementado y verificado con datos ficticios. La usuaria autorizó después respaldar y aplicar únicamente la migración local; `UsuarioApp.0004` aplicada el 2026-11-19 con respaldo íntegro e integridad comprobada. Aceptación funcional final de la usuaria/docente pendiente.
