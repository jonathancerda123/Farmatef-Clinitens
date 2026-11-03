# Verificación actual — actualización 004, 2026-10-08

Base main/e56913c inicialmente limpia; actualización autorizada. [Informe global](VALIDACION_PREPRODUCCION.md), [inventario](INVENTARIO_DEPENDENCIAS.md) y [validación 004](../specs/004-actualizacion-dependencias/validation.md).

| Control 004 | Resultado |
|---|---|
| Suite Django / JS | 47 / 4 aprobadas, cero fallidas/omitidas; Django 0.541 s |
| Check / dry-run / pip check | Exit 0; sin incidencias ni cambios de modelos |
| Build integrado | Tailwind 4.3.3, exit 0/131 ms; utilidades verificadas |
| Auditorías | 54 pins Python y lock npm tema: cero avisos conocidos; bundle editor un aviso distinto moderado separado |
| Autenticación normal replicada | 13 controles: login usuario/correo, CSRF/cookies/Argon2/sesiones, signup cerrado, reset/TOTP/Axes/cabeceras |
| Migración | Base vacía/copia de fixture previa correctas; cinco usuarios/dos fichas preservados, siete migraciones proveedor |
| UI / exportaciones | Escritorio/tablet/móvil, caso y borrador guardados, SVG/Escape; PDF dos páginas revisadas, Excel literal actual |
| Entorno / límites | Target actualizado, .venv previa preservada. Runtime parcheado, editor y operación pendientes; sin datos reales/despliegue/commit/push |

**Con bloqueadores para producción con Python 3.12.0 actual**, más evidencia operativa insuficiente. Detalle y criterio de cierre en PRE-005 a PRE-009 del informe. No aceptación humana automática.

---

# Registro histórico — rediseño 003, 2026-10-08

Rediseño solicitado implementado sobre f6e60fc; evidencia, auditoría y límites en [validación 003](../specs/003-redisenio-integral/validation.md). Correcciones de 002 conservadas; sus exportaciones/resultados anteriores permanecen en el registro histórico de abajo.

| Control 003 | Resultado |
|---|---|
| Django con core.test_settings | 47 aprobadas, 0.635 s; base ficticia |
| JS/build y sintaxis del script visual | 3 aprobadas; node --check correcto |
| Check / migraciones dry-run | Sin incidencias / No changes detected |
| Tailwind 3 | Build correcto, último 513 ms; ninguna dependencia nueva |
| Sintaxis / templates | 75 Python de apps/core/theme y 91 HTML sin errores |
| Renderizado por roles | 27 GET correctos y un H1; dos accesos directos denegados; formulario inválido conserva valores/errores |
| Navegador | Inicio/acceso/docente/ficha/rúbrica/cuentas; 1280–1440, 768 y 390 px; Escape/foco y guardado de borrador |
| Contraste | Cinco pares medidos, ratios 5.30 a 12.85; sin certificación global |
| Documentos / Git | 41 Markdown, 163 enlaces locales/fences correctos; diff sin errores |
| Operación | Servidor/tab temporales cerrados; no persistencia/dependencias nuevas, migración recibida ni despliegue |
| Pendiente previo | OBS-024 y preparación operativa de 002; aceptación humana visual/pedagógica |

La [guía visual](PERSONALIZACION_VISUAL.md) identifica tokens, bases, controles y recuperación. No se leyeron datos recibidos/secretos ni se hizo commit/push durante 003. Los siguientes resultados son históricos y no amplían lo probado en este rediseño.

---

# Registro de correcciones — spec 002, 2026-10-08

Correcciones autorizadas OBS-001 a OBS-023 implementadas localmente. Resultados detallados, entorno, comandos y límites en [validación de spec 002](../specs/002-correcciones-observaciones/validation.md).

| Control actual | Resultado |
|---|---|
| Suite Django con core.test_settings | 47 pruebas aprobadas, datos ficticios |
| Regresiones JavaScript/build | 3 pruebas aprobadas |
| Check / dry-run de migraciones / pip check | Sin incidencias / sin diferencias / dependencias consistentes |
| Tailwind 3 | Build correcto; conserva CSS anterior si falla |
| Sintaxis y plantillas | 77 Python y 85 HTML sin errores |
| Documentación | 36 Markdown, enlaces locales y fences sin errores |
| Git | Diff sin errores; migraciones incluidas; base/medios fuera del índice y conservados localmente |
| Navegador / PDF / Excel | Flujos ficticios y exportaciones revisados visualmente |
| Dependencias npm | 8 avisos restantes de build: nueva OBS-024 pendiente |

