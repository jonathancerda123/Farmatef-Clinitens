# Estado y punto de reanudación — CliniTENS

## Petición actual — DAU, laboratorio y Centro de Apoyo Diagnóstico / 2026-11-05

La solicitud 017 distingue procesos. DAU conserva signos vitales, procedimientos y cierre. Laboratorio permite órdenes con muestra/tubo, registro tubo a tubo y etiquetas educativas imprimibles. Centro de Apoyo Diagnóstico reemplaza el Kardex en la experiencia vigente y separa resultados ficticios de laboratorio, imagen, ECG e informes; el historial/modelos Kardex anteriores se conservan sin reutilizarlos. Migración 0005 creada y aplicada solo a memoria mediante `core.test_settings`; la base habitual no se migró. `manage.py check` y `makemigrations --check --dry-run` pasan. Navegador, impresión física, matriz de permisos y revisión docente/estudiante siguen pendientes. Ver [spec 017](../specs/017-flujos-dau-laboratorio-cad/spec.md).

La solicitud 018 amplía el laboratorio a un flujo de tres pasos (paciente SIM, exámenes y resumen), emisión de orden con snapshot, PDF, etiquetas por tubo e historial propio. La migración 0006 se aplicó en la base local tras crear y verificar el respaldo `.test-artifacts/lab-018/db.sqlite3.before-20261105`; la base recibida/producción no se modificó. Los checks técnicos pasan; revisión visual, docente y de impresión pendiente. Ver [spec 018](../specs/018-flujo-laboratorio-por-pasos/spec.md).

## Colaboración con GitHub — 2026-11-03

El usuario solicita subir el proyecto a `jonathancerda123/Farmatef-Clinitens` para trabajar desde dos equipos. Quedan autorizados la inicialización de Git, el primer commit y su publicación en ese repositorio; sin despliegue ni operación sobre la base recibida. Se comprobó que el remoto está vacío y es público. La carpeta local ya se inicializó con rama `main`; las menciones posteriores a ausencia de `.git` conservan el contexto histórico de 006.

Se amplió `.gitignore` y se añadió [la guía de colaboración](COLABORACION_GITHUB.md). La revisión del índice preparado contó 699 archivos y cero coincidencias con las rutas excluidas de configuración privada, base, medios, entornos, dependencias y temporales. Una búsqueda estática de patrones de secretos en archivos candidatos solo señaló dos valores ficticios de pruebas; no equivale a una auditoría exhaustiva. No se abrieron `.env`, bases ni medios. Se detectó whitespace preexistente en archivos incluidos, conservado sin reformatear. No se ejecutaron pruebas funcionales porque este cambio solo prepara versionado y documentación.

Se creó el commit inicial local `ae32dfa`. El primer intento de push quedó esperando y se interrumpió; el reintento no interactivo confirmó que Git no dispone de autenticación utilizable: `unable to get password from user`. La conexión de GitHub de la aplicación sí tiene permisos, pero esa sesión no autentica automáticamente el Git de Windows. No se ha confirmado publicación. Próximo paso: ejecutar `git push -u origin main` en una terminal interactiva y completar el inicio de sesión de GitHub; comparar después el commit local con el remoto. A continuación, clonar en el segundo equipo y preparar allí el entorno conforme a la guía. No compartir contraseñas ni tokens en el chat.

| Campo | Estado actual |
|---|---|
| Producto | CliniTENS: aplicación web para gestionar actividades, registros, usuarios y resultados de una organización. Incluye FarmaTEF para procesos de inventario y dispensación simulada. |
| Fase | Desarrollo de un prototipo funcional para revisión de usuarios y responsables del negocio. |
| Alcance técnico | El alcance vigente está descrito en la [especificación de FarmaTEF](../specs/005-farmatef-mvp-informe2/spec.md). |
| Capacidades existentes | Cuentas, perfiles, permisos, actividades, registros estructurados, revisión y publicación de resultados. |
| FarmaTEF implementado | Inventario ficticio, recetas multimed, casos asignados a curso, respuestas individuales y despacho FEFO simulado con stock atómico. |
| FarmaTEF pendiente | Comprobantes, etiquetas, pruebas funcionales y revisión visual/educativa del flujo estudiantil. |
| Integración externa | No implementada. No hay conexión con farmacias, sistemas clínicos, proveedores de identidad ni servicios de IA. |
| Verificación del incremento actual | `check` y cotejo de migraciones limpios con settings de prueba; no se ejecutaron pruebas funcionales ni navegador para el recorrido estudiante. |
| Entorno de desarrollo | El intérprete Python configurado para las dependencias actuales apunta a una instalación inexistente en este equipo. |
| Datos | Las pruebas y demostraciones deben usar registros ficticios. No se inspeccionaron ni modificaron `.env`, la base de datos recibida o los archivos de `media/`. |
| Siguiente hito | Completar un recorrido demostrable de inventario y dispensación simulada, validar reglas y permisos con usuarios responsables y registrar su aceptación y los pendientes. |

