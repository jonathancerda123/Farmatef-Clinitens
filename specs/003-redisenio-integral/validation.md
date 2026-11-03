# Validación — 003

2026-10-08. Base main/f6e60fc; rediseño autorizado, implementado y comprobado localmente. Aceptación visual humana pendiente. Se aplicaron las tres skills locales solicitadas; la integración genérica de frontend-design se adaptó al Django/Tailwind 3 real. No se modificaron esas skills.

## Entorno y preservación

Python 3.12/Django 5.1.2 de .venv, Tailwind 3.4.19 existente. Configuración independiente core.test_settings; suite en memoria y navegador con .test-artifacts/revision.sqlite3, creada con fixtures. No se leyó .env, la base ni medios recibidos. Roles ficticios docente_demo, alumno_demo, admin_demo y root_demo; correos example.test. Servidor temporal en loopback 127.0.0.1:8765, detenido al cierre; tab temporal cerrada y viewport restaurado.

Git inicial: f6e60fc, solo .codex/ sin seguimiento; conservada. Ningún cambio de modelos, migraciones, rutas, reglas, paquetes o datos recibidos. Cambios Python limitados a clases de widgets, textos corregidos e idioma español de CKEditor; test_settings usa el mismo idioma. Sin commit, push ni despliegue durante 003.

## Auditoría y correcciones

Ubicaciones relativas al proyecto; se citan elementos verificables, sin inventar líneas. Preferencias de identidad se distinguen de defectos funcionales/accesibles.

| Prioridad | Archivo / elemento | Evidencia y efecto | Corrección / verificación |
|---|---|---|---|
| Alta | components/Layout/base_extendido; docente/base_docente; ficha/base_estudiante | Tres navegaciones/fondos y accesos de cuenta distintos; el usuario pierde continuidad | app_shell compartido, contexto por rol, perfil/inicio y página activa; observado en inicio/docente/ficha/cuentas |
| Alta | docente/casos/codigos/formulario; ficha/ingreso/editor | Labels sin asociación; errores generales omitidos y formulario cerrado tras error | BoundFields/includes, labels dinámicos, resumen visible y panel abierto; POST inválido conserva título y no crea caso |
| Alta | header/components/profile; menú móvil | Estado ARIA fijo, enlaces fuera de tabulación, ausencia de Escape | details/summary nativos, foco visible, Escape/retorno; comprobados en perfil y menú móvil |
| Alta | ficha/editor, aside y fieldset | Navegador a 390 px: sección lateral y tabla de lectura ensanchaban el documento a 1521/754 px | min-width:0 en rejilla/secciones/fieldset; documento final 375/375 px, tabla conserva su scroll |
| Media | index/clinitens/farmatef | Gradientes y tarjetas sin relación visual; preferencia del usuario por identidad común | Portada por tareas, marca de ficha, petróleo/verde clínico, tipografía local y módulos previstos explícitos |
| Media | static/css/mensajes.css y mensajes.js | CSS global de button/icon y toast fijo; podía afectar controles y móvil | Estilos acotados, ancho adaptable, cierre con button etiquetado; tres regresiones JS correctas |
| Media | tablas/editor | Regiones sin nombre/foco y controles de fila sin label | th/scope, regiones identificadas y enfocables; fila añadida en navegador con siete nombres por columna/fila |
| Media | usuarios_lista, confirmación de cuenta | Buscador dependía del encabezado anterior; modal sin foco nativo y decía eliminar para desactivar | Buscador dentro de pantalla, preserva search/inactive; dialog nativo, Escape y retorno a Desactivar comprobados; no se desactivó cuenta |
| Media | CliniTensFichaApp/forms.py, selector de actividad | Caracteres dañados en Código, separador y errores; observados en navegador y en HEAD | Textos UTF-8 corregidos; GET final contiene Código de actividad sin mojibake; misma validación |
| Media | perfil/registro, apoyo_diagnostico, verified_email_required | H1 repetidos y una etiqueta h1/h2 desparejada | H1 común y H2 de subsección; 27 páginas renderizadas con un H1; 91 templates compilados |
| Media | docente/rubrica, resumen y niveles | Tres tarjetas de colores y repetición de explicación en cada opción; ruido al evaluar | Resumen único, instrucciones comunes y opciones neutrales; selección verde/aria-pressed, cálculo preservado |
| Media | components/input_perfil y formularios de cuenta | Error de imagen no se mostraba junto al selector; faltaban errores generales de perfil | Error visible/identificado y resúmenes; JS asocia errores identificados mediante aria-describedby |

## Comandos y resultados

