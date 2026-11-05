# 011 — Eliminar recetas sin actividad desde el historial

Fecha: 2026-11-04. Estado: implementación autorizada por la petición «falta un botón de eliminar receta en el historial». Área: FarmaTEF. Código autorizado: sí, solo interfaz y operación local. Revisión humana: pendiente.

## Problema, actores y resultado

El historial docente de recetas no ofrece una acción para retirar una receta ingresada por error. Se agregará una acción visible junto a cada registro, respetando el ámbito del docente y conservando cualquier historial de respuestas o dispensaciones.

## Alcance y exclusiones

- ADMIN/superusuario activos pueden operar globalmente; MANAGER solo sobre recetas propias, conforme a la política de permisos existente.
- La acción requiere POST y CSRF; GET nunca elimina.
- Solo se eliminan recetas sin respuestas estudiantiles, dispensaciones, saldo entregado ni estado/campos de entrega. Sus líneas se eliminan dentro de la misma transacción.
- Recetas con actividad estudiantil o docente muestran un indicador de historial protegido y no ofrecen un botón accionable.
- El servidor vuelve a comprobar propiedad y actividad; no confía en la tabla ni en un botón deshabilitado.
- Sin nuevas columnas, migraciones, borrado masivo, cambios en inventario, ni modificación de registros con auditoría.

## Permisos por acción

| Acción | RESTRICTED | MANAGER | ADMIN/superusuario | Ámbito |
|---|---|---|---|---|
| Eliminar receta sin actividad | Denegado | Permitido | Permitido | `objetos_del_docente` también en el POST |
| Eliminar receta con respuestas o dispensaciones | Denegado | Denegado | Denegado | La regla aplica globalmente |

## Requisitos y aceptación

- RF-011-01: El historial muestra «Eliminar» solo cuando una receta no tiene respuestas estudiantiles ni datos de entrega, y advierte que registros con actividad se conservan.
- RF-011-02: El botón solicita confirmación y envía POST con CSRF.
- RF-011-03: El POST directo de un usuario sin permiso, para una receta ajena o con cualquier respuesta/dato de entrega no elimina nada.
- RF-011-04: Una receta elegible y propia se elimina junto a sus líneas en una transacción; una falla deja la receta intacta.
- RF-011-05: La redirección vuelve al historial y comunica el resultado sin exponer registros de otro ámbito.

## Decisiones y revisión

«Eliminar» significa retirar una receta no utilizada. Respuestas y dispensaciones constituyen historial/auditoría y no se purgan mediante esta acción. La revisión funcional en navegador y aceptación docente quedan pendientes.