## Petición actual — DAU según referencia visual / 2026-11-04

Se reorganizó la pantalla DAU para aproximar las capturas compartidas: entrada por código ficticio, ficha de paciente, cuadrícula de signos, procedimientos cronológicos, cierre DAU, historial e impresión/PDF. Identidad del funcionario proviene de la sesión. PAM e IMC se recalculan en servidor; los datos permanecen marcados como simulación. [Spec 015](../specs/015-dau-flujo-visual/spec.md).

La migración `CliniTensSimulacionApp.0003` se generó y aplicó únicamente en la base SQLite en memoria de `core.test_settings`. **No se aplicó a la base local normal**; antes de usar el formulario DAU allí, revisar el plan, crear respaldo en `.test-artifacts/backups/` y ejecutar la migración. Pasaron `manage.py check`, cotejo de migraciones y carga de cuatro plantillas/resolución de rutas en settings aislados. No se ejecutaron pruebas funcionales, no se generó/revisó PDF ni se usó navegador; aceptación visual y pedagógica pendiente.

## Petición actual — accesos docentes diferenciados por módulo / 2026-11-04

Las tarjetas docentes ya no llevan a una misma ruta: DAU, laboratorio y Kardex tienen páginas de preparación distintas. Cada página permite editar únicamente su bloque en casos borrador de cursos visibles; los casos publicados se muestran en solo lectura. La DAU docente permite mantener identidad sintética SIM y escenario; laboratorio mantiene contexto de solicitud; Kardex mantiene actividades por línea. No se cambió el esquema. Pasaron `manage.py check`, cotejo de migraciones y carga/reverse de páginas/rutas con `core.test_settings`. No se corrieron pruebas funcionales, no se verificaron accesos por petición HTTP ni se revisó navegador. Aceptación visual/funcional pendiente. Ver [spec 016](../specs/016-modulos-clinicos-separados/spec.md).

## Petición actual — DAU, laboratorio y Kardex / 2026-11-04

La usuaria pidió implementar los tres módulos pendientes de la portada. Se añadió `CliniTensSimulacionApp`, con casos ficticios vinculados a cursos, preparación docente, práctica por etapas DAU/laboratorio/Kardex, intentos aislados por estudiante e historial de eventos Kardex. La cuarta tarjeta de administración de módulos permanece pendiente. [Spec 014](../specs/014-simuladores-clinicos/spec.md), [plan](../specs/014-simuladores-clinicos/plan.md), [tareas](../specs/014-simuladores-clinicos/tasks.md), [validación](../specs/014-simuladores-clinicos/validation.md).

Pasaron `manage.py check`, `makemigrations --check --dry-run`, carga de plantillas y resolución de rutas. Las migraciones se probaron en memoria y después se aplicaron a la base local tras guardar una copia en `.test-artifacts/backups/db.sqlite3.pre-simulaciones-20261104.bak`; `showmigrations` confirma ambas. No se inspeccionaron los registros. No se ejecutaron pruebas funcionales ni revisión de navegador. Próximo: actualizar la página de gestión y confirmar el flujo; luego revisar con la docente.

## Petición actual — 006, modales / 2026-10-21

Paquete documental revisado; el usuario autorizó después «ya revisé, puedes implementar». Se aplicó 04-implementar con comprobaciones del plan. [Spec](../specs/006-modales-tailwind4/spec.md), [plan](../specs/006-modales-tailwind4/plan.md), [tareas](../specs/006-modales-tailwind4/tasks.md) y [validación](../specs/006-modales-tailwind4/validation.md) actualizados. Aceptación funcional final pendiente.

Implementado: centrado y límites de scroll explícitos en cuentas; pacientes usa diálogo nativo tras reproducir foco detrás del overlay, con cierre siempre disponible y protección contra respuestas antiguas. Componente/helper compartido sin consumidor localizado intactos. No cambiaron backend, modelos, permisos, dependencias ni datos recibidos.

Esta carpeta no contiene `.git`: no hay rama/commit ni limpieza verificables; se compararon únicamente copias propias de los archivos editados. El launcher target volvió a fallar. 006 se comprobó con Python instalado 3.12.0 y paquetes del target, `core.test_settings` y fixture nueva en `.test-artifacts`; no se repararon entornos ni se valida 005 con esos resultados.

Resultados: check, 35 pruebas Django, 9 JS y build Tailwind 4.3.3 correctos; 21 GET/cuatro POST de permisos con resultados esperados. Navegador 1440/768/390, cierre/foco y scroll interno; regresión móvil de portadas, ingreso a ficha e inventario. T-006-06 parcial: quedan zoom real 200% y emulación de movimiento reducido. Próximo paso: completar esas comprobaciones y revisión funcional del usuario. El alcance/autorización y pendientes de FarmaTEF 005 siguen separados.