| Ejecución real | Resultado | Límite |
|---|---|---|
| npm.cmd run build, desde theme/static_src | Correcto; salida styles.css generada, último build 513 ms | Aviso existente caniuse-lite desactualizado; OBS-024 pendiente, sin instalar/actualizar paquetes |
| .venv/Scripts/python.exe manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp --settings=core.test_settings --verbosity=1 | 47 aprobadas, 0.635 s | Suite funcional existente; no demuestra cobertura visual ni carga |
| node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs | 3 aprobadas | Seguridad del texto de avisos, contenedor ausente y conservación del CSS ante fallo |
| node.exe --check static/js/design-system.js | Sin errores | Sintaxis; interacciones comprobadas aparte en navegador |
| manage.py check --settings=core.test_settings | Sin incidencias | No es check de despliegue |
| manage.py makemigrations --check --dry-run --settings=core.test_settings | No changes detected | No compara ni migra base recibida |
| ast.parse en apps/core/theme y get_template de templates/theme/templates | 75 Python y 91 HTML sin errores | Compilación no ejecuta cada estado de plantilla |
| Django Client con fixtures: 18 GET docente, 6 estudiante y 3 ADMIN | 27 respuestas 200, estructura común, un H1 | Incluye portadas, catálogos, cursos, ficha, rúbrica, perfil y MFA; no todos los estados posibles |
| URL directa: estudiante a docente; docente a usuarios | Dos 403 conservados | Roles/matrícula/globalidad completos cubiertos por suite 002 |
| POST de caso con título ficticio y contenido ausente | 200, errores/panel/título presentes, ningún caso creado | Solo fixture, no envío válido de caso |
| SVG de marca con ElementTree | XML válido | Inspección visual de marca realizada en navegador |
| Comprobador de Markdown/enlaces/fences en raíz, docs, specs y prompts | 41 Markdown, 163 enlaces locales, cero errores | No inspecciona enlaces externos; capturas de revisión permanecen locales |
| git diff --check al cierre | Sin errores | Avisos de normalización LF/CRLF de Git; archivos de skills preservados |

## Revisión en navegador

Se observaron acceso/logout, inicio, selección de módulos, dashboard/catálogo/formulario, revisión de ficha, editor estudiantil, rúbrica, cuentas/buscador/diálogo y creación de cuenta. Se revisaron escritorio 1280 y 1440, tablet 768x1024 y teléfono 390x844.

- Inicio y ficha final: documento sin desbordamiento horizontal. En ficha de lectura con tabla: clientWidth/scrollWidth 375/375, 753/753 y 1425/1425; tabla móvil contenida en 309 px. Secciones y tablas tienen desplazamiento propio.
- Menú y perfil: abrir/cerrar con controles nativos, Escape cierra y retorna foco. Diálogo de cuenta inicia en Cancelar; Escape retorna a Desactivar. Búsqueda otro_demo preservada en URL. Root protegido visible sin acción de desactivar.
- Estudiante: ingreso por código/docente, guardado real de borrador ficticio desde UI y valor conservado tras recarga. No se envió/finalizó una ficha. No aplica visible, bloqueo en ficha enviada y navegación de 13 secciones.
- Tabla estudiantil: desmarcar No aplica y agregar fila genera siete nombres accesibles por columna/fila; scroll del documento sigue 375 px. Cambios de esta prueba descartados al recargar, sin guardar.
- Rúbrica: selección local de un nivel refleja 1/15 criterios, 5 puntos, 5% y nota 1.3, con aria-pressed. No se publicó ni guardó esa selección. Resumen final revisado después de su simplificación.
- CKEditor: barra local española visible (Párrafo, Negrita, Cursiva). Sin errores de consola en el registro consultado al final de la revisión de rúbrica.

### Contraste medido

Luminancia relativa sRGB calculada con Python, no estimación visual. Pares concretos comprobados:

| Par | Ratio |
|---|---|
| Texto #19363C / blanco | 12.85:1 |
| Secundario #566B71 / blanco | 5.62:1 |
| Blanco / acción #00796F | 5.30:1 |
| Navegación #DFEFEF / #17474E | 8.66:1 |
| Selección #17474E / #D3EEE6 | 8.37:1 |

No se certifica WCAG ni se midieron exhaustivamente todos los colores/estados. CSS incluye foco visible y prefers-reduced-motion; reducción de movimiento revisada en fuente, sin simulación de esa preferencia en dispositivo.

### Capturas locales

Archivos de revisión ignorados por Git, con contenido ficticio. Conservarlos al revisar esta entrega; su enlace puede faltar en un clon.

- [Inicio anterior](../../.test-artifacts/003-inicio-antes.jpg).
- [Inicio final escritorio](../../.test-artifacts/003-inicio-despues.jpg) y [móvil](../../.test-artifacts/003-inicio-movil.jpg).
- [Dashboard docente](../../.test-artifacts/003-docente-despues.jpg).
- [Acceso final](../../.test-artifacts/003-acceso-desktop.jpg).
- [Ficha estudiantil](../../.test-artifacts/003-ficha-desktop.jpg).
- [Rúbrica final](../../.test-artifacts/003-rubrica-desktop.jpg).

## Límites y aceptación

No se probaron Safari, lectores de pantalla, dispositivos táctiles físicos, zoom extremo, cargas grandes ni todos los estados de MFA/correo. Regiones de tabla enfocables verificadas; desplazamiento horizontal por teclado requiere una revisión adicional en navegadores objetivo. PDF/Excel no cambian en 003; su validación permanece histórica en 002, sin nueva exportación aquí. Django admin queda fuera del rediseño. Los avisos de build en OBS-024 siguen pendientes.

No hay migración ni respaldo nuevo requerido por 003; recuperación de presentación en [guía visual](../../docs/PERSONALIZACION_VISUAL.md). Pendiente aceptación visual/pedagógica del usuario; esto no autoriza despliegue. Comprobación documental y Git final en [VERIFICACION](../../docs/VERIFICACION.md).

## Ajuste puntual solicitado — flecha de cuenta

Se sustituyó el carácter de flecha por un SVG decorativo de 16 px. CSS gira 180° con transición de 180 ms según details[open]; la regla existente de movimiento reducido sigue aplicando. Build correcto (514 ms), navegador ficticio: transformación identidad al cerrar y rotación 180° al abrir; Escape cierra y mantiene el foco. Captura local .test-artifacts/003-flecha-svg.jpg. No se repitió la suite funcional por este ajuste exclusivamente visual; servidor/tab temporales cerrados.
