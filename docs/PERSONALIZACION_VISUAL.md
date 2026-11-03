# Personalización visual — CliniTENS

2026-10-08. Identidad de [spec 003](../specs/003-redisenio-integral/spec.md), actualizada técnicamente en [004](../specs/004-actualizacion-dependencias/spec.md) a **Tailwind 4.3.3**. El rediseño conserva los contratos de la spec 002. La fuente usa @import y @source explícitos; config JS cargado por @config mantiene colores/plugins.

## Identidad y fuentes

Un espacio de aprendizaje clínico: navegación petróleo, superficie clara, acciones verde clínico, marca de ficha y contenido alineado a izquierda. La portada presenta observar, registrar y evaluar; el catálogo y la ficha usan la misma estructura. Las métricas provienen del servidor y las funciones futuras se identifican como pendientes.

La fuente de identidad es [tokens.css](../static/css/tokens.css): valores RGB separados por espacios, consumidos como `rgb(var(--color-primary))`. Los títulos usan Trebuchet MS y el cuerpo Segoe UI, con alternativas locales. No hay fuentes o fotografías remotas.

| Token | Valor | Uso |
|---|---|---|
| color-canvas | #F2F6F6 | Fondo de trabajo |
| color-surface | #FFFFFF | Formularios y datos |
| color-ink | #19363C | Texto principal |
| color-muted | #566B71 | Instrucciones y texto secundario |
| color-navigation | #17474E | Barra lateral y acceso |
| color-primary | #00796F | Acción principal y selección |
| color-primary-hover | #006058 | Acción al pasar el puntero |
| color-primary-soft | #E6F4F0 | Fondo de apoyo |

Conservar colores semánticos de error, advertencia y éxito acompañados de texto; no recolorear una escala de riesgo solo por estética. Las tonalidades auxiliares `brand-100` a `brand-950` están en [tailwind.config.js](../theme/static_src/tailwind.config.js); revisar esa escala al cambiar la identidad. Radio, fuentes y ancho de barra lateral se definen en tokens.

## Archivos y componentes

| Archivo | Responsabilidad |
|---|---|
| templates/components/Layout/base.html | Recursos, idioma, viewport, favicon y scripts comunes |
| templates/components/Layout/app_shell.html | Marca, navegación, encabezado, perfil, contenido y mensajes |
| base_extendido.html / base_pages.html | Compatibilidad de páginas y formularios existentes |
| pages/clinitens/docente/base_docente.html | Navegación docente; bloque docente_content |
| pages/clinitens/ficha/base_estudiante.html | Contexto estudiantil; bloque ficha_content |
| account/Layout/base_simple.html | Acceso y recuperación sin sesión |
| account/Layout/base_account.html | Gestión de acceso dentro del espacio común |
| templates/components/design/ | Marca, iconos, enlaces activos, campos y errores generales |
| theme/static_src/src/styles.css | Componentes, adaptación, controles y movimiento reducido |
| static/css/styles.css / mensajes.css | Compatibilidad existente y avisos acotados |
| static/js/design-system.js | Menús nativos/Escape, asociaciones de campos y tablas dinámicas |

Las páginas generales mantienen `content_main`; formularios `content_pages`; docente `docente_content`; ficha `ficha_content`. Definir `page_title` para el único H1 del encabezado y H2/H3 para subsecciones. Mantener `head_title` descriptivo. La revisión de ficha conserva su base dinámica.

Usar `btn-primary`, `btn-secondary`, `btn-danger`, `form-sheet`, `ui-field`, `error-summary`, `field-errors`, `metric-strip`, `evaluation-summary` y `section-navigation` cuando correspondan. Un formulario puede incluir `components/design/field.html` con un BoundField y `form_errors.html` para errores generales. No agregar un contenedor decorativo por cada dato.

## Contratos de interacción

Conservar URLs, `name`, `method`, CSRF, archivos multipart, campos ocultos, versiones, filtros y paginación. No cambiar consultas ni validaciones para resolver una diferencia visual. Usar `request.user` al comprobar navegación dentro de listas de usuarios. La autorización real permanece en servidor.

Asociar labels con controles en el HTML. El script común completa asociaciones de campos clínicos dinámicos y errores identificados; no reemplaza validación. En tablas usar `th scope="col"` y un contenedor desplazable con nombre y `tabindex="0"`. Añadir texto accesible a botones de icono y estados seleccionados.

El menú usa `details/summary`: abierto en escritorio desde 1024 px, compacto por debajo, Escape cierra y devuelve el foco al control. El perfil usa el mismo patrón; desactivar cuenta mantiene confirmación mediante `dialog` nativo. No añadir roles de menú sin implementar todo su patrón.

La ficha mantiene sus 13 secciones, guardado explícito, envío completo/No aplica y bloqueo por estado. La rúbrica distingue puntaje calculado, borrador y publicación. CKEditor usa la traducción española ya instalada. No incorporar dependencias para efectos visuales.

## Construcción y comprobación

Editar la fuente CSS y ejecutar `npm.cmd run build` en `theme/static_src/`, con npm ci previo cuando cambie el lock. El resultado es `theme/static/css/dist/styles.css`; no editar ese archivo a mano. Los tokens se sirven por separado y también deben estar disponibles en los estáticos. CLI separado @tailwindcss/cli; fuentes HTML/Python/JS explícitas, excluyendo entornos/datos. El build comprueba utilidades y conserva el CSS anterior si falla o no puede leer las fuentes. OBS-024 quedó resuelta en lock del tema; [inventario](INVENTARIO_DEPENDENCIAS.md) distingue el aviso del editor incorporado.

Tailwind 4 requiere Chrome 111+, Safari 16.4+ o Firefox 128+. En clases de nuevas páginas usar shrink-0, colores con opacidad mediante slash y outline-hidden cuando corresponda a la compatibilidad anterior; no recuperar las utilidades eliminadas de v3. El SVG del perfil mantiene giro de 180°/180 ms y respeta movimiento reducido.

Verificar 1280–1440 px, 768 px y 390 px: formularios fluidos, navegación operable y desplazamiento limitado a tablas/secciones, sin scroll horizontal del documento. Revisar teclado, Escape, foco, errores con valores preservados y contraste después de cualquier cambio de paleta. Respetar `prefers-reduced-motion` y el zoom del navegador.

Usar `core.test_settings` y fixtures aisladas según [entorno](ENTORNO_Y_VERIFICACION.md); no cargar `.env`, la base ni medios recibidos. Registrar evidencia y límites en la validación de la spec pertinente. La evidencia de 003 está en [validation.md](../specs/003-redisenio-integral/validation.md).

## Compatibilidad y recuperación

003 no añade modelos, migraciones, endpoints ni paquetes. Para revertir, revisar y restaurar únicamente los cambios de presentación de 003 respecto a f6e60fc y recompilar; conservar cambios posteriores y las correcciones funcionales de 002. No requiere restaurar SQLite/media. Un despliegue futuro requiere autorización y su proceso de estáticos habitual.
