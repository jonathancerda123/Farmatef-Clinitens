# Validación — 034

2026-11-19. Rama `valentina`. Entorno ficticio con `core.test_settings`, SQLite en memoria y medios temporales. El target indicado en AGENTS.md no está disponible; se verificó y usó `.venv/Scripts/python.exe`: Python 3.11.1, Django 5.2.18 y allauth 65.19.7. Esta comprobación funcional no certifica el runtime para producción.

| Requisito | Verificación | Resultado |
|---|---|---|
| 01 | Choices, docentes existentes y migración inversa en `tests_migracion_areas.py`. | Correcto; MANAGER anteriores reciben Ambos y otros perfiles conservan sus campos. |
| 02 | Creación/edición, cargo protegido, otro superusuario y POST de perfil en `tests_areas.py`. | Correcto; área exigida para docentes, valores inválidos rechazados y cambio solo administrativo. |
| 03/04 | Matriz de áreas, roles y rutas directas, incluidos GET/POST/PDF/medios. | Correcto; Farmacia/Enfermería/Ambos, administrador y superusuario sin perfil. Cambio en la siguiente petición, categoría vacía denegada y estudiantes sin regresión. |
| 05 | Gestión de cursos por propietario y colaboración por área. | Correcto; sin acceso a cursos ajenos. Colaborador reclasificado conserva su vínculo histórico y pierde acceso a recetas. |

Comandos ejecutados desde la raíz:

```powershell
.venv/Scripts/python.exe manage.py test UsuarioApp.tests_areas UsuarioApp.tests_migracion_areas --settings=core.test_settings
.venv/Scripts/python.exe manage.py check --settings=core.test_settings
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run --settings=core.test_settings
.venv/Scripts/python.exe manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp CliniTensSimulacionApp --settings=core.test_settings
node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs static/js/vitrina.test.cjs
.venv/Scripts/python.exe manage.py tailwind --settings=core.test_settings build
```

La primera ejecución de las 17 pruebas nuevas detectó una expectativa incorrecta del test: el formulario de colaboración inválido redirige al detalle con mensaje, en vez de responder 200. Se corrigió la aserción y se conservó la comprobación de que no se agrega el colaborador. Suite completa posterior: **119 pruebas, 118 correctas y una omitida por requerir PostgreSQL**. Incluye las 17 regresiones nuevas y el trabajo local de vitrina 033. Las seis pruebas JavaScript pasaron; check sin incidencias, sin migraciones pendientes de generar y build correcto.

Revisión visual en Edge a 1536×816: portadas de Farmacia/Enfermería muestran únicamente su área y Ambos muestra las dos; navegación coherente y cursos conservados. Formulario de creación oculta la categoría inicialmente, la muestra al elegir Docente y ofrece Farmacia/Enfermería/Ambos. Formulario administrativo muestra categoría vigente, ayuda y acciones. Se usaron respuestas Django renderizadas con datos sintéticos en memoria, exportadas a `.test-artifacts/areas034-qa`; no datos reales. El navegador integrado y Edge no conectaron al servidor de revisión HTTP 8034 (timeout); se revisaron los HTML y recursos locales en Edge. Guardado/denegaciones se verificaron mediante Django Client, no mediante envío del formulario en navegador. Revisión móvil y flujo HTTP completo en navegador pendientes.

Tras completar las pruebas, la usuaria autorizó expresamente respaldar y aplicar la migración a la base local. Respaldo consistente mediante SQLite backup API, con origen en lectura, en `.test-artifacts/areas034/db.sqlite3.before-areas034-20261119T052603Z` (811008 bytes, `quick_check=ok`; SHA-256 en `respaldo.json`, ignorado). No se inspeccionaron filas ni credenciales, `.env` o medios reales. Se usó `core.local_runtime`, que omite `.env`, y el plan contenía únicamente `UsuarioApp.0004_profile_area_docente_and_more`.

```powershell
.venv/Scripts/python.exe manage.py migrate UsuarioApp 0004 --plan --settings=core.local_runtime
.venv/Scripts/python.exe manage.py migrate UsuarioApp 0004 --settings=core.local_runtime
.venv/Scripts/python.exe manage.py showmigrations UsuarioApp --settings=core.local_runtime
.venv/Scripts/python.exe manage.py check --settings=core.local_runtime
```

Aplicación correcta, 0001–0004 marcadas `[X]`, check sin incidencias y `PRAGMA quick_check` posterior de la base local en lectura devuelve `ok`. La revisión de diferencias pasó con `core.whitespace=cr-at-eol`, respetando los finales CRLF de esta copia. No despliegue, commit ni push. Se conservan los cambios locales anteriores de vitrina, documentos, diagramas y recursos. Próximo paso: revisión de la usuaria/docente y clasificación administrativa de docentes que deban tener una sola área. Aceptación funcional final pendiente.
