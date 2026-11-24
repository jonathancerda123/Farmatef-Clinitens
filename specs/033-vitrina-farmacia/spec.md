# 033 — Vitrina estudiantil de farmacia

Actualización 2026-11-24: experiencia reemplazada por [036 — Sala de farmacia](../036-sala-farmacia/spec.md), autorizada por la usuaria. Este documento conserva el alcance y la evidencia históricos de 033. Sus gráficos/vista ya no son la experiencia vigente; la URL anterior redirige a la sala.

Fecha: 2026-11-19. Estado: implementada localmente y verificada con datos ficticios; implementación autorizada por la usuaria («ya puedes añadirlo al proyecto») después de revisar la maqueta. Aceptación de la integración: pendiente. Evidencia y límites en [validation.md](validation.md).

## Problema, actores y resultado

El alumno debe poder consultar una representación del inventario después de dispensar y como módulo opcional. La maqueta aprobada presenta cuatro muebles (35 espacios cada uno: dos columnas móviles y tres fijas, siete niveles), dos muebles por vista, cajas rectangulares, orden alfabético y agotados oscuros con X. Se reduce la carga visual: cantidades exactas y ubicación se consultan al seleccionar.

## Alcance y exclusiones

Vista GET en FarmaTEF, entrada desde recetas, portada y navegación estudiantil; enlace contextual después de una dispensación registrada. Usa los medicamentos activos del inventario registrado; no incrusta el PDF ni cantidades de demostración. Reutiliza el layout, fondo, tipografía, botones y acento jade existentes. Sin modelos, migraciones, dependencias, reservas ni escritura de inventario; la bandeja de la maqueta se excluye porque la dispensación ya tiene un flujo transaccional.

## Permisos por acción/dato

| Acción | Anónimo | Estudiante activo | Otros cargos / inactivo | Ámbito |
|---|---|---|---|---|
| Consultar vitrina | Login | Permitido | 404, igual práctica | Matrícula actual en curso |
| Elegir inventario | Login | Solo creadores de recetas asignadas a ese curso | Denegado | Filtro en servidor; curso/docente ajeno devuelve 404 |
| Alterar stock desde vitrina | Denegado | Denegado (405 POST) | Denegado | Solo consulta |

El selector separa inventarios por creador, conforme a `lotes_de_practica`. Ser colaborador del curso no publica su catálogo si no creó recetas allí. No se expone clave de receta, historial ajeno, credenciales ni metadatos personales innecesarios. Sin cursos/recetas/catálogo se muestran estados vacíos.

## Requisitos y aceptación

- RF-033-01: acceso opcional desde recetas/portada/navegación; enlace contextual desde dispensación correcta con curso y creador preseleccionados. La vista no altera stock.
- RF-033-02: solo catálogo activo del inventario seleccionado y autorizado; disponibilidad suma lotes cuyo vencimiento sea hoy o posterior. Sin lotes/vencidos: 0 y X. Recargar tras dispensar refleja el stock actualizado. Mostrar momento de consulta y botón Actualizar, sin prometer tiempo real.
- RF-033-03: cuatro muebles, dos por vista, dos móviles independientes por mueble y siete niveles; nunca se atraviesan. Fondo oculto no se selecciona con puntero ni teclado. Orden por nombre español, concentración y forma; 140 espacios repartidos sin perder registros, incluso más de 420 productos mediante selector de contenido por compartimento. El stock 0 mantiene ubicación mientras no cambie el catálogo; altas/bajas pueden redistribuirlo (sin ubicaciones persistentes).
- RF-033-04: aspecto integrado, frente/fondo distinguibles; cantidades exactas al seleccionar, sin códigos repetidos; leyenda plegable. Teclado, alternativa a arrastrar, foco visible, movimiento reducido y móvil. Sin JS: lista de consulta con nombre/presentación/stock.
- RF-033-05: JSON con campos permitidos y escape seguro; sin HTML de medicamentos interpretado. URL directa protegida; no selección de inventarios ajenos por parámetros.

## Decisiones y límites

Consulta del stock vigente actual, no reconstrucción histórica posterior a una receta. No revela respuestas esperadas. Alcance autorizado no incluye despliegue, migración de bases, commit o push. Validación docente y aceptación visual final pendientes.
