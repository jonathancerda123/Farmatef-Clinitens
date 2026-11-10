# 022 — Inicio por áreas y selector de medicamentos con búsqueda

2026-11-10. Usuario autoriza trabajo en jonathan, dos accesos grandes al iniciar sesión y búsqueda en selectores de medicamentos. Confirmó «Buscador dentro del selector». Preservar cambios pendientes 021 y bases privadas; no commit/push ni cambio de permisos.

RF-022-01: inicio presenta primero FarmaTEF y CliniTENS con igual tamaño y una sola acción principal por área, usando la identidad turquesa actual. Actividad reciente permanece debajo. Estudiante va a práctica de farmacia; docente/ADMIN a gestión existente.
RF-022-02: selectores de medicamentos en lotes, recetas y etiquetado permiten filtrar dentro del control por nombre, principio activo, concentración y forma, sin distinguir acentos/mayúsculas. Lista acotada visualmente con número de coincidencias.
RF-022-03: mantener select/ID/name/opciones autorizadas y validación servidor; elección dispara change existente, cambio limpia lote incompatible y vista previa; texto libre no equivale a elección. Sin JavaScript queda select nativo.
RF-022-04: filas nuevas de recetas, reinicio, selección tras errores, opción vacía, sin coincidencias, teclado (flechas/Enter/Escape/Tab), labels/foco y móvil. No usar HTML de datos como código.

Sin dependencias ni migraciones; no alterar stock, dispensación o permisos estudiantiles. No se inventa un selector donde el alumno solo consulta una receta asignada.