## Estado de FarmaTEF

Recetas incorpora búsqueda, historial, líneas múltiples (hasta 10), despacho parcial docente y práctica estudiantil asignada a cursos. La clave de falsificación/vencimiento se reserva a docentes; el estudiante recibe pistas y retroalimentación después de responder. Solo una respuesta correcta de dispensar en receta válida descuenta stock por FEFO atómicamente; otras respuestas no cambian existencias. El historial ofrece eliminar recetas sin actividad; las que tienen respuestas o dispensaciones se conservan. La spec 012 añade docentes colaboradores por curso con acceso limitado a recetas FarmaTEF; migración 0008 aplicada a la base local después de un respaldo. `manage.py check`, el cotejo de migraciones, carga de plantillas y rutas pasan con `core.test_settings`; la revisión de navegador y pruebas funcionales siguen pendientes. Detalles: [spec 009](../specs/009-historial-entrega-parcial/validation.md), [spec 010](../specs/010-practica-estudiantil-recetas/validation.md), [spec 011](../specs/011-eliminar-recetas-sin-actividad/validation.md) y [spec 012](../specs/012-docentes-colaboradores-farmatef/validation.md).

El 2026-11-03 se añadieron cinco recetas técnicas no clínicas multimed a la base local (`DEMO-MULTI-*`), dos medicamentos y una unidad por línea, sin alterar lotes ni existencias. Respaldo previo: `.test-artifacts/recetas-011/db.sqlite3.before`.

La spec 011 agrega eliminación docente de recetas sin respuestas ni datos de entrega. No cambió el esquema ni se eliminaron registros de la base durante la implementación; la revisión del botón en navegador sigue pendiente.

La spec 012 agrega asignación y revocación de colaboradores para que Alexandra pueda acceder a las recetas del curso autorizado por su responsable. La migración `CliniTensDocenteApp.0008` se aplicó después del respaldo `.test-artifacts/recetas-012/db.sqlite3.before`. Próximo paso: agregar a Alexandra desde el detalle del curso y revisar su historial.

La spec 013 agrega Etiquetado desde la portada FarmaTEF. La vista prepara una etiqueta de un lote accesible, con dimensiones y copias acotadas; no persiste ni modifica stock y no requiere migración. La pantalla se ajustó a la referencia aportada: formulario y datos a la izquierda, vista previa y controles a la derecha, cuatro presets y medidas editables. Tras las capturas de la usuaria se aclaró que medicamento es el producto y lote la partida; el selector destaca número de lote, vencimiento y stock y filtra las partidas según el medicamento seleccionado. Un reporte de selectores vacíos identificó que los widgets personalizados habían perdido sus `choices`; se restableció la vinculación campo/widget y se comprobó sin consultar los registros de inventario. La relación también se valida en servidor. Los mínimos son 40×30 mm para evitar recortes. `manage.py check`, cotejo de migraciones, vínculo de opciones y resolución de plantilla/ruta pasan tras esta corrección. No se ejecutaron pruebas funcionales ni se pudo completar la revisión visual automatizada porque la herramienta no identificó con confianza la URL activa; no se interactuó con páginas. Pendiente calibrar con impresora; se solicita imprimir al 100% y medir una copia antes de usar el tamaño.

El primer incremento permite a usuarios autorizados registrar medicamentos y lotes de demostración, consultar existencias y ver alertas calculadas desde el stock mínimo y las fechas de vencimiento almacenadas.

El siguiente recorrido propuesto es localizar una receta ficticia, validar productos y cantidades, seleccionar lotes disponibles, confirmar la operación y actualizar el inventario en una transacción atómica. Si ocurre un error, no debe quedar un descuento parcial ni generarse un comprobante que indique éxito.

Los comprobantes y etiquetas deben indicar que corresponden a una operación simulada. El prototipo no debe utilizarse para dispensar medicamentos reales ni para tomar decisiones clínicas. La generación asistida por IA tampoco está implementada; cualquier integración futura requiere revisión de privacidad, costos, seguridad y aprobación del contenido antes de mostrarlo a usuarios.

## Preparación para una entrega funcional

Antes de acordar una entrega con una organización usuaria, se deben definir:

- Los perfiles que usarán cada función y los permisos asociados.
- Las reglas de catálogo, lotes, vencimientos, recetas, sustituciones y dispensación.
- El historial que se debe conservar y cómo se corrigen errores operativos.
- Los criterios de aceptación que permitan demostrar cada flujo.
- El entorno de demostración, respaldo, recuperación y responsables de aprobación.
- Los indicadores de servicio que realmente se medirán.

