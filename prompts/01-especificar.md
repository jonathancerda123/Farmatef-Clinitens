# Especificar el resultado

Contexto CliniTENS: leer [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md), [observaciones](../docs/OBSERVACIONES_PROYECTO.md) y [estado](../docs/ESTADO_PROYECTO.md). Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). Configuración normal core/settings.py y pruebas independientes core/test_settings.py. Política 002: MANAGER por autor, ADMIN/superusuario global; ficha estudiantil propia, matrícula si código tiene curso. Proteger superusuarios por atributo. La spec 001 es documental/histórica; 002 fue implementada por autorización explícita. No ampliar alcance sin pedido.


Puedes pedir a la IA que lea este archivo en el proyecto. Si copias el mensaje, reemplaza los campos entre <...>. Los nombres/IDs de ejemplo no son trabajo autorizado.

```text
Nombre del módulo: <área de CliniTENS o cambio propuesto>.
Requerimiento: <texto y ejemplos>.

Fase DOCUMENTAR. Lee reglas, estado, decisiones y código relacionado.
Usa specs/_templates/spec.md para redactar qué debe hacer: actores, alcance/exclusiones, datos, RF identificados, permisos por acción, casos límite, criterios observables y regresiones a preservar.
Incluye la política de superusuario real de esta base y cualquier excepción explícitamente solicitada; no copies la de otro proyecto.
Para módulo nuevo usa siguiente número libre; un ajuste pequeño actualiza su spec.
Conserva lo que esté claro. Si falta una decisión crítica, identifica la parte afectada y pregunta solo eso. No inventes aprobación, requisitos comerciales ni funcionalidades futuras.
Actualiza el índice y estado pertinente. No generes código. Entrega la spec para revisión o para continuar con el plan si esa fase documental también está pedida.
```