El servidor de revisión temporal se detuvo al cierre. No se leyeron datos recibidos/secretos ni se migró producción, hizo commit/push o purgó historial. Aceptación humana y preparación operativa pendientes; consultar [recuperación](ENTORNO_Y_VERIFICACION.md).

---

# Registro histórico de spec 001

Lo siguiente corresponde exclusivamente al escaneo documental del 2026-10-07. Sus cero tests y verificaciones no ejecutadas no describen el estado después de la implementación 002.

# Verificaciones realizadas — CliniTENS

2026-10-07, PowerShell, Python 3.12.0 de .venv, Django 5.1.2; rama main, commit 4126cc7. Scripts de inspección efímeros enviados por stdin, sin nuevos archivos Python. Detalle del aislamiento en [entorno](ENTORNO_Y_VERIFICACION.md).

| Comando / método ejecutado | Resultado real | Límite |
|---|---|---|
| `git status --short`, `git branch --show-current`, `git log -5 --format='%h %s'`, `git ls-files` | Rama/commit e inventario; RAR eliminado, Markdown sin seguimiento; base/medios versionados | No lectura de datos ni historial del RAR |
| `rg --files` con exclusiones y lecturas selectivas de fuentes | Inventario de módulos, plantillas, configuración, documentos y dependencias | Sin .env, registros SQLite, medios ni credenciales |
| `git check-ignore UsuarioApp/migrations/0001_initial.py CliniTensDocenteApp/migrations/0005_curso.py CliniTensFichaApp/migrations/0002_fichaclinica_evaluacion_rubrica_and_more.py` | Tres rutas ignoradas; regla migrations/ confirmada | Migraciones están en equipo local, no en Git |
| `.\.venv\Scripts\python.exe -m pip check` | No broken requirements found | No auditoría de vulnerabilidades ni instalación limpia |
| AST selectivo de settings e importlib.metadata | Config única, SQLite, zona y versiones confirmadas; valores sensibles omitidos | No carga de .env; no estado productivo |
| `call_command('check')` con configuración aislada | System check identified no issues (0 silenced) | No check de despliegue ni prueba de permisos |
| `call_command('makemigrations', check=True, dry_run=True)` aislado | No changes detected | Coincide con migraciones locales; no compara esquema de base recibida |
| `call_command('test', 'homeApp', 'UsuarioApp', 'CliniTensDocenteApp', 'CliniTensFichaApp', verbosity=1, interactive=False)` aislado | Found 0 tests; Ran 0 tests; NO TESTS RAN | **No hay suite funcional aprobada** |
| ast.parse de Python fuera de .venv/.git/node_modules/__pycache__ | 58 archivos, cero errores | Incluye migraciones locales; solo sintaxis |
| get_template de HTML en templates/ y theme/templates/ con DB/media aislados | 85 plantillas, cero errores | Compilación sin render de páginas; no comprueba todos los includes dinámicos |
| Get-Command node,npm; Test-Path theme/static_src/node_modules | Herramientas y directorio presentes | Versiones/build/consistencia lockfile no verificados |
| Comprobador efímero con pathlib/re: Markdown de raíz/docs/prompts/specs, enlaces relativos y equilibrio de fences | 32 Markdown y 101 enlaces locales, sin errores | No evalúa presentación visual de Markdown ni enlaces externos |
| `git diff --name-only`, `git ls-files --others --exclude-standard`, `git diff --check` al cierre | Solo eliminación previa del RAR entre seguidos; 32 Markdown sin seguimiento; ningún archivo nuevo de otro tipo; sin errores de diff seguidos | Los Markdown son locales sin versión original en Git; revisados aparte |

## No ejecutado

Instalación de dependencias, build CSS, runserver/navegador, pruebas de acceso directo, reproducción de riesgos, concurrencia, exportación/renderizado PDF/Excel, migraciones aplicadas, lectura de base/medios, despliegue, commit y push.

La validación documental y revisión final de enlaces se registran en [VALIDACION_SDD.md](VALIDACION_SDD.md). Check y sintaxis no demuestran seguridad, usabilidad ni aceptación.
