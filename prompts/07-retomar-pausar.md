# Pausar o retomar sin reconstruir

Contexto CliniTENS: leer [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md), [observaciones](../docs/OBSERVACIONES_PROYECTO.md) y [estado](../docs/ESTADO_PROYECTO.md). Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). Configuración normal core/settings.py y pruebas independientes core/test_settings.py. Política 002: MANAGER por autor, ADMIN/superusuario global; ficha estudiantil propia, matrícula si código tiene curso. Proteger superusuarios por atributo. La spec 001 es documental/histórica; 002 fue implementada por autorización explícita. No ampliar alcance sin pedido.


Puedes pedir a la IA que lea este archivo en el proyecto. Si copias el mensaje, reemplaza los campos entre <...>. Los nombres/IDs de ejemplo no son trabajo autorizado.

```text
Modo: <PAUSAR o RETOMAR>.

PAUSAR:
Guarda en tasks.md y docs/ESTADO_PROYECTO.md fase autorizada, módulo/spec/tarea activa, cambios realmente guardados, trabajo del usuario a preservar, comandos/resultados, pendientes, bloqueos y próximo paso seguro. No secretos, no datos reales, no commit/push. No marques lo no verificado.

RETOMAR:
Lee AGENTS.md, estado, spec/plan/tareas activas. Comprueba archivos y cambios locales antes de continuar.
Respeta la fase y tareas ya autorizadas; si DOCUMENTAR, no programes. Si no hay tarea activa o no consta autorización de código, informa el estado sin iniciar un módulo.
No reconstruyas trabajo terminado ni repitas la entrevista. Señala discrepancias entre el estado escrito y los archivos, y actualiza el punto de continuación.

En ambos casos, devuelve un resumen breve y verificable.
```
