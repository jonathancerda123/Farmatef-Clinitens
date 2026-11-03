# Proponer integración técnica

Contexto CliniTENS: leer [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md), [observaciones](../docs/OBSERVACIONES_PROYECTO.md) y [estado](../docs/ESTADO_PROYECTO.md). Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). Configuración normal core/settings.py y pruebas independientes core/test_settings.py. Política 002: MANAGER por autor, ADMIN/superusuario global; ficha estudiantil propia, matrícula si código tiene curso. Proteger superusuarios por atributo. La spec 001 es documental/histórica; 002 fue implementada por autorización explícita. No ampliar alcance sin pedido.


Puedes pedir a la IA que lea este archivo en el proyecto. Si copias el mensaje, reemplaza los campos entre <...>. Los nombres/IDs de ejemplo no son trabajo autorizado.

```text
Spec a trabajar: <ruta>/spec.md.
Fase DOCUMENTAR, no implementación.

Lee spec, reglas de la base y archivos existentes afectados.
Crea/actualiza plan.md con la plantilla: arquitectura propuesta, app nueva o ampliación, archivos, modelos/relaciones, validación, permisos, rutas, plantillas, transacciones/migraciones si aplican y pruebas por RF.
Distingue rutas existentes de archivos propuestos. No inventes una configuración de pruebas que la base no trae. Reutiliza autenticación, User/Profile/Position, los mixins existentes y templates/components/Layout/base.html. Para ficha usa sus estados/secciones reales; para cursos revisa consultas por creado_por.
Registra riesgos, alternativas relevantes y decisiones pendientes. Actualiza docs solo si la información lo exige, marcando propuestas como tales.
No escribas código ni ejecutes startapp, migraciones o compilaciones. Entrega el plan y continúa solo con tareas documentales si se solicitaron.
```
