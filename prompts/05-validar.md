# Validar con evidencia

Contexto CliniTENS: leer [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md), [observaciones](../docs/OBSERVACIONES_PROYECTO.md) y [estado](../docs/ESTADO_PROYECTO.md). Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). Configuración normal core/settings.py y pruebas independientes core/test_settings.py. Política 002: MANAGER por autor, ADMIN/superusuario global; ficha estudiantil propia, matrícula si código tiene curso. Proteger superusuarios por atributo. La spec 001 es documental/histórica; 002 fue implementada por autorización explícita. No ampliar alcance sin pedido.


Puedes pedir a la IA que lea este archivo en el proyecto. Si copias el mensaje, reemplaza los campos entre <...>. Los nombres/IDs de ejemplo no son trabajo autorizado.

```text
Valida <carpeta de spec> contra spec, plan, tareas y código.
Esta fase autoriza comprobaciones en entorno aislado y actualización documental; no correcciones funcionales automáticas.

Lee docs/ENTORNO_Y_VERIFICACION.md; no uses db.sqlite3 ni media recibidos y usa core.test_settings independiente. Revisa RF uno por uno; ejecuta pruebas pertinentes y registra resultados reales, incluyendo casos denegados y límites. Distingue fallos previos de nuevos.
Si hay interfaz interactiva, verifica navegador; si se modifican reportes/exportaciones, verifica el contenido y representación que corresponda.
No declares tests pasados si no se ejecutaron ni cobertura por encontrar cero tests.
Crea/actualiza validation.md usando su plantilla, tareas, trazabilidad y estado. Señala qué no se pudo comprobar y por qué.
No marques mi aceptación funcional ni despliegues. Propón tareas documentadas para hallazgos que necesiten corrección.
```
