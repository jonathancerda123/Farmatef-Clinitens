# 015 — Flujo DAU con estructura de atención educativa

Fecha: 2026-11-04. Estado: especificación autorizada en implementación local. Fuente: solicitud de la usuaria «así luce lo de urgencias, céntrate en dejarlo así», con tres capturas de referencia. Área: DAU en `CliniTensSimulacionApp`. Código autorizado para aproximar el flujo y jerarquía visual; revisión académica pendiente.

## Resultado esperado

El módulo DAU debe sentirse como un registro organizado de atención: entrada al caso, identificación del paciente del escenario, signos vitales, registro cronológico de procedimientos, cierre DAU, historial y opción de imprimir/descargar. Reutiliza sesión, cursos y casos ficticios del sistema existente.

## Alcance y límites

- Entrada dedicada al DAU, con funcionario identificado por la cuenta autenticada y búsqueda del caso por código de paciente simulado `SIM-...`.
- Datos del paciente ficticio configurados por docente en el caso: nombre, código, sexo, edad, fecha de nacimiento, comuna y antecedentes crónicos.
- Registro de presión sistólica/diastólica, PAM calculada, frecuencia cardiaca, frecuencia respiratoria, temperatura, saturación, HGT, peso, talla e IMC calculado. El servidor recalcula PAM e IMC, no confía en valores enviados para los campos automáticos y no clasifica resultados.
- Procedimientos educativos acumulados con descripción, observación, rol profesional simulado y fecha/autor de sesión.
- Cierre estructurado con motivo de consulta, antecedentes relevantes, evaluación registrada, observaciones e indicaciones educativas. Cerrar vuelve el DAU de solo lectura.
- Historial individual de atenciones DAU; nuevo registro crea una atención separada sin reemplazar registros cerrados.
- Documento PDF generado desde ReportLab ya instalado. Encabezado y pie dicen «SIMULACIÓN EDUCATIVA — DATOS FICTICIOS»; botón de impresión usa el diálogo del navegador.
- La presentación se aproxima a la jerarquía/campos de las capturas, adaptada a la identidad compartida de CliniTENS.

No se solicita ni almacena RUT de funcionarios o pacientes reales. El usuario autenticado se muestra como funcionario; el paciente se busca solo por el código ficticio configurado por docente. El módulo no se usa para atención real, triage ni recomendación diagnóstica/terapéutica. Los cálculos son aritmética educativa, no interpretaciones. No se copian de las capturas nombres, RUT, diagnósticos ni otros datos de personas.

## Permisos y datos

| Acción | Anónimo/inactivo | RESTRICTED | MANAGER | ADMIN/superusuario activo |
|---|---|---|---|---|
| Buscar paciente simulado y abrir DAU | Denegado | Caso publicado de curso con matrícula vigente; solo su cuenta crea/consulta | No accede como alumno | No accede como alumno en esta ruta |
| Registrar signos/procedimientos/cierre | Denegado | Solo atención propia y no cerrada | Denegado | Denegado |
| Historial y PDF | Denegado | Solo atenciones propias del curso vigente | Resultados docentes se mantienen en la vista de revisión limitada | Global solo mediante vista docente ya definida |
| Preparar perfil simulado | Denegado | Denegado | Solo casos en curso propio/colaborado | Global por curso visible |

Cada POST comprueba nuevamente sesión, inscripción, publicación, propiedad y estado. Un caso no se encuentra si el código no pertenece a un curso matriculado. Un DAU finalizado no se modifica; otro ejercicio genera una nueva atención. Ningún listado revela atenciones de otros estudiantes.

## Criterios de aceptación

- RF-015-01: Vista de entrada muestra la identidad autenticada del funcionario y busca pacientes solo por identificador ficticio SIM; no pide RUT real.
- RF-015-02: Caso del docente presenta ficha de paciente sintético y los datos aparecen en la identificación DAU.
- RF-015-03: Signos vitales se guardan en un borrador individual; PAM/IMC se calculan en cliente para vista previa y en servidor al guardar. No se generan banderas ni consejos clínicos.
- RF-015-04: Procedimientos se agregan al historial con texto acotado, rol simulado, autor y hora del servidor. No se borran con la edición del cierre.
- RF-015-05: Cierre requiere motivo y evaluación; persiste los demás campos, registra fecha y bloquea cambios y nuevos procedimientos.
- RF-015-06: Historial solo muestra atenciones del estudiante activo, permite abrir las propias y descargar PDF identificado como ficticio.
- RF-015-07: URL directa con código/atención ajena, usuario no inscrito, caso borrador o registro cerrado no permite lectura/escritura indebida.
- RF-015-08: Layout se adapta a escritorio, tablet y móvil, con labels, errores por campo y controles de teclado.

## Migración, reversión y revisión

Migración aditiva: datos simulados del paciente en `CasoSimulacion`; nueva entidad `AtencionDAU` para registros múltiples por estudiante/caso, y `ProcedimientoDAU` ligado a atención. La migración se prueba primero en SQLite en memoria y, para uso local, solo tras respaldo, conservando tablas y datos actuales. Reversión de app requiere mantener copia de respaldo compatible; no borrar atenciones automáticamente. Revisión visual/pedagógica por la usuaria y docente pendiente.
