# Manual SDD — CliniTENS

Este flujo usa la estructura real de CliniTENS: Django 5.2.18 LTS, core/settings.py, cuatro apps, usuario Django con Profile/Position y Tailwind 4.3.3. Contexto en [arquitectura](docs/ARQUITECTURA_BASE.md), comandos y aislamiento en [entorno](docs/ENTORNO_Y_VERIFICACION.md).

## Punto de partida

La [spec 001](specs/001-linea-base-clinitens/spec.md) registra el escaneo y adaptación documental. No es permiso para corregir hallazgos ni una aprobación retrospectiva de toda la aplicación. La [spec 002](specs/002-correcciones-observaciones/spec.md) registra correcciones autorizadas/verificadas. El [informe](docs/OBSERVACIONES_PROYECTO.md) reúne estado y límites; el [estado](docs/ESTADO_PROYECTO.md) permite retomar.

Para una solicitud futura, indicar área y resultado esperado. No hace falta inventar una app: gestión docente pertenece a CliniTensDocenteApp, ficha a CliniTensFichaApp, cuentas a UsuarioApp y portadas a homeApp. El plan justificará una app nueva solo cuando corresponda.

## Documentar antes de implementar

Se puede usar [00-orquestador](prompts/00-orquestador.md) para coordinar spec → plan → tasks, o las guías 01/02/03 por separado. Leer una guía no concede permisos.

Ejemplo de pedido futuro, **no autorizado por este manual**:

```text
Área: CliniTensFichaApp.
Quiero definir validación de campos y condiciones para enviar una ficha.
Conserva las 13 secciones y los estados actuales.
Primero analiza OBS-007 y el código; documenta alternativas y decisiones pendientes.
Fase DOCUMENTAR: sin código, migraciones ni pruebas persistentes.
Lee AGENTS y prompts/00-orquestador. Crea spec/plan/tareas en el siguiente número libre.
```

La siguiente spec libre tras 002 es 003, pero debe comprobarse el índice al usarla. El ejemplo no fija campos obligatorios ni decide quién puede ver datos: esas reglas deben explicitarse en el pedido/spec.

## Documentos de cada cambio

| Archivo | Contenido |
|---|---|
| spec.md | Problema, actores, alcance, datos/reglas, permisos por acción, RF y aceptación observable |
| plan.md | Integración en rutas/archivos reales, contratos, servidor, migraciones/reversión y pruebas propuestas |
| tasks.md | Pasos pequeños, ID, RF, dependencias y condición de terminado |
| validation.md | Resultados ejecutados, fallos y límites; no evidencia inventada |

Las tareas de código empiezan sin marcar y requieren autorización explícita. Si el alcance es solo documental, se marcan únicamente tareas documentales efectivamente completadas. Fuentes observadas, propuesta y aprobación son estados distintos.

## Revisar y autorizar

Primero revisar reglas de negocio/permisos y después plan/tareas. Para cambiar documentos, pedirlo manteniendo DOCUMENTAR. Cuando se acuerde una spec funcional futura, la autorización puede ser:

```text
Revisé la spec de [ruta real]. Autorizo implementar [IDs de tareas / alcance definido].
Conserva mis cambios locales y usa prompts/04-implementar.
Prueba con datos ficticios; registra resultados y actualiza documentación.
No despliegues, migres producción ni hagas commit/push.
```

La autorización debe referirse a la spec funcional elegida; las tareas de 001 son documentales. No hace falta pedir permiso otra vez para cada edición ya incluida en una implementación autorizada.

## Precauciones concretas de esta base

- core.test_settings independiente y fixtures: no cargar base/media/.env recibidos.
- Migraciones incluidas; aplicación a base existente requiere respaldo/autorización. Base/media retirados del índice, historia previa no purgada.
- Política confirmada: MANAGER por autor, ADMIN/superusuario global; root protegido. Matrícula si código tiene curso, docente responsable.
- Ficha: esquema estricto, versiones, completitud/No aplica; rúbrica con borrador separado/publicación atómica.
- Medios privados, HTML sanitizado, uploads validados, credenciales efímeras. Revisar proxy/correo/caché para despliegue.
- Tailwind 4 autorizado/implementado en 004, @source explícitos y config JS de compatibilidad. OBS-024 resuelta en lock del tema; revisar inventario e informe preproducción para el bundle CKEditor y pendientes de runtime/operación. Las actualizaciones futuras requieren alcance autorizado.
- Ver [entorno y recuperación](docs/ENTORNO_Y_VERIFICACION.md) antes de comandos normales.

## Validar y retomar

Usar [05-validar](prompts/05-validar.md) para comparar RF con evidencia. Permisos requieren intentos de acceso directo, UI requiere navegador/teclado/móvil y exportaciones revisión visual cuando correspondan. Cero tests significa cero tests; no aprobación funcional.

Para un error usar [06-cambios](prompts/06-cambios.md), registrar reproducción y regresión propuesta. Para pausa/reanudación usar [07-retomar-pausar](prompts/07-retomar-pausar.md) y mantener ESTADO/tareas con fase autorizada, cambios guardados, comandos y próximo paso. No reconstruir trabajo terminado ni asumir autorización por ver una tarea en roadmap.
