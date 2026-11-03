# Validación — 006 / Modales con Tailwind 4

2026-10-21. Implementación autorizada después de la revisión documental: «ya revisé, puedes implementar». Implementación local comprobada con límites; aceptación funcional humana pendiente. Sin `.git`: no hay commit/estado de árbol verificable. Se compararon los dos archivos editados con copias propias anteriores mediante `git diff --no-index` (exit 1 significa diferencias).

## Antecedente documental

La entrega inicial leyó reglas/contexto/specs y aplicó 06 → 01/02/03, sin código ni pruebas. Se cotejaron 254 archivos sin cambios y 60 enlaces locales sin roturas en diez documentos. El diagnóstico inicial del margen era hipótesis. Esta sección conserva ese antecedente; los resultados siguientes corresponden a la implementación posterior mediante 04 y comprobaciones del plan.

## Entorno e aislamiento reales

- El launcher `.test-artifacts/dependencias-004/target/Scripts/python.exe --version` sigue fallando por ruta inexistente. No se reparó ni reemplazó `.venv`/target.
- `py.exe -3.12` usa un Python instalado que informa **3.12.0**. Se añadieron al `sys.path` los paquetes locales del target; Django informa **5.2.18**. `django.setup()` y check correctos con `DJANGO_SETTINGS_MODULE=core.test_settings`. No se importó `core.settings` ni se leyó `.env`.
- Ejecución del Python instalado requirió salir del sandbox por «Acceso denegado»; escalación aprobada para el arnés local. No hubo instalación ni actualización de dependencias. El runtime no se presenta como parcheado/productivo.
- Arnés temporal: `.test-artifacts/modales-006/review.py`, modos prepare/checks/permissions/serve. Prepare creó exclusivamente `.test-artifacts/modales-006-review.sqlite3`, previa comprobación de carpeta y ausencia de archivo, aplicó migraciones a esa base nueva y generó siete cuentas y dos pacientes ficticios. Pruebas Django en base temporal en memoria. Medios solo de configuración ficticia.
- Servidor de revisión ligado a `127.0.0.1:8766`; comprobaciones visuales con IAB. Se usó `localhost:8766` tras detectar que el navegador conservaba el CSS anterior en caché; se comprobó la hoja efectivamente aplicada. No se alteraron datos recibidos ni se añaden endpoints al producto.

## Fallos reproducidos y corrección

| Caso | Antes | Después |
|---|---|---|
| Cuentas, 1440 × 900 | Dialog de 480 × 209,1 px en x=0/y=0; margen computado 0 | x=480/y=345,45; margen automático, centro del viewport y tamaño conservado |
| Pacientes, teclado | Sin dialog semántico; foco en activador y Tab alcanzaba Editar detrás del overlay | Dialog nativo modal, nombre ligado a H2, foco inicial en Cerrar, fondo inerte, retorno al activador al cerrar |
| Respuestas/fallos antiguos | Cuatro pruebas iniciales fallaron: Alfa sobrescribía Beta, fallo antiguo cerraba nueva consulta, respuesta repoblaba modal cerrado, error cerraba sin recuperación en diálogo | Contador invalida solicitudes previas; cierre limpia datos/carga/error; error HTTP/red visible dentro con cierre siempre disponible. Cuatro pruebas pasan |
| Clic exterior | Se conserva cierre exterior de pacientes | Quinta regresión distingue backdrop de contenido/borde; cierre exterior también comprobado en navegador |

Cambios: `static/css/styles.css`, `templates/pages/clinitens/docente/pacientes.html`, nueva `static/js/paciente-modal.test.cjs` y CSS generado por build. Componente/helper compartido sin consumidor localizado: intactos. Vistas/permisos/rutas y dependencias: intactos; nueve hashes de referencias coinciden antes/después.

## Comandos y resultados ejecutados

