# 005 — MVP FarmaTEF y preparación del Informe 2

Fecha: 2026-10-17. Estado: borrador de trabajo. Fuente: Informe 1 y guía/plantilla TIHI84 Unidad 2. Código autorizado: sí, por solicitud explícita del equipo de avanzar programando la solución. Revisión académica y validación docente: pendientes.

## Problema, actores y resultado

El Informe 1 identifica que Técnico en Farmacia carece de un flujo digital persistente para practicar inventario y dispensación. El repositorio actual implementa CliniTENS para TENS, pero deja FarmaTEF pendiente. Se propone construir incrementalmente un prototipo formativo que integre Farmacia con el sistema existente y conserve el flujo complementario CliniTENS ya implementado.

Actores: estudiante, docente/gestor del curso y administrador. Todas las recetas, personas, medicamentos y transacciones de demostración serán ficticios. El sistema no prescribe ni se conecta a farmacias o sistemas clínicos reales.

## Alcance y exclusiones

El alcance académico de referencia es el MVP definido en el Informe 1:

- Flujo Farmacia: catálogo ficticio de medicamentos; inventario con lotes, vencimientos y umbrales; búsqueda/validación de receta; dispensación con descuento consistente de stock; comprobante PDF simulado y etiqueta imprimible.
- Flujo TENS complementario: especificación docente estructurada, propuesta visual sintética asistida por IA, trazabilidad y aprobación docente previa a publicación; observación y registro ficticio del estudiante según el MVP aprobado.
- Funciones transversales: identidad y permisos reutilizando Django/UsuarioApp, registro de eventos relevantes y pruebas de aceptación con datos sintéticos.
- Informe 2: tecnologías y factibilidad; herramientas/componentes; tres procesos BPMN con subprocesos; casos de uso y componentes UML; modelo lógico y diccionario; topología, infraestructura y arquitectura; KPI SMART y SLA; plan de pruebas y estándares; disponibilidad, continuidad, mantención y cronograma ajustado; conclusiones, referencias APA 7 y anexos.
- Preinforme EF2: fecha límite 2026-11-04, para retroalimentación del docente sobre el rumbo. Informe ES2 completo: 2026-11-25.
- EVS3: presentación del Informe ES2 y demostración del prototipo funcional los días 2026-12-02 y 2026-12-09. EVS4: defensa del proyecto los días 2026-12-16 y 2026-12-23. Las fechas vienen de confirmación del equipo el 2026-10-17; las pautas/rúbricas específicas aún no fueron adjuntadas.

Fuera del alcance del MVP: los módulos futuros del Informe 1, integraciones institucionales/productivas, uso de datos reales, diagnóstico/prescripción, despliegue productivo y generación de video.

## Requisitos y aceptación

- RF-005-01: Para el 2026-11-04 existe un preinforme trazable a los criterios EA3/EA4, con avances y pendientes distinguidos y sin presentar propuestas como implementación terminada.
- RF-005-02: Para el 2026-11-25 existe un informe alineado con las secciones II–X de la plantilla ES2, con anexos citados, evidencias verificables y referencias APA 7.
- RF-005-03: Para la demostración EVS3 (2026-12-02/09), el prototipo permite completar un recorrido Farmacia acordado, con datos sintéticos, permisos en servidor y resultado visible; el recorrido se prioriza en plan/tasks antes de cada incremento de código.
- RF-005-04: Toda operación de dispensación valida receta y disponibilidad y actualiza stock de manera atómica; una falla no deja descuento parcial ni comprobante que aparente éxito.
- RF-005-05: Inventario representa medicamento, lote, vencimiento, cantidad y umbral; alertas se derivan de datos almacenados y no de valores escritos por el estudiante.
- RF-005-06: Casos o material visual asistidos por IA no se publican a estudiantes hasta aprobación docente registrada. Si la integración externa no es viable por costo/tiempo/privacidad, el flujo conserva generación sintética simulada claramente identificada, sin afirmar uso de un proveedor real.
- RF-005-07: BPMN, UML, arquitectura, modelo de datos, KPI/SLA, plan de pruebas, normas y plan de implementación describen el sistema efectivamente construido y declaran explícitamente los elementos propuestos o no verificados.
- RF-005-08: URL directa, propiedad/curso/rol y archivos se protegen del lado servidor; se reutilizan permisos/patrones del proyecto sin atribuir acceso a la navegación visual.

## Primer incremento autorizado

T-005-04 se concreta en un inventario docente inicial dentro de una app FarmaTEF separada: crear/listar medicamentos y lotes ficticios, indicar stock agregado, señalar stock bajo el mínimo configurado y lotes vencidos/próximos a vencer. ADMIN/superusuario activos tienen vista global; MANAGER ve/gestiona lo propio, usando permisos centrales y filtros en consultas/forms. Estudiante o anónimo no puede abrir ni enviar la gestión. Próximo vencimiento usa un umbral configurable por medicamento (90 días por defecto). No incluye dispensación, ajuste manual de cantidades, eliminación de historial ni acceso estudiante en este incremento.

Aceptación del incremento: (a) docente autorizado puede registrar medicamento y lotes con código, vencimiento y unidades; (b) validación de formulario impide valores vacíos/fuera de tipo y el servidor fija autor; (c) lista muestra totales y alertas calculadas de datos persistidos; (d) usuario ajeno no puede leer ni modificar inventario de MANAGER por URL directa; (e) rutas de estudiante/anónimo reciben la protección definida por mixins y login existente. Cambio de persistencia es aditivo; migración nueva y recuperación se documentan antes de aplicar a cualquier base real.

## Restricciones y decisiones por validar

El Informe 1 estima 560 horas y 14 semanas (40 h/semana entre dos integrantes). Entre 2026-10-17 y ES2 (2026-11-25) hay aproximadamente 5,6 semanas/220 horas; hasta la última fecha de EVS4 (2026-12-23), unas 9,6 semanas/380 horas. Es un riesgo de cronograma, no evidencia de que todo el MVP esté terminado. La priorización y cualquier reducción deben quedar validadas por el equipo/docente; el plan propone un recorrido vertical de Farmacia primero y mantiene IA/TENS como flujo complementario sujeto a factibilidad.

Pendiente confirmar con el equipo/docente: rúbricas EA3/EA4 completas y fechas de carga AAI, alcance exacto que evaluarán como prototipo, reglas docentes de receta/dispensación/etiqueta, responsable de datos y disponibilidad/costo/condiciones del proveedor IA. Hasta recibir esos datos, las propuestas se etiquetan como supuestos.

No se presupone que la estimación 99,5% de disponibilidad aplique a un prototipo local; KPI y SLA académicos deben diferenciar metas propuestas de mediciones observadas y acordarse con el docente/cliente.

## Revisiones

- 2026-10-17: primera síntesis de Informe 1, pauta y plantilla de Unidad 2; el equipo confirma 04/11 para preinforme, 25/11 para ES2, 02/12 y 09/12 para EVS3, y 16/12 y 23/12 para EVS4.
