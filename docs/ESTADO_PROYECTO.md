# Estado y punto de reanudación — CliniTENS

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
| FarmaTEF implementado | Primer incremento para registrar y consultar medicamentos y lotes ficticios, calcular existencias y mostrar alertas por stock mínimo y vencimiento. |
| FarmaTEF pendiente | Validación de recetas, dispensación, descuento atómico de stock, comprobantes, etiquetas e historial de movimientos. |
| Integración externa | No implementada. No hay conexión con farmacias, sistemas clínicos, proveedores de identidad ni servicios de IA. |
| Verificación del incremento actual | Pendiente: no se ejecutaron `manage.py check` ni pruebas para FarmaTEF. La migración inicial se escribió manualmente y requiere cotejo automático. |
| Entorno de desarrollo | El intérprete Python configurado para las dependencias actuales apunta a una instalación inexistente en este equipo. |
| Datos | Las pruebas y demostraciones deben usar registros ficticios. No se inspeccionaron ni modificaron `.env`, la base de datos recibida o los archivos de `media/`. |
| Siguiente hito | Completar un recorrido demostrable de inventario y dispensación simulada, validar reglas y permisos con usuarios responsables y registrar su aceptación y los pendientes. |

## Petición actual — 006, modales / 2026-10-21

Paquete documental revisado; el usuario autorizó después «ya revisé, puedes implementar». Se aplicó 04-implementar con comprobaciones del plan. [Spec](../specs/006-modales-tailwind4/spec.md), [plan](../specs/006-modales-tailwind4/plan.md), [tareas](../specs/006-modales-tailwind4/tasks.md) y [validación](../specs/006-modales-tailwind4/validation.md) actualizados. Aceptación funcional final pendiente.

Implementado: centrado y límites de scroll explícitos en cuentas; pacientes usa diálogo nativo tras reproducir foco detrás del overlay, con cierre siempre disponible y protección contra respuestas antiguas. Componente/helper compartido sin consumidor localizado intactos. No cambiaron backend, modelos, permisos, dependencias ni datos recibidos.

Esta carpeta no contiene `.git`: no hay rama/commit ni limpieza verificables; se compararon únicamente copias propias de los archivos editados. El launcher target volvió a fallar. 006 se comprobó con Python instalado 3.12.0 y paquetes del target, `core.test_settings` y fixture nueva en `.test-artifacts`; no se repararon entornos ni se valida 005 con esos resultados.

Resultados: check, 35 pruebas Django, 9 JS y build Tailwind 4.3.3 correctos; 21 GET/cuatro POST de permisos con resultados esperados. Navegador 1440/768/390, cierre/foco y scroll interno; regresión móvil de portadas, ingreso a ficha e inventario. T-006-06 parcial: quedan zoom real 200% y emulación de movimiento reducido. Próximo paso: completar esas comprobaciones y revisión funcional del usuario. El alcance/autorización y pendientes de FarmaTEF 005 siguen separados.

## Estado de FarmaTEF

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
