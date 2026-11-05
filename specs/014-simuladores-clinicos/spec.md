# 014 — Simuladores educativos DAU, laboratorio clínico y Kardex

Fecha: 2026-11-04. Estado: alcance propuesto para revisión; no implementado. Fuente: petición explícita de la usuaria para habilitar los tres módulos que aparecen como «en desarrollo». Área: CliniTENS. La petición autoriza trabajar en estos módulos, pero no define reglas docentes/clínicas detalladas. Revisión académica pendiente.

## Problema, actores y resultado

La portada de Área clínica anuncia Atención de urgencia (DAU), Laboratorio clínico y Kardex de enfermería, pero hoy son rótulos sin acceso. El objetivo es convertirlos en recorridos de práctica dentro de CliniTENS usando exclusivamente casos, pacientes, resultados, órdenes y registros sintéticos.

Actores: estudiante RESTRICTED practica en actividades asignadas; docente MANAGER prepara y revisa material de sus cursos; ADMIN/superusuario activo administra material global según permisos centrales. Se reutilizan autenticación, cursos y permisos actuales.

## Alcance y exclusiones

- DAU: ficha de recepción/atención simulada por caso con motivo, observaciones del escenario, registro educativo y disposición de cierre. No representa triage clínico oficial ni recomienda atención real.
- Laboratorio: crear una solicitud educativa de exámenes desde un caso, registrar resultados ficticios con unidades y rangos de referencia definidos por el caso, y marcar el flujo solicitado/resultado disponible/revisado. Los valores no se presentan como rangos clínicos de uso real.
- Kardex: hoja cronológica educativa por caso con indicaciones ficticias preparadas por docente, horarios planificados, marca de administración/omisión, responsable autenticado y observación. No calcula dosis, no genera indicaciones y no recomienda fármacos.
- El material se restringe al responsable/colaboradores docentes del curso y a estudiantes inscritos, siguiendo las comprobaciones de CliniTENS. Las actividades sin curso no se convierten automáticamente en cohortes.
- Cada pantalla indica «Simulación educativa — datos ficticios». No se incorporan datos reales, diagnósticos/órdenes de pacientes ni reglas clínicas institucionales.

Fuera de alcance: operación asistencial, guía de decisiones clínicas, escalas de triage oficiales, interpretación automática de resultados, integración con laboratorio/farmacia/hospital, firma clínica, notificaciones de emergencia, analítica de salud, acceso a fichas ajenas, el módulo de administración de módulos que también aparece en la portada y cualquier despliegue.

## Permisos por acción/dato

| Acción | Anónimo | RESTRICTED | MANAGER | ADMIN / superusuario activo | Propiedad/curso |
|---|---|---|---|---|---|
| Ver/practicar caso publicado | Denegado | Solo actividad asignada y propio intento | No participa como estudiante | Sin intento de alumno | Matrícula vigente si hay curso |
| Crear/editar caso, solicitud, indicación | Denegado | Denegado | Solo material y cursos propios o colaborados según permiso específico | Global | Responsable/colaborador del curso |
| Ver resultados de práctica | Denegado | Solo resultado propio permitido | Casos de cursos propios/colaborados | Global | Nunca fichas o intentos ajenos del estudiante |
| Registrar acción de Kardex | Denegado | Solo en su propio intento | Denegado en vista estudiante | Sin intento de alumno | Matrícula y caso autorizado |

Las vistas deben validar en servidor autenticación, cargo, propiedad, curso, matrícula, estado publicado y pertenencia del intento; ocultar enlaces no reemplaza esos controles. Usuario inactivo, cargo ausente o acceso directo no autorizado se deniega.

## Flujo, datos y reglas

