# 018 — Flujo de solicitud de laboratorio por pasos

Fecha: 2026-11-05. Estado: autorizado para implementación local por solicitud explícita de la usuaria. Revisión humana pendiente. Área: `CliniTensSimulacionApp`.

## Problema y resultado

La práctica vigente permite registrar tubos preparados por el docente, pero no presenta el flujo de laboratorio de las referencias: identificación del paciente SIM, selección de exámenes, resumen y emisión de una orden con historial y etiquetas.

## Alcance y exclusiones

- Implementar flujo de solicitud de laboratorio de tres pasos y pantalla de orden emitida.
- Reutilizar el paciente ficticio SIM de un caso publicado y el usuario autenticado como operador simulado. No pedir RUT, RUN real ni crear acceso paralelo.
- El catálogo de exámenes proviene de las órdenes configuradas por el docente en el caso. La orden guarda una instantánea de esos exámenes para conservar el historial.
- Agrupar tubos por muestra/tipo, permitir prioridad y observaciones ficticias, emitir orden, imprimir/descargar orden y etiquetas, consultar historial del estudiante.
- Solo datos educativos ficticios. No hay interpretación de resultados, integración con laboratorio real ni publicación.
- Mantener rutas y registros previos compatibles; no borrar `IntentoSimulacion.tubos_laboratorio` ni alterar sus datos.

## Permisos por acción/dato

| Acción | Anónimo | RESTRICTED | MANAGER | ADMIN/superusuario activo | Propiedad/curso |
|---|---|---|---|---|---|
| Crear/editar borrador de orden | Denegado | Permitido | Denegado | Denegado | Caso publicado y matrícula activa; orden propia |
| Emitir orden | Denegado | Permitido | Denegado | Denegado | Estudiante autenticado inscrito en curso del caso |
| Ver historial, PDF y etiquetas | Denegado | Permitido | Denegado | Denegado | Solo órdenes propias |

## Flujo, datos y reglas

1. Paso Paciente: mostrar datos SIM existentes del caso, el operador de la sesión y curso/escenario; no pedir identificadores personales reales.
2. Paso Exámenes: buscar/filtrar el catálogo docente, seleccionar uno o más exámenes; mostrar resumen de seleccionados.
3. Paso Resumen: revisar paciente, exámenes, tubos requeridos, prioridad y observaciones antes de emitir.
4. Emisión genera código único y orden de solo lectura, con fecha/operador y copia inmutable de exámenes y tubos.
5. La confirmación ofrece impresión/descarga de orden y etiquetas educativas. Las etiquetas identifican código SIM, tubo, muestra y exámenes; cualquier código de barras visual es decorativo y se marca como no escaneable.
6. El historial lista órdenes emitidas del estudiante y caso; “Nueva solicitud” inicia un borrador independiente.
7. El servidor comprueba IDs del catálogo actual al crear borrador, sesión de alumno, matrícula, publicación y propiedad. Solo se aceptan hasta 30 exámenes y observaciones limitadas.

## Requisitos y aceptación

- RF-018-01: pasos Paciente → Exámenes → Resumen reflejan la referencia y navegan sin perder selecciones.
- RF-018-02: búsqueda y selección solo permiten exámenes del catálogo ficticio del caso; el resumen agrupa tubos correctamente.
- RF-018-03: emitir crea registro inmutable con código único, operador, fecha, prioridad, observaciones y snapshots.
- RF-018-04: confirmación permite imprimir/descargar orden y etiquetas educativas, adaptables a impresión.
- RF-018-05: historial muestra solo órdenes del estudiante autenticado y permite iniciar una nueva solicitud.
- RF-018-06: permisos de matrícula/publicación/propiedad se verifican en servidor; cambios persistentes son aditivos y no tocan la base recibida.

| RF | Dado / cuando | Entonces | Caso negativo/límite |
|---|---|---|---|
| 01 | Abrir laboratorio desde un caso matriculado | Aparece paso de paciente SIM y progreso de tres pasos | Caso ajeno no se revela |
| 02 | Buscar, seleccionar y continuar | Selección aparece y tubos se agrupan por muestra/tipo | ID manipulado, vacío o >30 no se acepta |
| 03 | Confirmar resumen | Orden queda emitida con código y snapshot | Reemitir orden emitida no cambia sus datos |
| 04 | Abrir recursos de orden | Orden y etiquetas imprimibles solo muestran datos SIM | Orden ajena no permite descargar |
| 05 | Consultar historial | Solo órdenes propias visibles | Cambiar PK a orden de otro alumno denegado |
| 06 | Ensayar migración | Cambio aditivo aplicado a memoria | No ejecutar migración en base habitual |

## Compatibilidad y decisiones

Se conserva el antiguo avance tubo-a-tubo en intentos por compatibilidad; las órdenes emitidas usan su snapshot y tienen su propio estado. Migración aditiva ensayada en `core.test_settings`; antes de aplicar en una base con datos debe hacerse copia y verificarse recuperación. PDF e impresión son educativos, no documentos clínicos reales. Revisión docente/estudiantil pendiente.
