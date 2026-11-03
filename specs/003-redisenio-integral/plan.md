# Plan — 003

[Spec](spec.md). Implementación autorizada. Base f6e60fc; único cambio previo sin seguimiento: .codex/ con skills del usuario, preservado.

## Dirección y tokens

Identidad: mesa de trabajo para simulación clínica. Barra lateral petróleo estable, superficie clara de trabajo, acento verde clínico y un distintivo de ficha en la portada. Contenido alineado a izquierda; lectura y formularios con ancho acotado, tablas usan el espacio disponible. No fotografías, gradientes ni animaciones decorativas.

Paleta base: superficie #FFFFFF, fondo #F2F6F6, tinta #19363C, secundario #566B71, petróleo #17474E, acción #00796F. Estados de éxito/advertencia/error separados con texto. Tipografía local: Trebuchet MS para títulos (cercanía y formas reconocibles), Segoe UI para lectura/controles; fallback del sistema. Sin fuentes remotas.

~~~text
escritorio: [marca / navegación fija] [ruta + título / perfil]
                                       [tarea y acciones]
                                       [contenido amplio / ficha]
móvil:     [marca / menú] [título / perfil]
           [contenido en una columna; tablas con scroll propio]
~~~

Se revisó el plan frente al pedido: sustituye el hero promocional y las tarjetas idénticas por un acceso orientado a tareas y una ficha como referencia visual. Sidebar común evita identidad distinta por rol; secciones clínicas conservan su numeración porque representan partes reales del registro. Bordes agrupan datos, no decoran.

## Integración

| RF | Archivos | Acción / comprobación |
|---|---|---|
| 01/02 | Layout/app_shell, bases, navegación, index/clinitens/farmatef | Una estructura y portada por tarea; navegador con roles |
| 03/04 | Templates docente/ficha/cuentas, CSS y widgets | Componentes compartidos, labels/errores, lectura/acciones |
| 05/06 | Shell/JS/tablas/diálogos | Menú compacto, teclado/Escape/foco/scroll y contraste medido |
| 07 | tokens.css, styles.css, docs/PERSONALIZACION_VISUAL.md | Tailwind 3 existente; build y reporte |

Validar inicialmente con servidor ficticio y conservar evidencia; después revisar acceso, inicio, catálogo/formulario, curso, ficha y rúbrica en escritorio/móvil. Regresiones existentes si cambian plantillas de flujos. No instalar paquetes estéticos ni modificar permisos/modelos.