| Comando / directorio | Resultado real | Alcance |
|---|---|---|
| Launcher target `--version` | Fallo: instalación anterior inexistente | No se ocultó ni reparó |
| `py.exe -3.12 .test-artifacts/modales-006/review.py prepare` | Exit 0; migraciones y fixture nueva aisladas | No se migró la base recibida |
| `node.exe --test static/js/paciente-modal.test.cjs` antes del parche | Exit 1; cuatro fallos reproducidos | Prueba del controlador real extraído de la plantilla, no de copia simulada |
| `py.exe -3.12 .test-artifacts/modales-006/review.py checks` | Exit 0; check sin incidencias, **35 pruebas Django**, cero fallidas/omitidas, 1,331 s | UsuarioApp y CliniTensDocenteApp; no suite completa ni validación 005 |
| `py.exe -3.12 .test-artifacts/modales-006/review.py permissions` | Exit 0; **21 GET y cuatro POST** con resultados esperados | Anónimo/inactivo 302; alumno/sin perfil 403; MANAGER paciente propio 200/ajeno 404/cuentas 403; ADMIN y superusuario activo sin perfil 200. POST superusuario 403, propia cuenta sin cambios, CSRF ausente 403 y desactivación permitida; fixture restaurada por rollback |
| `node.exe build.cjs`, desde `theme/static_src` | Exit 0; Tailwind **4.3.3**, 282 ms | Build existente, salida regenerada; no edición manual ni cambio de lock |
| `node.exe --test static/js/mensajes.test.cjs static/js/paciente-modal.test.cjs theme/static_src/build.test.cjs` final | Exit 0; **9 JS**, cero fallidas/omitidas, 140,5 ms | Cinco nuevas de pacientes, dos mensajes, dos conservación CSS ante fallo/incompletitud |

## Interfaz comprobada

| RF | Comprobación real | Resultado y límite |
|---|---|---|
| RF-006-01 | Cuentas a 1440/768/390 px | Centrado y acciones legibles. 390 px: x=16/ancho≈358,4, sin scroll horizontal de documento. Zoom real 200% pendiente |
| RF-006-02 | Cuentas: Cancelar/Escape; pacientes: Cerrar/Escape/clic exterior/reapertura; consulta de estado modal y foco | Apertura nativa, fondo bloqueado y foco de retorno correctos. La tabulación nativa no permite acceder a controles del fondo; puede salir al chrome del navegador. Sin errores/warnings de consola al revisar pacientes |
| RF-006-03 | Éxito, carga visible, cambio de Alfa a Beta en navegador; respuestas diferidas, cierre en carga y fallos HTTP/red en pruebas JS | Paciente correcto; cierre/error recuperables en controlador. Error/red no se simularon en la UI integrada |
| RF-006-04 | Matriz de URLs/POST, UI de confirmación/cancelación | Permisos, métodos y CSRF preservados; no se pulsó desactivación en UI. Superusuario protegido y propia cuenta sin cambios comprobados en fixture |
| RF-006-05 | Build, controles de recuperación y regresión visual móvil | Portadas inicio/CliniTENS/FarmaTEF, inventario vacío y formulario de ingreso a ficha: un H1, sin desbordamiento horizontal. No valida editor completo, dispensación ni alcance 005 |

Pacientes a 1440/768/390 px: anchos 768/736/≈358,4; fondo con overflow bloqueado durante apertura y restaurado al cerrar. Contenido largo a 390 px: ventana de 812 px, scrollHeight 1282/clientHeight 810, desplazamiento interno≈471; historial alcanzable, documento sin desplazamiento. Escape desde el contenido largo devuelve foco al activador. Sin transición nueva; emulación de `prefers-reduced-motion` no ejecutada.

El atajo de zoom probado no cambió `innerWidth` ni `devicePixelRatio` en IAB. No se declara revisado zoom 200% ni se sustituye por una captura más pequeña. No se probaron Safari/Firefox ni se certifica accesibilidad exhaustiva.

## Evidencia conservada

- [Cuentas antes](../../docs/evidencias/006-modales/cuentas-antes.png), [después a 1440](../../docs/evidencias/006-modales/cuentas-despues-1440.png) y [después a 390](../../docs/evidencias/006-modales/cuentas-despues-390.png).
- [Pacientes a 390 con contenido largo](../../docs/evidencias/006-modales/pacientes-despues-390.png).
- [Medidas de interfaz](../../docs/evidencias/006-modales/interfaz.json), [regresión móvil](../../docs/evidencias/006-modales/regresion.json) y [matriz de permisos](../../docs/evidencias/006-modales/permisos.json).

Referencias técnicas del diagnóstico documental: [guía de migración Tailwind](https://tailwindcss.com/docs/upgrade-guide#dialog-margins-removed) y [contrato HTML de dialog](https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element). No sustituyen la evidencia propia anterior.

## Cierre y pendientes

Implementación terminada en los consumidores demostrados; T-006-06 queda parcial por zoom 200%/emulación de movimiento reducido. P-006-01/02/03 resueltos para este alcance. Próximo paso: completar esas verificaciones y revisión funcional del usuario; aceptación final pendiente. Servidor ficticio detenido al cierre, pestaña temporal cerrada y viewport restaurado. No se modificaron modelos/migraciones/endpoints/permisos, reglas generales, datos recibidos ni PDF/Excel. Sin despliegue, commit/push o restauración del RAR.
