# 028 — Inventario y prácticas APS en la demo 8025

Fecha: 2026-11-18. Carga de datos ficticios autorizada por el usuario. Destino: `.test-artifacts/farmacia-025-fixture.sqlite3`, continuación de 027.

- RF-028-01: Completar los 359 medicamentos añadidos en 027 con mínimos positivos y lotes marcados como simulados. El stock registrado suma todos los lotes. El stock disponible excluye los vencidos. El estado muestra las alertas calculadas por FarmaTEF. Se conservan los siete lotes y cinco mínimos históricos.
- RF-028-02: Asignar cinco recetas nuevas con medicamentos recién cargados a los cursos existentes. Incluir dispensación válida, comparación de presentaciones, receta vencida, información incompleta y falta de stock vigente. Dejar los casos nuevos sin intentos en la demo.
- RF-028-03: Publicar cinco escenarios integrados en el curso clínico para DAU, RAE, Laboratorio, Apoyo Diagnóstico y Ficha Clínica Electrónica. Cada escenario incluye identidad SIM, motivo, antecedentes, solicitud y resultado ficticios. Incluir ejemplos de historial con registros de prueba. El panel docente usa los cursos, actividades y fichas existentes. El perfil administrador conserva las cuentas de la demo.

## Aceptación verificable

- Los 364 productos quedan con mínimo positivo y lotes. Se observan stock bajo, vencimiento próximo, lotes vencidos y productos sin alertas.
- Los dos cursos tienen recetas nuevas. Una dispensación de prueba descuenta solo los lotes seleccionados y los tres rechazos de prueba conservan stock.
- El alumno inscrito abre los cinco casos de cada recorrido. Un alumno ajeno recibe denegación. Los ejemplos aparecen en sus historiales, y el docente puede revisar una ficha enviada.
- El catálogo, las recetas y los casos históricos conservan sus datos. Se respalda y ensaya la carga antes de confirmar en la demo. Sin cambios de esquema ni aplicación a la base habitual.
