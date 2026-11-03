# Lista local de revisión de interfaz

Adaptación de las categorías de Vercel Web Interface Guidelines a HTML, Django y React. Versión local 2026-10-06. Fuente: https://github.com/vercel-labs/web-interface-guidelines ; no se necesita descargar reglas para usar esta lista.

## Semántica y teclado

- Usar button para acciones y a con href real para navegación. Conservar apertura en nueva pestaña y enlace directo.
- Usar controles nativos; no añadir manejadores de teclado redundantes a botones y enlaces que ya los implementan. Si un control personalizado es necesario, implementar el patrón completo de teclado y roles.
- Dar nombre accesible a botones de solo icono y controles. Preferir label visible; asociar for/id en HTML y htmlFor/id en React.
- Mantener jerarquía de títulos, landmarks y acceso al contenido principal cuando corresponda.
- Mostrar foco visible sin eliminar outline sin sustituto. Evitar que barras fijas tapen el control enfocado.
- Gestionar foco, Escape y retorno en diálogos. No encerrar al usuario en un menú o zona sin salida.
- Identificar página activa y estado seleccionado con semántica pertinente.
- Añadir alternativas de teclado y toque para drag, swipe y gestos no esenciales.

## Formularios y validación

- Mantener name, type, inputmode y autocomplete apropiados a cada campo. No desactivar autocomplete de forma global ni bloquear pegado.
- Asociar instrucciones y errores mediante aria-describedby cuando corresponda; mantener mensajes visibles.
- Mantener validación en servidor, csrf_token y comprobaciones de permisos en Django; la validación cliente es complementaria.
- Conservar valores tras errores y permitir reintentar. No borrar un formulario al fallar el envío.
- Indicar envío en curso y prevenir duplicados sin impedir corrección o dejar una acción permanentemente deshabilitada.
- Presentar errores generales y por campo. Gestionar foco en resumen o primer error sin moverlo inesperadamente mientras se escribe.
- Evitar placeholders como único label. No exigir puntos suspensivos por regla estética.
- Asociar label y área de interacción en checkboxes y radios.
- Advertir sobre pérdida de cambios cuando exista edición no guardada real, no bloquear navegación indiscriminadamente.
- No añadir beforeunload a toda pantalla; evaluar necesidad y limitaciones de plataforma.

## Contenido, contraste y datos

- Verificar contraste de texto, controles, estados y foco con herramientas cuando se afirme un cumplimiento concreto.
- No depender solo del color para éxito, error o seleccionado.
- Permitir ampliación de texto y contenido largo sin solapamientos ni pérdida de acciones.
- Reservar truncado para contenido secundario; proporcionar acceso al texto íntegro cuando sea necesario.
- Revisar estados vacío, carga, error, sin permiso y datos extremos pertinentes al flujo.
- Usar table, encabezados th/scope y caption cuando ayude a comprender datos tabulares.
- Mantener encabezados asociados en adaptación móvil. Identificar el área desplazable cuando exista y verificar su manejo por teclado.
- Usar números tabulares cuando faciliten comparaciones; no exigir monospace para todo número.
- Respetar idioma de la página y formato local. En JS usar Intl cuando corresponda; en Django conservar localización del framework.

## Imágenes y medios

- Dar alt descriptivo a imágenes con información; alt vacío a imágenes puramente decorativas.
- Reservar dimensiones o proporción para evitar desplazamientos de layout.
- Cargar diferidamente imágenes fuera de la vista inicial cuando proceda; no aplicar lazy a la imagen crítica principal.
- Priorizar medios críticos con mecanismos compatibles con la versión, sin marcar todas las imágenes high.
- Proporcionar subtítulos, transcripción o descripción para medios informativos según su contenido y uso.
- Conservar controles accesibles de medios. Evitar autoplay de audio.
- No descargar fotografías aleatorias ni presentar retratos o testimonios inventados como reales.

## Movimiento y rendimiento

- Respetar prefers-reduced-motion. Mantener el contenido utilizable si se deshabilitan animaciones o JavaScript.
- Preferir transform y opacity; listar propiedades de transición. Evitar transition: all.
- No ocultar información crítica hasta un IntersectionObserver ni requerir animación para acceder a acciones.
- Añadir mecanismos de pausa cuando movimiento automático prolongado los requiera; preferir evitar decoración persistente en pantallas operativas.
- Evitar leer y escribir layout intercaladamente en bucles. Medir antes de recomendar microoptimizaciones.
- Evaluar paginación, carga gradual o virtualización de listas largas según contenido, rendimiento, búsqueda y accesibilidad; no imponer virtualización a toda lista de más de 50 elementos.
- Usar preconnect/preload solo para recursos críticos confirmados. Mantener fuentes disponibles y fallback.

## Móvil, navegación y tema

- Revisar ancho estrecho, zoom, orientación y dispositivo de entrada sin perder controles o contenido.
- Mantener objetivos de toque usables, etiquetas y separación; medir tamaños cuando corresponda.
- No impedir zoom o gestos nativos sin razón funcional. No imponer touch-action o overscroll globales.
- Respetar áreas seguras cuando haya controles junto al borde. Usar altura flexible si el contenido crece.
- Permitir URLs de filtros o paginación cuando el flujo deba compartirse o restaurarse; no sincronizar cada estado interno con la URL.
- Revisar atrás, recarga y enlaces profundos del flujo pertinente.
- Conservar confirmación o recuperación para acciones destructivas según su efecto y diseño existente.
- En modos claro/oscuro comprobar color-scheme, controles nativos, contrastes y preferencia configurada.

## Evidencia y límites

Separar observación estática, comprobación en navegador y resultado de herramienta. Registrar defectos con ubicación verificable y prioridad por impacto. Esta lista es una revisión práctica, no una certificación exhaustiva de WCAG ni seguridad del backend.
