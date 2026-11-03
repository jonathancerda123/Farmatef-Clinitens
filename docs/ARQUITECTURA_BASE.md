# Arquitectura actual — CliniTENS

## Resumen

CliniTENS es una aplicación web Django renderizada en el servidor. Sus módulos actuales gestionan cuentas, actividades, fichas estructuradas, revisión de resultados y, en una primera etapa, inventario simulado de FarmaTEF. La interfaz se entrega como HTML y CSS; las operaciones de escritura se procesan en el servidor.

La arquitectura descrita aquí refleja el código y la configuración del repositorio. No implica que el sistema esté desplegado ni preparado para uso productivo. La base local es SQLite; los servicios compartidos de correo, proxy, caché, almacenamiento y respaldo deben definirse para cada entorno de operación.

## Componentes

| Componente | Responsabilidad actual |
|---|---|
| `core/settings.py` | Configuración de la aplicación, variables de entorno, seguridad y correo |
| `core/test_settings.py` | Configuración aislada de pruebas con base en memoria y medios temporales; no carga `.env` ni settings normales |
| `core/permissions.py`, `core/mixins.py` | Autorización por cargo y propiedad, comprobaciones para vistas y formularios |
| `core/media.py` | Entrega de archivos privados luego de comprobar autorización sobre el objeto relacionado |
| `UsuarioApp` | Cuentas, cargos, perfiles, cambio de contraseña inicial e integración de autenticación |
| `homeApp` | Portadas, navegación y actualización de actividad |
| `CliniTensDocenteApp` | Actividades, cursos, participantes, importación de planillas, revisión y publicación de resultados |
| `CliniTensFichaApp` | Fichas estructuradas, validación de esquema, estados y control de versiones |
| `FarmaTEFApp` | Inventario inicial de medicamentos y lotes, con acceso por rol y propiedad |
| `theme/static_src/` | Fuentes de estilos, configuración y proceso de compilación de CSS |

## Flujo de solicitudes

1. El navegador solicita una página o envía un formulario.
2. Django resuelve la ruta y comprueba autenticación, cargo, estado y propiedad según la operación.
3. La vista valida los datos y aplica las reglas de negocio en el servidor.
4. El modelo persiste los cambios y la plantilla presenta el resultado.
5. Los archivos privados se entregan a través de una vista autorizada; el servidor web no debe exponer `MEDIA_ROOT` como directorio público.

No hay una API REST pública, una SPA, workers asíncronos ni WebSockets. La actividad visible se actualiza mediante solicitudes periódicas. La operación de inventario comienza en `/farmatef/inventario/`; las rutas de receta y dispensación aún no existen.

## Persistencia y modelos existentes

La aplicación utiliza modelos Django y SQLite en el entorno local documentado. Entre las estructuras existentes se encuentran cuentas/perfiles, actividades, cursos, fichas, rúbricas, resultados y archivos asociados.

Las fichas usan versiones para detectar escrituras obsoletas. La publicación de una evaluación conserva el resultado vigente hasta que se completa la nueva publicación. La relación entre actividad y curso condiciona el acceso de participantes cuando hay matrícula configurada.

FarmaTEF añade `Medicamento` y `LoteInventario`. El total se calcula a partir de las unidades de los lotes y las alertas se derivan del mínimo y de la proximidad del vencimiento. El umbral de vencimiento tiene un valor predeterminado configurable. La migración inicial es aditiva, fue escrita manualmente y aún requiere cotejo automático; no se ha aplicado a una base persistente recibida.

Antes de aplicar migraciones a un entorno con datos, se requiere generar/cotejar migraciones con el runtime previsto, respaldar la base y documentar recuperación. Las pruebas deben usar datos ficticios y una base aislada.

## Autorización

Los nombres técnicos de cargos son RESTRICTED, MANAGER y ADMIN. El superusuario activo tiene reglas globales conforme a los permisos definidos en el proyecto.

| Operación | RESTRICTED | MANAGER | ADMIN / superusuario activo |
|---|---|---|---|
| Cuentas | Sin acceso administrativo | Sin acceso administrativo | Gestión global, con protección especial de otras cuentas superusuario |
| Actividades, catálogo y cursos | Sin gestión | Gestiona los elementos propios | Acceso global |
| Fichas y resultados | Acceso a sus propios elementos permitidos | Acceso según responsabilidad y propiedad | Acceso global |
| Inventario FarmaTEF | Sin gestión en el incremento actual | Gestiona y consulta inventario propio | Consulta y gestión global |
| Archivos privados | Solo si la regla del objeto lo permite | Solo asociados a objetos propios/autorizados | Acceso global según las reglas del sistema |

La matriz resume el diseño actual y no sustituye las comprobaciones de cada vista. El servidor debe denegar accesos directos no autorizados aunque el usuario conozca la URL.

## Validación y contratos de datos

