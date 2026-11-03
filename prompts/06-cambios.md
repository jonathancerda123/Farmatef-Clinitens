# Documentar un cambio o error

Contexto CliniTENS: leer [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md), [observaciones](../docs/OBSERVACIONES_PROYECTO.md) y [estado](../docs/ESTADO_PROYECTO.md). Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). Configuración normal core/settings.py y pruebas independientes core/test_settings.py. Política 002: MANAGER por autor, ADMIN/superusuario global; ficha estudiantil propia, matrícula si código tiene curso. Proteger superusuarios por atributo. La spec 001 es documental/histórica; 002 fue implementada por autorización explícita. No ampliar alcance sin pedido.


Puedes pedir a la IA que lea este archivo en el proyecto. Si copias el mensaje, reemplaza los campos entre <...>. Los nombres/IDs de ejemplo no son trabajo autorizado.

```text
Módulo afectado: <área de CliniTENS o cambio propuesto>.
Cambio o error: <descripción y ejemplo reproducible>.
Resultado esperado: <qué debería ocurrir>.
Fase DOCUMENTAR: no código todavía.

Lee la spec vigente y el comportamiento real. Si es error, distingue requisito incumplido de una regla nueva; no cambies la spec para justificar un bug.
Si cambia un acuerdo, registra qué decisión sustituye y conserva su antecedente.
Un ajuste pequeño actualiza spec/plan/tareas y añade registro fechado; un módulo nuevo/cambio transversal usa siguiente carpeta libre. No ejecutes ideas del roadmap o de otros clientes.
Identifica efectos sobre permisos, datos, UI, pruebas y docs; no hagas una entrevista por rutina.
Entrega documentos actualizados y pendientes críticos. Detente para revisión e instrucción posterior de implementación.
```
