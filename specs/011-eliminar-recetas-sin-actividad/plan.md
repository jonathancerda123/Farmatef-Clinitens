# Plan técnico — 011 / eliminar recetas sin actividad

Spec: [spec.md](spec.md). Implementación local autorizada.

## Base inspeccionada

Se revisaron las instrucciones del repositorio, el índice SDD, la spec 010 y los modelos, servicio, vista, ruta y plantilla vigentes de FarmaTEF. Se preservan los cambios locales existentes. `RecetaLinea`, `RespuestaReceta`, `Dispensacion` y sus auditorías usan relaciones protectoras; respuestas y entregas no se deben borrar.

## Integración

| RF | Archivo | Cambio | Verificación prevista |
|---|---|---|---|
| 011-01/02 | `templates/pages/farmatef/recetas.html`, `FarmaTEFApp/views.py` | Acción de historial, anotaciones para mostrar disponibilidad y endpoint POST con confirmación | Carga de plantilla, ruta inversa y revisión estática |
| 011-03/04 | `FarmaTEFApp/services.py` | Servicio transaccional, filtro por autor y bloqueo si hay respuestas o datos de entrega; borrar líneas antes de la receta | Inspección del control de permisos y regla de conservación; sin modificar la base local |
| 011-05 | `FarmaTEFApp/urls.py` | Ruta POST con nombre explícito | Resolver URL |
| 011-01/05 | `specs/README.md`, `docs/TRAZABILIDAD.md`, `docs/ESTADO_PROYECTO.md`, validación | Registrar alcance, estado y límites | Coherencia documental |

## Migraciones y reversión

No se modifican modelos ni esquema; no requiere migración. El endpoint realiza una eliminación acotada, atómica e iniciada por el docente después de una confirmación visible. Los registros con historial quedan protegidos.

## Riesgos y límites

La confirmación del navegador no es autorización: propiedad/rol y ausencia de actividad se revalidan en servidor. No se ejecutan pruebas funcionales ni se navega a la base local bajo las instrucciones vigentes; revisión de UI queda pendiente.