1. El docente crea un caso educativo para un curso, completa los datos sintéticos y prepara sus etapas. Nada se publica de forma parcial.
2. El estudiante inscrito abre el caso publicado y genera un intento propio; no recibe material reservado a corrección docente.
3. En DAU registra los campos solicitados por el caso y cierra la etapa con una disposición educativa. Se conserva historial de cambios relevante.
4. En laboratorio, registra solicitud y resultados simulados; valores/unidades/rangos se capturan desde el material preparado. No se interpretan automáticamente como normal/anormal.
5. En Kardex, cada acción se realiza contra una indicación y horario preparados; se registra administrado/omitido y una observación acotada. Una misma acción no puede confirmarse dos veces; las correcciones se agregan como eventos auditables y no borran silenciosamente el registro original.
6. El docente revisa la actividad desde los cursos autorizados. Los estudiantes no consultan el trabajo de compañeros.

Toda persistencia nueva usa migración aditiva, restricciones de integridad y escrituras atómicas donde haya transición de estado. Formularios validan tipos, longitudes, fechas y vínculos en servidor. No se guardan medios ni se lee/escribe la base local recibida como parte de esta spec.

## Requisitos y aceptación

- RF-014-01: Las tres tarjetas de la portada abren módulos navegables y el cuarto («Perfil administrador de módulos») permanece pendiente.
- RF-014-02: Docente puede preparar, guardar como borrador y publicar un caso ficticio con etapas DAU, laboratorio y Kardex; datos incompletos no se publican.
- RF-014-03: Estudiante inscrito puede abrir solo casos publicados de sus cursos y registrar su propio intento en las tres etapas.
- RF-014-04: Las solicitudes y resultados de laboratorio conservan los renglones ficticios ingresados; la interfaz no los diagnostica ni los etiqueta como interpretación clínica.
- RF-014-05: La administración/omisión del Kardex exige acción explícita del estudiante, guarda actor, fecha/hora y observación, y no permite duplicar ni alterar silenciosamente el evento.
- RF-014-06: Docente ve resultados solo de cursos propios/colaborados; estudiantes no pueden leer ni alterar intentos ajenos por URL directa.
- RF-014-07: Las pantallas y exportaciones, si luego se aprueban, advierten que son simulaciones educativas con datos ficticios.
- RF-014-08: Los casos se pueden demostrar sin usar datos recibidos, servicios externos ni inventario FarmaTEF.

| RF | Dado / cuando | Entonces | Caso negativo/límite |
|---|---|---|---|
| 014-01 | Usuario autenticado selecciona cualquiera de las tres tarjetas | Abre la sección correspondiente con navegación y título coherentes | Anónimo redirigido a autenticación |
| 014-02/03 | Docente publica material de curso y estudiante inscrito abre | Se crea intento individual con contenido ficticio | No inscrito, borrador o curso ajeno: denegado |
| 014-04 | Estudiante guarda un resultado preparado | Valor y unidad se conservan literalmente | No hay juicio ni interpretación automática |
| 014-05 | Estudiante registra una administración u omisión | Evento aparece con autor y marca temporal | Repetición o ID ajeno no crea ni modifica otro evento |
| 014-06 | Usuario intenta URL/ID de otra persona o curso | No revela existencia ni datos restringidos | Roles inactivo/sin perfil también se rechazan |

## Compatibilidad y no funcionales

Se mantiene la ficha clínica existente y las rutas actuales. Reutilizar templates base, componentes, tokens y reglas de los docs de arquitectura y personalización visual. Todo contenido debe ser ficticio y usar texto explícito de simulación. Accesibilidad por teclado, labels/errores, diseño móvil y separación de datos por curso forman parte de la aceptación.

## Decisiones y revisión

Supuesto elegido para permitir prototipo: son módulos de simulación educativa vinculados a cursos, no una herramienta de trabajo clínico. Los formularios son flexibles y el docente define contenido; no se incorporan protocolos, rangos, escalas ni dosis predeterminadas. Validación pedagógica y de contenido por la docente queda pendiente. La aceptación final de interfaz/recorrido pertenece a la usuaria.
