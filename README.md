# CliniTENS

Plataforma Django de simulación clínica y registro electrónico para la formación de Técnicos en Enfermería.

Para trabajar desde varios equipos, consultar la [guía de colaboración con GitHub](docs/COLABORACION_GITHUB.md). Cada equipo usa su propia copia y entorno; los cambios se comparten mediante ramas y pull requests.

## Estado actual

La [spec 001](specs/001-linea-base-clinitens/spec.md) conserva el escaneo del 2026-10-07. La [spec 002](specs/002-correcciones-observaciones/spec.md) implementa las correcciones autorizadas del 2026-10-08. La [spec 003](specs/003-redisenio-integral/spec.md) unifica el diseño de inicio, módulos, cuentas y acceso, con prioridad escritorio y adaptación móvil. La [spec 004](specs/004-actualizacion-dependencias/spec.md) actualiza bibliotecas/Tailwind y aporta [revisión preproducción](docs/VALIDACION_PREPRODUCCION.md). Las migraciones de 002 **no se aplicaron a la base recibida**; revisar [entorno y recuperación](docs/ENTORNO_Y_VERIFICACION.md) antes de ejecutar la aplicación normal.

- MANAGER gestiona sus casos, códigos, pacientes, resultados y cursos. ADMIN y superusuario activos tienen acceso global. Las cuentas superusuario se protegen por atributo, sin depender de IDs.
- Código con curso exige matrícula; sin curso conserva acceso abierto por actividad. El docente corresponde al responsable del código.
- Ficha de 13 secciones: borradores parciales; envío con identificación y otras doce secciones completas o «No aplica». Versiones detectan guardados obsoletos.
- Rúbrica de 15 indicadores: borrador independiente y publicación completa con nota/retroalimentación consistentes.
- Resultados publicados o habilitados disponibles al estudiante; medios y PDF con autorización en servidor.
- Excel valida identidad y crea cuentas por transacción. Credenciales entregadas una vez, durante diez minutos; contraseña inicial caduca a las 24 horas y obliga cambio.
- Seguimiento cada 30 segundos en pestaña visible, actividad y métricas reales. Portadas distinguen módulos pendientes.

FarmaTEF permite gestionar inventario y lotes simulados, asignar recetas a cursos, consultar historiales y practicar la decisión de dispensar o rechazar con estudiantes inscritos. El responsable del curso puede asignar docentes colaboradores para compartir solo las recetas FarmaTEF de ese curso. La clave docente no se muestra antes de la respuesta. Una dispensación válida descuenta stock FEFO atómicamente; rechazos y decisiones incorrectas no lo alteran. Las recetas sin actividad se pueden eliminar desde el historial; las que tienen respuestas o dispensaciones se conservan. Comprobantes, etiquetas y Kardex de inventario FarmaTEF siguen pendientes.

CliniTENS incorpora tres recorridos educativos vinculados a cursos: DAU con paciente SIM, signos vitales, procedimientos, cierre e historial; Laboratorio con solicitud por pasos, selección de exámenes, emisión PDF e historial por estudiante, además de una etiqueta por tubo; y Centro de Apoyo Diagnóstico con resultados ficticios de laboratorio, imágenes representadas, ECG e informes. El historial Kardex anterior se conserva como legado. Solo se usan datos ficticios; la migración 0006 se aplicó a la base local después de un respaldo verificado; revisión visual/docente pendiente. Ver [spec 014](specs/014-simuladores-clinicos/spec.md), [spec 015](specs/015-dau-flujo-visual/spec.md), [spec 016](specs/016-modulos-clinicos-separados/spec.md), [spec 017](specs/017-flujos-dau-laboratorio-cad/spec.md) y [spec 018](specs/018-flujo-laboratorio-por-pasos/spec.md).

La interfaz comparte marca, barra lateral, colores, tipografía, formularios y estados. La [guía visual](docs/PERSONALIZACION_VISUAL.md) explica cómo mantener la coherencia con Tailwind 4 y tokens centrales.

El trabajo para el Informe 2 y las fechas EF2/ES2/EVS3/EVS4 está en la [spec 005](specs/005-farmatef-mvp-informe2/spec.md). El [borrador de preinforme](docs/borradores/PREINFORME_EVS2_FARMATEF_CLINITENS_2026.md) está preparado para retroalimentación y requiere revisión antes de pasarlo a la plantilla Word.

## Tecnología y estructura

Python 3.12 evaluado, Django **5.2.18 LTS**, SQLite, allauth **65.19.7** con MFA, Axes **8.3.1**, django-tailwind **4.5.0**, Tailwind **4.3.3**, Alpine 3.17.4 y DOMPurify 3.4.16 locales; nh3 sanitiza HTML en servidor. Dependencias en [requirements](requirements.txt) y [package.json](theme/static_src/package.json).

| Ruta | Responsabilidad |
|---|---|
| core/ | Configuración normal/pruebas independientes, rutas, permisos, medios privados y mixins |
| UsuarioApp/ | Cuentas, cargos, perfiles y cambio obligatorio de contraseña |
| homeApp/ | Portadas y actividad |
| CliniTensDocenteApp/ | Catálogo, cursos, importación, rúbrica, PDF y seguimiento |
| CliniTensFichaApp/ | Ficha JSON, esquema, versiones y editor |
| FarmaTEFApp/ | Inventario, recetas simuladas, historial y dispensación parcial por lotes |
| CliniTensSimulacionApp/ | Casos educativos por curso: DAU, órdenes/tubos de laboratorio, Centro de Apoyo Diagnóstico y registros Kardex legados |
| templates/, theme/, static/ | Django, Tailwind 4 y recursos locales |
| docs/, specs/, prompts/ | Contexto, trazabilidad y flujo SDD |

**Entorno de esta sesión:** el target de dependencias documentado no arranca en este equipo; las comprobaciones se realizaron con `.venv` y `core.test_settings`. Migraciones FarmaTEF 0003–0007 están aplicadas en la base local tras respaldos específicos; la base no se comparte por Git. Antes de usar otro equipo, aplicar las migraciones allí con respaldo. No se modificó una base de producción. [Comandos y recuperación](docs/ENTORNO_Y_VERIFICACION.md).

## Verificación

La línea base 004 registró su propia suite. Para el flujo de recetas 008–012 pasaron `manage.py check`, el cotejo de migraciones y la carga de plantillas/rutas con `core.test_settings`. La migración de colaboración se aplicó a la base local tras respaldo; no se ejecutaron pruebas funcionales ni revisión de navegador. [Inventario completo](docs/INVENTARIO_DEPENDENCIAS.md). Evidencia y límites en [VERIFICACION](docs/VERIFICACION.md), [observaciones](docs/OBSERVACIONES_PROYECTO.md) y [estado](docs/ESTADO_PROYECTO.md).

Migraciones de 002 incluidas; SQLite, medios y secretos ignorados. Retirar base/medios del índice conserva archivos locales y no purga versiones históricas. 003 no cambia persistencia ni dependencias y no se desplegó ni se hizo commit/push durante el rediseño.

Leer [AGENTS](AGENTS.md), [proyecto](docs/PROYECTO.md), [arquitectura](docs/ARQUITECTURA_BASE.md), [manual SDD](MANUAL_SDD.md) e [índice de specs](specs/README.md). Un alcance nuevo comienza con documentación y autorización explícita.
