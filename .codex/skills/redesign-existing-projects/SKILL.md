---
name: redesign-existing-projects
description: Auditar y mejorar la interfaz de un proyecto existente conservando su
  stack y funcionalidad. Usar al mejorar formularios, tablas, dashboards, navegación,
  móvil o jerarquía visual en Django, React u otros frameworks. Revisar primero y
  corregir solo el alcance autorizado.
---

# Rediseño de proyectos existentes

Leer [el contrato de trabajo](references/contrato.md).

## Auditar antes de cambiar

Leer los archivos de la pantalla objetivo y dependencias pertinentes, no toda la base por defecto. Identificar usuarios, tareas, datos, rutas, roles, construcción CSS y componentes reutilizables. Si hay capturas, contrastarlas con el código; si solo hay código, declarar que no se observó la interfaz renderizada.

Revisar jerarquía de títulos y acciones, tamaño de texto, ancho de lectura, alineación, ritmo, agrupación, navegación y vista móvil. Evaluar estados vacíos, errores, carga, guardado y permisos. Diferenciar fallos funcionales o de accesibilidad de preferencias estéticas.

Entregar una tabla con prioridad, ubicación, evidencia, efecto en el usuario y mejora concreta. Si la petición incluye correcciones, continuar con las autorizadas; no detenerse para confirmar cada detalle reversible.

## Mejorar por impacto

1. Corregir primero acciones ambiguas, formularios inaccesibles, errores invisibles y navegación rota.
2. Ordenar jerarquía y agrupación; alinear títulos, campos y acciones relacionados.
3. Ajustar espaciado, ancho, contraste y escala tipográfica reutilizando tokens.
4. Mejorar tablas, filtros y navegación en móvil sin perder datos.
5. Pulir estilos y microinteracciones cuando no dificulten la tarea.

## Preservar flujos Django

- Mantener nombres de campos, URLs, consultas, permisos, validación del servidor y csrf_token. No sustituir un formulario funcional por una simulación de frontend.
- Mostrar errores por campo y errores generales; conservar valores al fallar. Asociar instrucciones y errores a sus controles.
- En tablas usar caption cuando aporte contexto, th y scope. Para pantallas pequeñas permitir desplazamiento en un contenedor identificado o una representación alternativa que conserve datos y encabezados.
- Mantener paginación y filtros existentes. Si se cambia su comportamiento, tratarlo como cambio funcional dentro de una spec autorizada.
- Usar colores semánticos con texto o icono adicional. No depender solo del verde o rojo.

## Criterio visual

No reemplazar automáticamente fuentes, iconos, sidebar, tarjetas o tres columnas solo por ser comunes. Mantener identidad y consistencia. No agregar textura, imagen, doble contenedor o animación para llenar espacio. Dar prioridad a lectura y ejecución de tareas.

No inventar políticas legales, testimonios, fechas ni métricas. Si falta contenido, señalarlo como pendiente. Usar activos locales y evitar imágenes remotas aleatorias.

Comprobar las pantallas y flujos afectados; informar cambios, validaciones y limitaciones. Para un control independiente posterior utilizar web-design-guidelines.
