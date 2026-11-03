# Preparar pasos verificables

Contexto CliniTENS: leer [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md), [observaciones](../docs/OBSERVACIONES_PROYECTO.md) y [estado](../docs/ESTADO_PROYECTO.md). Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). Configuración normal core/settings.py y pruebas independientes core/test_settings.py. Política 002: MANAGER por autor, ADMIN/superusuario global; ficha estudiantil propia, matrícula si código tiene curso. Proteger superusuarios por atributo. La spec 001 es documental/histórica; 002 fue implementada por autorización explícita. No ampliar alcance sin pedido.


Puedes pedir a la IA que lea este archivo en el proyecto. Si copias el mensaje, reemplaza los campos entre <...>. Los nombres/IDs de ejemplo no son trabajo autorizado.

```text
Spec y plan: <carpeta>.
Fase DOCUMENTAR.

Lee los documentos y prepara tasks.md siguiendo la plantilla.
Divide el plan en tareas pequeñas con ID, RF, dependencias, archivos previstos y condición comprobable de terminado. Incluye pruebas de reglas/permisos, regresiones y revisión visual cuando aplique.
Todas las tareas de implementación comienzan sin marcar. No escribas pruebas ejecutables ni código. Registra bloqueos sin inventar decisiones.
Actualiza trazabilidad prevista y estado. Entrega spec, plan y tareas disponibles; detente antes de implementar. No marques aceptación del usuario.
```