La entrega se considerará aceptada cuando las personas responsables revisen los criterios acordados y quede registrada la evidencia de lo que funciona y de lo que permanece pendiente. No hay fecha de entrega comprometida en este documento.

## Riesgos y decisiones pendientes

- El intérprete Python indicado no inicia; hasta contar con un entorno válido, el código actual no está verificado.
- La migración `0001_initial` requiere cotejo automático y aplicación de prueba en una base ficticia aislada.
- Las reglas operativas de recetas, cantidades, sustituciones, lotes, vencimientos y dispensación deben acordarse con usuarios responsables.
- Deben definirse los permisos de administración del catálogo, autorización de dispensación y acceso al historial.
- Los indicadores de servicio, disponibilidad y rendimiento no se han medido ni constituyen compromisos.
- El prototipo aún no está preparado para almacenar o procesar información real; faltan verificaciones técnicas y operativas.

## Reglas para reanudar

- Inspeccionar archivos y estado del proyecto antes de editar.
- Distinguir requisitos acordados, propuestas, implementación y validación.
- Usar datos ficticios en pruebas y demostraciones.
- No leer secretos, datos de la base local ni contenido de `media/`.
- Aplicar permisos en el servidor y verificar también las rutas directas.
- Registrar comandos y resultados únicamente después de ejecutarlos.
- Antes de migrar un entorno persistente, documentar respaldo, migración y recuperación.
- No desplegar, modificar producción, hacer commit/push ni eliminar historia sin autorización explícita.

## Referencias internas

- [Definición del producto](PROYECTO.md)
- [Arquitectura](ARQUITECTURA_BASE.md)
- [Trazabilidad](TRAZABILIDAD.md)
- [Entorno, verificación y recuperación](ENTORNO_Y_VERIFICACION.md)
- [Revisión de preparación operativa](VALIDACION_PREPRODUCCION.md)


## Carga autorizada de catálogo Vademécum 2023 — 2026-10-31

Tras revisar la tabla extraída de las fichas pp. 8–55, el usuario confirmó la base habitual y la cuenta valita, e indicó «Solo preparar cantidades; no crear lotes todavía». Se verificó exclusivamente identidad/rol activo de valita, esquema/migración y catálogo/lotes necesarios para esta operación, sin leer contraseñas, .env ni media. La autorización puntual permite esta carga en la base habitual; no habilita otras lecturas o migraciones.

Se crearon 109 medicamentos bajo valita (cuenta activa ADMIN/superusuario). El catálogo estaba vacío: no se actualizaron existentes. Para nombres repetidos se añadió concentración y forma al nombre, conforme a la restricción existente por responsable, sin cambiar modelos. Datos ausentes o contradictorios no se completaron: Diclac conserva concentración vacía y Tronsalan forma vacía, con evidencia en manifiesto. Los 11 suplementos no se cargaron.

Las cantidades ficticias de 1 a 40 (2.465 unidades propuestas para medicamentos) permanecen solo en el archivo de preparación. No se crearon lotes ni vencimientos ni códigos de barras. El stock mínimo conserva el valor predeterminado del modelo (0); el stock de los nuevos medicamentos es 0. No se modificó código, configuración, dependencias ni migraciones.

Plan, recuperación, preparación y manifiesto con IDs/páginas/notas: `output/farmatef/vademecum-2023-plan-carga.json`, `vademecum-2023-preparacion.md`, `vademecum-2023-preparacion.json` y `vademecum-2023-carga.json`. Respaldo SQLite previo en `.test-artifacts/farmatef-vademecum-2023/` (ruta exacta en manifiesto); no compartirlo como artefacto público.

Comandos ejecutados mediante bloques Python por stdin con `C:/Users/jonat/AppData/Local/Programs/Python/Python312/python.exe`, paquetes del target por sys.path: inspección acotada SQLite en modo lectura; `settings.configure` mínimo para auth/contenttypes/FarmaTEFApp sin importar settings normales ni core.test_settings; `full_clean` de los 109 modelos; respaldo SQLite e integrity_check; ensayo de las 109 altas en transaction.atomic con rollback obligatorio; carga atómica; reapertura y comparación de campos/autor/valores predeterminados; cotejo de lotes antes/después mediante instantánea y SHA-256; integrity_check final. Resultados correctos, 109 altas, 0 actualizaciones, lotes 0 antes/0 después. Python 3.12.0, Django 5.2.18. Launcher target sigue roto; no se reparó.

Límites: no se ejecutó navegador, URLs ni suite funcional completa; esta verificación respalda la carga de datos, no certifica permisos de vistas ni dispensación/descuento. No hubo migraciones, despliegue, commit/push. Próximo paso: revisar catálogo visible con valita; antes de cargar otro PDF comparar los cuatro campos y reportar nuevos/existentes/diferencias, sin sobrescritura automática ni cambios de lotes/existencias. Crear lotes o probar descuentos requiere una solicitud posterior.
