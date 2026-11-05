# 012 — Docentes colaboradores para recetas FarmaTEF

Fecha: 2026-11-04. Estado: implementación autorizada por «sí». Área: cursos / FarmaTEF. Código autorizado: sí; migración aditiva aplicada a la base local tras respaldo. No producción ni commit/push. Revisión humana: pendiente.

## Problema, actores y resultado

La propiedad actual de una receta pertenece al usuario que la creó. Un docente distinto del propietario del curso no puede revisar las recetas de práctica ni sus respuestas, aunque trabaje con ese curso. El responsable podrá agregar docentes colaboradores al curso para compartir la gestión de recetas FarmaTEF asignadas allí.

## Alcance y exclusiones

- ADMIN/superusuario activos gestionan colaboradores en cualquier curso. MANAGER solo administra colaboradores de cursos propios.
- Solo se pueden agregar cuentas activas con cargo MANAGER. El propietario no se agrega como colaborador; no se elevan cargos ni se crean cuentas.
- El responsable y los colaboradores activos ven recetas y respuestas de FarmaTEF asignadas a ese curso; pueden crear recetas para el curso y retirar las que no tengan actividad, sujeto a las validaciones existentes.
- Al retirar un colaborador, este pierde acceso a las recetas asignadas a ese curso, incluso si las creó. Conserva acceso a recetas propias sin curso.
- Los colaboradores no obtienen acceso a listas de estudiantes, importación, fichas clínicas, resultados ni gestión global de inventario/lotes. La selección de medicamentos mantiene el filtro actual por autor.
- La matrícula estudiantil no se altera; solo los estudiantes inscritos siguen viendo la práctica. ADMIN/superusuario mantienen acceso global conforme a la política vigente.
- Incluye una relación M2M aditiva con migración. No aplicar migraciones a la base recibida durante este cambio; documentar respaldo y reversión.

## Permisos por acción

| Acción | RESTRICTED | MANAGER responsable | MANAGER colaborador | ADMIN/superusuario activo |
|---|---|---|---|---|
| Asignar/quitar colaboradores | Denegado | Sí, en cursos propios | Denegado | Sí, global |
| Ver y gestionar recetas del curso | Denegado | Sí | Sí, solo cursos compartidos | Sí, global |
| Ver/modificar matrícula, fichas o resultados por colaboración | Denegado | Según permisos existentes | Denegado por esta colaboración | Según permisos existentes |

## Requisitos y aceptación

- RF-012-01: El detalle de curso permite buscar/seleccionar docentes MANAGER activos y agregarlos/quitarles acceso a FarmaTEF del curso.
- RF-012-02: Solo el propietario del curso o ADMIN/superusuario activo puede gestionar colaboradores; el POST valida cargo, estado y ámbito en servidor.
- RF-012-03: Los colaboradores activos ven en FarmaTEF las recetas asignadas a cursos compartidos y pueden revisar intentos de estudiantes.
- RF-012-04: Las recetas de un curso siguen visibles al propietario y a colaboradores actuales; al retirar un colaborador, sus recetas de esos cursos dejan de aparecerle.
- RF-012-05: Un colaborador puede asignar una receta nueva al curso, usando los formularios y el catálogo que le pertenecen según permisos actuales.
- RF-012-06: La colaboración no concede acceso a roster/importación, fichas, resultados ni medicamentos/lotes de otro autor.
- RF-012-07: Estudiantes, cuentas inactivas y managers ajenos no pueden ver la administración ni acceder por URL directa.
- RF-012-08: La migración solo añade la relación de colaboración; no cambia matrículas, recetas, autores ni datos existentes.

## Compatibilidad y decisiones

Los cursos conservan un responsable único `creado_por`; el M2M solo añade docentes colaboradores. Las recetas sin curso siguen bajo el autor individual. Revisión funcional de la matriz de permisos y aceptación de docentes quedan pendientes.
