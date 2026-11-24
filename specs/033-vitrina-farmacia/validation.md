# Validación — 033

2026-11-19. Fase: implementación autorizada y comprobada localmente; sin commit. Aceptación de integración pendiente. Python 3.11.1 y Django 5.2.18 desde `.venv`; target indicado en AGENTS ausente. `core.test_settings` independiente, SQLite en memoria para suite; fixture nueva exclusiva para navegador.

| RF | Evidencia ejecutada | Resultado y límite |
|---|---|---|
| 01 | `test_vista_solo_lectura_y_stock_actual_tras_dispensar` y navegador desde Ver resultado → Ver inventario en la vitrina | Enlace contextual preselecciona curso/creador. POST 405, GET no descuenta; dispensación real de prueba consume 3 y consulta devuelve 0. |
| 02,05 | `test_ambito_stock_vigente_y_json_permitido`, `test_url_directa_curso_docente_y_parametros_ajenos`, `test_inventarios_separados_y_matricula_revocada` | Hoy incluido; vencido excluido; catálogo ajeno/inactivo fuera; inventarios separados; colaborador sin recetas no publica catálogo; anónimo login, cargos distintos 404, inactivo sin acceso; revocar matrícula invalida URL. |
| 02,03 | `test_sin_cursos_sin_recetas_y_sin_medicamentos`, `test_orden_espanol_ceros_y_distribucion_sin_perder_registros` | Vacíos diferenciados; orden Á/N/Ñ/O; 506 registros únicos repartidos en 140 espacios, 505 sin stock. Cambios de stock no redistribuyen ubicaciones. |
| 04,05 | `test_json_y_fallback_no_interpretan_html` | Cadena con cierre de script/img escapada; JSON con lista de campos permitidos; tabla alternativa en HTML. No se interpreta HTML desde JS (usa textContent). |
| 03,04 | `node --test static/js/vitrina.test.cjs` | Límites de móviles y paginado de 11 productos sin omisiones, dos pruebas correctas. No prueba física de arrastre. |
| 01,03,04 | Navegador IAB/Chromium, QA 8033, login alumno ficticio, navegación y receta dispensada | Dos muebles por vista, cambio de pareja, un H1, 363 productos, 8 columnas móviles. Agotado con X y detalle; movimiento por clic y ArrowLeft; fondo con `inert`/aria-hidden. |
| 04 | Viewports 1280, 768, 390 | Sin desbordamiento horizontal; fondo/tipografía/botones compartidos. A 390 los muebles se apilan. Capturas observadas en escritorio y móvil; en 768 se midió estructura/desbordamiento. |

## Comandos y resultados

Desde la raíz del repositorio:

```powershell
.venv/Scripts/python.exe manage.py check --settings=core.test_settings
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run --settings=core.test_settings
.venv/Scripts/python.exe manage.py test FarmaTEFApp.tests_vitrina --settings=core.test_settings
.venv/Scripts/python.exe manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp CliniTensSimulacionApp --settings=core.test_settings
node --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs static/js/vitrina.test.cjs
node theme/static_src/build.cjs
```

Check sin incidencias, sin cambios de migraciones, siete pruebas nuevas correctas; suite completa: 102 descubiertas, 101 correctas y una omitida por requerir PostgreSQL. Seis pruebas JS correctas; Tailwind 4.3.3 compilado. No auditoría de dependencias ni pruebas de carga.

## Navegador y aislamiento

La primera ejecución del servidor QA falló por un argumento `insecure` no admitido por `StaticFilesHandler`; se corrigió solo el script ficticio ignorado. El aislamiento bloqueó sockets y el primer navegador no conectó. Tras la autorización de ejecución fuera del aislamiento, el servidor enlazado exclusivamente a 127.0.0.1:8033 funcionó y permitió la revisión indicada. No fue un error de la vista del producto.

Datos QA: `.test-artifacts/vitrina033-qa.sqlite3`, creada desde cero con migraciones y usuarios ficticios; catálogo documental de prueba de 363 registros y una receta dispensada por el servicio. Script ignorado `.test-artifacts/vitrina033_demo.py`. No se consultó ni modificó 8025 ni la base habitual. Configuración normal y .env intactos.

## Límites y recuperación

Sin migraciones de 033 ni dependencia nueva. Retirar solo sus rutas/enlaces/archivos y recompilar revierte la integración sin restaurar bases. La consulta es una foto del stock al cargar; Actualizar es explícito. El stock puede cambiar por otras dispensaciones. Altas/bajas de catálogo pueden redistribuir espacios; no son ubicaciones físicas persistidas.

Pendientes: arrastre real con mouse/táctil, emulación de movimiento reducido (regla CSS incluida), zoom 200 %, otros motores, revisión con lector de pantalla, volumen de catálogo mayor que la fixture en navegador y aceptación de docente/usuaria. La paginación por compartimento se probó en lógica; no en navegador. La tabla sin JS se comprobó en respuesta HTML, sin sesión de navegador con JS desactivado. No se afirma preparación para producción.
