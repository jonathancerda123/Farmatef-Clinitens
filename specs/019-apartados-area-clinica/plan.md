# Plan técnico — 019

Spec: [spec.md](spec.md). Navegación autorizada por solicitud del usuario; RAE autorizado por confirmación posterior de la primera versión propuesta.

## Base y solución

Inspeccionados Git, documentación inicial, specs 014–018, portada, rutas, permisos y guía visual. No hay cambios locales previos. Reutilizar `CliniTENSView` para resolver destinos mediante `cargo`, `es_docente`, `es_administrador` y `reverse`; la plantilla itera los siete apartados. Los destinos mantienen su autorización actual.

| RF | Archivos | Verificación |
|---|---|---|
| 01/02 | `homeApp/views.py`, `templates/pages/clinitens/clinitens.html` | Render y GET directos con cuentas ficticias de diferentes cargos |
| 03 | Fuente `theme/static_src/src/styles.css`, iconos compartidos, CSS compilado | Build existente; navegador 1440/768/390, foco y orden |
| 04 | Modelo `AtencionEnfermeria`, migración 0007, formularios y vistas RAE en app existente; plantillas RAE | Pruebas funcionales sobre memoria: guardado/cierre/CAS/aislamiento/límites/URLs directas |
| 06 | Guía en portada; preparación docente paciente reutilizando validación SIM existente | Crear paciente ficticio sin modificar los otros bloques; publicado solo lectura |
| 05 | Git y documentación | `git status`, rama/upstream y diff final |

## Dirección visual

Identidad existente: canvas #F2F6F6, superficie #FFFFFF, texto #19363C, navegación #17474E, acción #00796F, apoyo #E6F4F0. Trebuchet MS para títulos y Segoe UI para cuerpo. Mantener introducción y guía actuales, con texto más específico; cuadrícula de apartados alineados a izquierda con icono, público, descripción y acción al pie. Orden de lectura fila a fila, sin ordenar por CSS. Tres columnas en escritorio amplio, dos en tablet y una en móvil.

Se revisó la dirección contra el pedido: no trasladar el azul ni la cabecera pública de las capturas porque el usuario pide conservar el estilo de la página actual. Las tarjetas corresponden a accesos reales solicitados, no a métricas/decoración; no se anuncia «sistema operativo» ni una versión sin evidencia.

## Datos y comprobación

Modelo nuevo aditivo RAE en `CliniTensSimulacionApp`, con caso/estudiante, cuidados/observaciones, cierre, fechas y versión. Restricción de un borrador por caso/estudiante; apertura con `get_or_create`. Guardado con queryset autorizado + estado/version esperados y `F('version') + 1`; 409 si no actualiza. Reutilizar búsqueda SIM y campos de paciente del formulario docente; RAE no redefine diagnósticos, tratamientos ni protocolos. Historial con paginación. Caso publicado y matrícula se vuelven a comprobar por cada solicitud.

Usar exclusivamente `core.test_settings`, fixtures sintéticas y artefactos ignorados. El target indicado por AGENTS no existe en esta copia; Python disponible 3.12.0 no tenía Django. Se preparó entorno aislado en `.test-artifacts/clinica-019-env` con requirements actuales. No migrar base habitual.

No añadir tests que solo dupliquen el listado de tarjetas; ejecutar verificaciones existentes y matriz HTTP pertinente. Añadir regresiones de RAE por persistencia, autorización y concurrencia lógica. Navegador para portada y recorrido RAE con datos exclusivamente sintéticos; no equivale a prueba de carga ni validación clínica. El esquema nuevo debe migrarse después con respaldo/autorización en el entorno habitual para usar RAE allí.
