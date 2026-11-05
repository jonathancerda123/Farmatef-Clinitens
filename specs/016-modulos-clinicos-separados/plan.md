# Plan técnico — 016 / Módulos clínicos diferenciados

Spec: [spec.md](spec.md). Autorizado por petición de la usuaria. No incluye cambios de base de datos: se reutilizan campos y eventos existentes.

| RF | Archivos previstos | Cambio | Evidencia |
|---|---|---|---|
| 016-01 | `urls.py`, `views.py`, portada CliniTENS | Rutas diferenciadas por módulo para docentes y tarjetas específicas | `reverse()` y plantillas cargadas |
| 016-02 | `forms.py`, `views.py`, formularios docentes por módulo | Actualización aislada de los campos DAU, laboratorio o Kardex | Check Django y revisión de flujo con datos ficticios en memoria si es posible |
| 016-03 | Mixins/querysets y vistas | Revalidar cargo, propiedad/colaboración y curso en cada POST | Revisar URL directa permitida/denegada con cliente de prueba si la configuración lo permite |
| 016-04/05 | Plantillas estudiantiles existentes | Conservar tres experiencias: atención DAU, laboratorio, Kardex | Rutas y plantillas cargadas; no confundir revisión estática con aceptación |
| 016-06 | Estilos de gestión y módulo | Identidad visual diferenciada, adaptable y accesible | Revisión navegador escritorio/móvil/teclado pendiente |

## Estructura elegida

El caso conserva sus tres bloques integrados y la publicación existente. Para evitar sobrescribir campos ajenos, cada vista docente usa un formulario acotado al bloque seleccionado. La pantalla de casos general se mantiene como entrada de creación de casos base; las tres tarjetas dejan de mandar allí. Cambiar datos de paciente afecta la presentación de futuras y actuales atenciones asociadas, por lo que no se permiten cambios a casos ya publicados desde la vista DAU sin retirar temporalmente la publicación. Si no hay mecanismo seguro existente para esto, dejar lectura en publicados y permitir edición solo en borrador.

## Verificación

Usar `core.test_settings`, comprobar `manage.py check`, cotejo de migraciones (sin cambios esperados), carga de plantillas y resolución de URLs. No correr pruebas funcionales automatizadas si no se solicitan; indicar límites. No migrar la base normal ni inspeccionar registros reales.
