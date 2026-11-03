# Implementar después de revisión

Contexto CliniTENS: leer [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md), [observaciones](../docs/OBSERVACIONES_PROYECTO.md) y [estado](../docs/ESTADO_PROYECTO.md). Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). Configuración normal core/settings.py y pruebas independientes core/test_settings.py. Política 002: MANAGER por autor, ADMIN/superusuario global; ficha estudiantil propia, matrícula si código tiene curso. Proteger superusuarios por atributo. La spec 001 es documental/histórica; 002 fue implementada por autorización explícita. No ampliar alcance sin pedido.


Puedes pedir a la IA que lea este archivo en el proyecto. Si copias el mensaje, reemplaza los campos entre <...>. Los nombres/IDs de ejemplo no son trabajo autorizado.

```text
He revisado los documentos de <carpeta de spec>.
Autorizo implementar únicamente <IDs de tareas o alcance completo de esa spec>.
Esta instrucción es posterior a la fase documental.

Lee docs/ENTORNO_Y_VERIFICACION.md y AGENTS.md, spec.md, plan.md y tasks.md. Comprueba cambios locales y conserva los míos.
Implementa en pasos pequeños reutilizando la base. Añade/ajusta las pruebas pertinentes, verifica permisos en servidor y no amplíes el alcance.
Si aparece una decisión crítica nueva, contradicción o migración con efectos no acordados, explica el bloqueo antes de asumirlo. No repitas preguntas ya resueltas.
Registra lo realmente ejecutado en tareas y validación; actualiza documentos que hayan cambiado y docs/ESTADO_PROYECTO.md.
No uses datos reales, despliegues, hagas commit/push o modifiques producción por esta autorización.
Entrega cambios, resultados de pruebas, pendientes y siguiente paso.
```
