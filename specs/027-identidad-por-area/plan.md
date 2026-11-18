# Plan — 027

El estado inicial de Git contiene `docs/diagramas/` y `work/` sin seguimiento. La paleta única actual está en `static/css/tokens.css`, con consumidores de marca directos en Tailwind y CSS de simuladores.

| Requisito | Archivos y trabajo |
|---|---|
| RF-027-01 | Tokens base, estilos de navegación y marca. Mantener tipografía local y distribución actual. |
| RF-027-02 | Añadir `data-area` en el body según namespace o nombre de ruta resuelta. Usar el mismo atributo en las tarjetas del inicio. Definir tokens por área y conectar toda la escala brand a esos tokens. Integrar colores de DAU y Laboratorio. |
| RF-027-03 | Conservar estilos semánticos de riesgo y éxito al conectar los consumidores de identidad. |
| RNF-027-01 | Compilar CSS, comprobar contraste y rutas autorizadas/denegadas y revisar pantallas ficticias en Chrome. |

La selección de color se realiza en la plantilla base con la ruta resuelta, incluidos accesos directos y formularios con errores. No se persiste en sesión. La navegación usa azul profundo en ambas áreas. Las superficies blancas y el contenido alineado a izquierda permiten que el color identifique las acciones.

Recuperación mediante reversión de los archivos de esta spec y recompilación del CSS. Sin migraciones ni dependencias nuevas.