- Las fichas aceptan campos conocidos, tipos y catálogos permitidos; el servidor limita longitud, filas y tamaño total.
- El envío requiere los campos de identificación y que las demás secciones estén completas o marcadas «No aplica».
- Las escrituras de ficha y rúbrica incluyen una versión y estado esperado. Una versión obsoleta no debe sobrescribir cambios más recientes.
- La publicación de evaluación valida los indicadores requeridos y persiste la actualización de forma consistente.
- Los formularios de FarmaTEF deben validar tipos, cantidades, fechas y relaciones en servidor, y asignar el responsable desde la sesión autenticada.
- La dispensación todavía no está implementada. Su diseño requiere reservar/seleccionar lotes y actualizar stock de forma atómica, sin comprobante de éxito si la operación falla.

## Archivos, contenido y credenciales

Los archivos se validan por extensión, tamaño y firma según el tipo. Las imágenes se inspeccionan con Pillow. El contenido HTML se sanitiza en servidor con la biblioteca configurada. Los medios privados requieren autorización y cabeceras que eviten almacenamiento compartido no deseado.

Los enlaces de credenciales temporales usan caché efímera, se vinculan a usuario/curso/sesión, permiten un solo uso y expiran. La contraseña inicial obliga a cambiarla y caduca según la configuración documentada. Las celdas importadas desde planillas se tratan como texto literal.

La validación antivirus de documentos y medios no está integrada. El despliegue deberá decidir escaneo, límites, almacenamiento, retención y recuperación de archivos antes de operar con información real.

## Interfaz y recursos

Las plantillas comparten el layout de la aplicación, componentes y estilos. Tailwind 4 se compila mediante el CLI del proyecto; los recursos JavaScript de Alpine y DOMPurify se sirven localmente. La guía de tokens y componentes está en [PERSONALIZACION_VISUAL.md](PERSONALIZACION_VISUAL.md).

La compilación produce CSS y conserva el artefacto anterior si falla la generación o se detectan utilidades faltantes, de acuerdo con los controles descritos en la validación de la spec 004. La interfaz no sustituye permisos, validaciones ni estados del servidor.

### Modales implementados — 006 / 2026-10-21

Cuentas usa `dialog.account-dialog` con API nativa (`usuarios_lista.html`, estilos en `static/css/styles.css`). 006 reprodujo la pérdida de centrado por margen cero y añadió margen automático, máximos de tamaño y desplazamiento acotados a los diálogos activos. Pacientes ahora usa `dialog.patient-dialog`, controlado por Alpine mediante API nativa; reemplaza el overlay que permitía alcanzar controles del fondo. El nombre se asocia a H2, Cerrar está disponible también durante carga/error, Escape devuelve foco y el clic exterior conserva cierre.

Un contador de solicitud invalida respuestas y errores anteriores al cierre/reapertura; el detalle sigue consumiendo el mismo JSON autorizado y no añade persistencia. CSS bloquea scroll del documento mientras uno de esos diálogos está abierto. El componente `components/modal/modal.html` y helper `static/js/modal.js` no tienen consumidores localizados y siguen intactos. Sin framework, endpoint o dependencia nueva. [Validación 006](../specs/006-modales-tailwind4/validation.md): pruebas/build/navegador ejecutados, zoom y movimiento reducido pendientes; no reemplaza evidencia histórica 004 ni valida 005.

## Entornos y operación

- La configuración normal carga opciones del entorno y puede conectarse a servicios configurados para la instalación.
- `core.test_settings` es exclusivamente para pruebas aisladas y no debe usarse para operar el producto.
- El correo está configurado para consola por defecto; SMTP requiere credenciales y verificación propias del entorno.
- HTTPS, cookies seguras y HSTS dependen de la configuración de producción y del proxy frontal.
- Proxy, caché compartida, base de datos administrada, almacenamiento privado, logging, alertas, respaldo y restauración requieren configuración y pruebas operativas.
- El runtime Python indicado para las dependencias actuales no está disponible en el equipo de desarrollo, por lo que el incremento FarmaTEF aún no tiene `manage.py check` ni pruebas ejecutadas.

Ver [ENTORNO_Y_VERIFICACION.md](ENTORNO_Y_VERIFICACION.md), [VALIDACION_PREPRODUCCION.md](VALIDACION_PREPRODUCCION.md) y la [validación de la spec activa](../specs/005-farmatef-mvp-informe2/validation.md) antes de preparar un entorno persistente.

## Límites actuales

- Receta, dispensación, comprobante y etiqueta no están implementados.
- FarmaTEF no se integra con farmacias ni con sistemas clínicos reales; sus transacciones son simuladas.
- La integración de IA no está implementada.
- La migración inicial de FarmaTEF requiere cotejo automático y verificación sobre base ficticia aislada.
- No se han medido indicadores de rendimiento o disponibilidad para una instalación operativa.
- No se debe considerar el sistema listo para producción hasta completar pruebas, configurar y verificar servicios operativos, revisar seguridad y obtener aceptación de los responsables del producto.
