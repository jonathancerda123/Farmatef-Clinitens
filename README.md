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

FarmaTEF inició su primer incremento: el personal docente puede registrar medicamentos y lotes simulados, consultar existencias y ver alertas calculadas por stock mínimo/vencimiento. Recetas, dispensación, etiquetas, comprobantes y el acceso de práctica estudiantil siguen pendientes. Kardex y laboratorio independiente también permanecen como trabajo futuro.

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
| FarmaTEFApp/ | Inventario docente inicial de medicamentos y lotes; sin receta/dispensación aún |
| templates/, theme/, static/ | Django, Tailwind 4 y recursos locales |
| docs/, specs/, prompts/ | Contexto, trazabilidad y flujo SDD |

**Entorno de esta sesión:** dependencias nuevas instaladas en `.test-artifacts/dependencias-004/target`; `.venv` original conservado con versiones anteriores. Usar el intérprete nuevo para revisar con datos ficticios. Antes de ejecutar la aplicación normal, instalar requirements actuales en un entorno con runtime parcheado y revisar migraciones de proveedores sobre copia respaldada. No se alteró la base recibida. [Comandos y recuperación](docs/ENTORNO_Y_VERIFICACION.md).

## Verificación

La línea base 004 registró 47 pruebas Django y 4 JavaScript, check/dry-run/pip check/build e integración con datos ficticios. El nuevo incremento 005 aún no se ha validado: el ejecutable Python del target referenciado en la documentación no arranca en este equipo y apunta a una instalación inexistente; no se ejecutaron pruebas para este cambio. [Inventario completo](docs/INVENTARIO_DEPENDENCIAS.md). Evidencia y límites en [VERIFICACION](docs/VERIFICACION.md), [observaciones](docs/OBSERVACIONES_PROYECTO.md) y [estado](docs/ESTADO_PROYECTO.md).

Migraciones de 002 incluidas; SQLite, medios y secretos ignorados. Retirar base/medios del índice conserva archivos locales y no purga versiones históricas. 003 no cambia persistencia ni dependencias y no se desplegó ni se hizo commit/push durante el rediseño.

Leer [AGENTS](AGENTS.md), [proyecto](docs/PROYECTO.md), [arquitectura](docs/ARQUITECTURA_BASE.md), [manual SDD](MANUAL_SDD.md) e [índice de specs](specs/README.md). Un alcance nuevo comienza con documentación y autorización explícita.
