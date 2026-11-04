# Tareas — 012 / docentes colaboradores FarmaTEF

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Autorización: «sí», 2026-11-04. Migración local aplicada con respaldo; sin commit ni push.

- [x] T-012-01 — Añadir la relación curso-colaboradores y formulario de gestión owner/admin.
  - RF: 012-01/02/08. Hecho cuando solo MANAGER activos se asignan y la migración es aditiva.
- [x] T-012-02 — Aplicar alcance de cursos compartidos a las consultas y operaciones de recetas FarmaTEF.
  - RF: 012-03/04/05. Hecho cuando solo owner, colaboradores activos y ADMIN ven/gestionan recetas de curso.
- [x] T-012-03 — Conservar aislamiento de datos ajenos y actualizar documentación.
  - RF: 012-06/07. Hecho cuando colaboración no habilita acceso a roster/fichas/resultados ni catálogo/lotes ajenos.
- [x] T-012-04 — Generar/revisar migración y checks básicos; registrar límites.
  - RF: 012-08. Hecho cuando la migración aditiva se aplica solo a la base local tras respaldo, no a producción, y la validación refleja lo realmente ejecutado.
