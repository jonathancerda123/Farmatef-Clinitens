# Guías SDD — CliniTENS

Estas guías usan el contexto real en [AGENTS](../AGENTS.md), [arquitectura](../docs/ARQUITECTURA_BASE.md) y [estado](../docs/ESTADO_PROYECTO.md). Para un pedido nuevo se puede usar el coordinador o las fases por separado. Leer un prompt no autoriza código ni crea agentes paralelos.

| Guía | Uso |
|---|---|
| [00-orquestador](00-orquestador.md) | Seleccionar fases dentro del alcance solicitado |
| [01-especificar](01-especificar.md) | Resultado, datos, permisos y aceptación |
| [02-planificar](02-planificar.md) | Integración en archivos reales y pruebas propuestas |
| [03-tareas](03-tareas.md) | Pasos verificables vinculados a RF |
| [04-implementar](04-implementar.md) | Código solo con autorización explícita |
| [05-validar](05-validar.md) | Evidencia en entorno ficticio/aislado |
| [06-cambios](06-cambios.md) | Modificación o error, sin justificar defectos con reglas inventadas |
| [07-retomar-pausar](07-retomar-pausar.md) | Continuar la fase autorizada preservando archivos |

Apps reales: UsuarioApp, homeApp, CliniTensDocenteApp y CliniTensFichaApp; theme integra Tailwind 4 (actualización autorizada en 004). core/settings.py configura operación; core/test_settings.py aísla pruebas sin .env/base recibida. Consultar [entorno](../docs/ENTORNO_Y_VERIFICACION.md) antes de ejecutar comandos.

La [spec 001](../specs/001-linea-base-clinitens/spec.md) es documental. El siguiente número libre es 002, sujeto a comprobar el índice. Los campos `<...>` son datos del próximo pedido; no trabajo aprobado. El [manual](../MANUAL_SDD.md) muestra cómo revisar y autorizar un cambio futuro. Las [observaciones](../docs/OBSERVACIONES_PROYECTO.md) no se corrigen solo por leerlas.
