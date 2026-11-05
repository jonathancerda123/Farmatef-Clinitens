# 010 — Práctica estudiantil de validación y dispensación de recetas

Fecha: 2026-11-04. Estado: implementación autorizada localmente. Fuente: «me gusta, hazlo». Código autorizado para preparar casos docentes, permitir respuesta de estudiantes inscritos y descontar inventario solo ante una dispensación simulada correcta.

## Problema, actores y resultado

FarmaTEF permite al personal docente administrar y dispensar recetas simuladas, pero no ofrece un ejercicio de decisión a estudiantes. Se añadirá un flujo que evalúa si reconocen una receta vencida, una sospecha de falsificación u otra inconsistencia configurada por el docente, sin revelar la clave antes de responder.

## Alcance y exclusiones

- Docente MANAGER crea casos para sus cursos; ADMIN/superusuario activo puede operar globalmente conforme a la política 002.
- Cada receta nueva se asigna a un curso. Recetas históricas sin curso permanecen en el historial docente y no aparecen a estudiantes.
- RESTRICTED activo inscrito en el curso puede revisar el caso y escoger «Dispensar» o «Rechazar receta» con un motivo.
- El docente configura una clave privada (por ejemplo, sospecha de falsificación), una pista visible para el estudiante y retroalimentación posterior a la respuesta. La clave no se renderiza ni se serializa en la página estudiantil.
- Vencimiento se obtiene de la fecha de vigencia. Si es inválida, se espera el rechazo por vencimiento; si no está vencida y tiene clave de rechazo, se espera el rechazo indicado; si no, se espera dispensar.
- Solo una decisión correcta de dispensación en una receta válida descuenta todas las líneas en una transacción atómica y registra lotes FEFO. Rechazos y respuestas incorrectas no afectan stock. Si no hay existencias suficientes, se revierte todo y se puede intentar de nuevo.
- Un estudiante puede responder una vez por receta. El historial de intentos se conserva por estudiante; una respuesta de una persona no altera la respuesta de las demás.
- Los datos, personas y operaciones son ficticios. Los casos y combinaciones no constituyen pautas clínicas ni recomendaciones.
- No incluye carga de receta real, OCR, firma, verificación externa, diagnósticos, prescripción clínica, comprobantes ni despliegue.

## Permisos por acción

| Acción | RESTRICTED | MANAGER | ADMIN/superusuario | Ámbito |
|---|---|---|---|---|
| Administrar casos | Denegado | Solo propios y vinculados a curso propio | Global | Servidor, no solo menú |
| Ver ejercicio | Recetas de cursos donde está inscrito | No como estudiante | No como estudiante | Membresía comprobada en GET y POST |
| Responder | Una respuesta propia por receta/curso | Denegado | Denegado | Unicidad receta/estudiante |
| Ver respuestas | Denegado | Casos propios | Global | Excluir clave secreta del estudiante |

## Requisitos y aceptación

- RF-010-01: El docente asigna la receta a un curso autorizado.
- RF-010-02: Solo estudiantes activos inscritos en ese curso pueden abrir y responder el caso; rutas directas ajenas dan 404/denegación.
- RF-010-03: La pantalla estudiantil muestra receta, medicamentos, fecha y pistas configuradas, pero no la marca de sospecha, respuesta esperada ni retroalimentación previa.
- RF-010-04: «Rechazar receta» requiere motivo: vencida, sospecha de falsificación, datos inconsistentes, información incompleta u otro.
- RF-010-05: Luego de responder se muestra si la decisión fue correcta y la explicación docente; no se permite un segundo intento.
- RF-010-06: La clave esperada para receta vencida se determina de la fecha; la clave para falsificación u otra inconsistencia se almacena separada de la pista visible.
- RF-010-07: Dispensación correcta de receta válida descuenta todos los medicamentos en lotes FEFO dentro de una transacción; la falta de stock no deja descuentos parciales.
- RF-010-08: Rechazo o decisión incorrecta no modifica existencias. Un intento incorrecto de dispensar caso inválido queda registrado para evaluación sin descontar stock.
- RF-010-09: La respuesta y la auditoría de despacho se almacenan por estudiante para que un estudiante no cierre el caso a los demás.
- RF-010-10: Los registros existentes se conservan; recetas sin curso no quedan asignadas automáticamente.

## Decisiones

- Una receta de curso se comparte como caso, pero cada estudiante tiene un intento independiente. Si varios estudiantes dispensan correctamente, cada operación consume inventario compartido; el docente debe disponer de stock ficticio suficiente para la cohorte.
- Un caso de falsificación permanece visible con pistas educativas. No se muestra «falsa» como aviso previo. La marca docente se usa en servidor para corregir la respuesta.
- Si se marca sospecha de falsificación, se requiere una pista visible y retroalimentación posterior para que el ejercicio sea evaluable y pedagógico.
- Aceptación humana del flujo y pertinencia académica de las pistas siguen pendientes.
