# Validación — 036 / 2026-11-24

SAL-09: la usuaria solicita aplicar la distribución de su imagen a la sala del proyecto. Autorización de configuración local con lectura mínima de sala/propietario y respaldo para esta operación; no acceso a credenciales, .env, medios o contenido clínico ajeno. Conciliación, ensayo en copia, aplicación local y verificación completados; detalle al final.

Ampliación SAL-08 autorizada posteriormente por la solicitud de incluir una zona de entrada. Implementada y verificada; evidencia de esa ampliación al final, separada de la validación y activación 0011 previas. No se aplicó otra migración habitual.

Autorización: solicitud explícita de reemplazar la vitrina e incorporar configuración docente/localización al dispensar. Implementación terminada y probada con datos ficticios. Posteriormente la usuaria respondió «autorizo» al respaldo y aplicación local de 0011; activación completada y verificada. Aceptación docente pendiente. Se conservan los cambios de 034 y el trabajo simultáneo 035-demo-render-gratuita; el número de esta spec se cambió de 035 a 036 al detectar esa creación paralela.

## Entorno y comandos

Target indicado en AGENTS ausente. Se comprobó `.venv` existente: Python 3.11.1/Django 5.2.18. Node 20.15.0. Settings `core.test_settings`, SQLite en memoria para suite; sin `.env`, base habitual, medios ni credenciales reales.

```powershell
.venv/Scripts/python.exe manage.py makemigrations FarmaTEFApp --name sala_farmacia --settings=core.test_settings
.venv/Scripts/python.exe manage.py test FarmaTEFApp.tests_sala --settings=core.test_settings --noinput
.venv/Scripts/python.exe manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp CliniTensSimulacionApp --settings=core.test_settings --noinput
.venv/Scripts/python.exe manage.py check --settings=core.test_settings
.venv/Scripts/python.exe manage.py makemigrations --check --dry-run --settings=core.test_settings
.venv/Scripts/python.exe manage.py tailwind --settings=core.test_settings build
node.exe --experimental-default-type=module --test static/js/sala-modelo.test.mjs static/js/mensajes.test.cjs theme/static_src/build.test.cjs
git -c core.whitespace=cr-at-eol diff --check
```

Resultados: migración aditiva **0011_sala_farmacia** generada; **16 pruebas nuevas** correctas; **128 Django, 127 correctas y una omitida por requerir PostgreSQL**; **9 JS correctas**; check sin incidencias, sin cambios de migración por generar, build Tailwind 4.3.3 correcto. Diff sin errores de whitespace; avisos de normalización LF/CRLF en recursos previos, sin reformatearlos.

La primera suite de FarmaTEF detectó dos expectativas antiguas de redirección al resultado; se actualizaron para comprobar la entrada automática al localizador, manteniendo las comprobaciones de stock, historial y reintento. No se debilitó la validación de dispensación. Tras cambiar la extensión pública a `.js`, Node 20 requiere `--experimental-default-type=module` para interpretar esos módulos en pruebas; los `.cjs` conservan su formato. La ejecución sin ese flag falló y no se cuenta como válida.

## Matriz ejecutada

| Requisito | Resultado |
|---|---|
| SAL-01/02 | Seis tipos; medidas/posiciones/orientaciones, filas/columnas, huella con sillas y límites; alta y lectura sin creación por GET |
| SAL-03 | Asignaciones por ID, varios productos por compartimento, ubicación pendiente, stock vigente/cero y exclusión de inactivos al alumno |
| SAL-04 | Propietario/ADMIN/superusuario, docente ajeno/Enfermería/alumno denegados, CSRF; CAS, IDs/tipos/bools/duplicados, rollback, protección de reducción/borrado asignado |
| SAL-05 | GET de alumno matriculado, POST 405, inventario ajeno/colaborador sin inventario y matrícula revocada denegados; JSON seguro y tabla alternativa |
| SAL-06 | Receta multiproducto redirige a su dispensación propia; sin sala sigue consultable; rechazo conserva resultado; GET repetido sin consumo adicional y URL de otro alumno denegada |
| SAL-07 | Gráficos y vista 033 retirados; redirección antigua conservada; estilos/layout actuales, teclado y cinco pruebas de geometría JS |

No se atribuye concurrencia real a las pruebas lógicas de CAS ni rendimiento a los tests de geometría.

## Navegador y fixture

`work/sala035_qa.py` crea exclusivamente `.test-artifacts/sala035-qa.sqlite3` o, con `--browser`, `.test-artifacts/sala035-browser.sqlite3`. Se aplicó 0011 en esas bases nuevas ficticias y en memoria. Nombres internos QA035 conservados tras renumerar la spec; no son la spec de despliegue. Ninguna lectura/migración de base habitual.

Servidor dentro del entorno restringido 8035: timeout en IAB/Chrome. Se autorizó ejecutar la revisión fuera de ese entorno en **127.0.0.1:8036**, ligado a loopback y usando solo la fixture. Se reinició únicamente ese proceso de QA para recoger el cambio de extensión de scripts.

La primera carga visual detectó que Windows asigna `text/plain` a `.mjs`, bloqueando módulos. Se cambió la extensión pública de los módulos y del kit local a `.js` (`application/javascript`), sin alterar el código del kit. No se cambió configuración global MIME del sistema.

IAB real: guardado docente de sala de 10 a 11 m; asignación de Ibuprofeno SIM a Estante 2/F3-7; cambio a alumno, selección de dos lotes y confirmación de dispensación. Se verificó la redirección automática, stock actualizado a 20 u., selección de Losartán SIM y descubrimiento de Estante 3/fondo columna 2/fila 4. Flecha izquierda del módulo B ocultó el centro y dejó visible la tercera columna al terminar; enlaces ocultos protegidos. Seleccionar de nuevo un producto restaura el destino.

Revisión visual de escritorio y anchos 390/768 px; sin desbordamiento horizontal (375/375 y 753/753 px de ancho de documento disponible, descontando barra vertical). Override restaurado. Captura completa: `.test-artifacts/sala035/alumno-dispensacion.png`. Tab de revisión conservada para la usuaria con datos ficticios. No se revisaron impresión, zoom 200%, arrastre táctil real, otros motores, carga/FPS ni auditoría geométrica especializada de Anatomy.

## Activación y recuperación

La usuaria autorizó explícitamente el respaldo y aplicar únicamente 0011. `work/sala036_migracion_local.py` verifica el destino exacto `db.sqlite3`, crea respaldo mediante SQLite backup API con origen de solo lectura, comprueba integridad/hash, comprueba el plan y vuelve a validarlo antes de migrar. Usa `core.local_runtime`, que omite `.env`; su secreto se carga internamente sin imprimirlo ni inspeccionarlo. No se consultaron filas originales ni credenciales ni medios.

Respaldo: `.test-artifacts/sala036/db.sqlite3.before-sala036-20261124T162854540714Z`, **819200 bytes**, `quick_check=ok`. SHA-256: `096cce224d4d60195f721cf5bb8c4a462391fb79cb615fffe86c0d035b5c402b`. Metadatos privados/ignorados en `.test-artifacts/sala036/respaldo.json`. El plan contenía únicamente `FarmaTEFApp.0011_sala_farmacia`, sin retrocesos ni dependencias adicionales pendientes. Aplicación `OK`; tres tablas nuevas verificadas mediante introspección, integridad posterior `ok`, `showmigrations` marca 0011 `[X]` y `manage.py check` no informa incidencias.

```powershell
.venv/Scripts/python.exe work/sala036_migracion_local.py
.venv/Scripts/python.exe work/sala036_migracion_local.py --apply
.venv/Scripts/python.exe manage.py showmigrations FarmaTEFApp --settings=core.local_runtime
.venv/Scripts/python.exe manage.py check --settings=core.local_runtime
```

No se trasladaron datos de las fixtures a la base habitual. La migración no precarga muebles ni distribuye medicamentos; la sala empieza vacía y el docente configura desde FarmaTEF → Sala de farmacia. Inventario/historial anteriores no se transforman ni cambian de propietario. No se afirma una nueva revisión de navegador sobre datos originales; la revisión visual previa usó exclusivamente la fixture.

Después de uso persistente no revertir las tablas sin preservar asignaciones nuevas. Recuperar con copia y código compatibles, siguiendo `plan.md`. Sin despliegue, commit/push ni acceso a servicios externos. Aceptación pedagógica/visual del docente pendiente.

## Ampliación SAL-08 — Entrada

Se agregó Zona de entrada al selector de elementos del plano. Configurable por docente: nombre, ancho, fondo, posición y orientación. Se identifica como «Entrada» con área jade de borde discontinuo y umbral; rótulo legible limitado al borde de la sala en móvil. Máximo una por sala; no ofrece cajones, asignaciones o frontal 3D. Los alumnos la consultan en el mismo plano.

Pruebas: 18 `FarmaTEFApp.tests_sala` correctas; regresión `FarmaTEFApp UsuarioApp.tests_areas`: **59 pruebas, 58 correctas/una omitida por PostgreSQL**; **6 pruebas JS de sala** correctas; check, cotejo, build y diff correctos. Se verifican persistencia/lectura estudiantil, ausencia de compartimentos, rechazo de asignación, entrada duplicada/fuera de sala y rollback de versión. Estos conteos son los comandos de esta ampliación; no se repitió la suite completa de 128 por rutina.

```powershell
.venv/Scripts/python.exe manage.py makemigrations FarmaTEFApp --name zona_entrada --settings=core.test_settings
.venv/Scripts/python.exe manage.py sqlmigrate FarmaTEFApp 0012 --settings=core.test_settings
.venv/Scripts/python.exe manage.py test FarmaTEFApp.tests_sala --settings=core.test_settings --noinput
.venv/Scripts/python.exe manage.py test FarmaTEFApp UsuarioApp.tests_areas --settings=core.test_settings --noinput
node.exe --experimental-default-type=module --test static/js/sala-modelo.test.mjs
```

0012_zona_entrada altera únicamente choices del campo tipo. `sqlmigrate` confirma `(no-op)` en SQLite: sin nuevas columnas/tablas ni transformación de datos. Se incluye para coherencia del estado de migraciones; pendiente de aplicar en base habitual en una operación autorizada futura. La función ya usa las columnas de 0011. No se modificó la migración 0011 aplicada ni se accedió a datos habituales en esta ampliación.

IAB sobre fixture 8036 conservada con esquema 0011: el docente añadió Entrada, cambió nombre a Entrada principal, posición a X=1010/Y=700 y orientación a 90°, guardó y recargó; posición/orientación persistieron. Se cambió al alumno y se comprobó la zona en el localizador de su dispensación, sin controles docentes ni frontal al seleccionarla. Móvil 390: documento/viewport disponible 375/375 px, una zona y sin overflow; revisión a 1280 y override restaurado. Captura `.test-artifacts/sala036/entrada-plano.png`. Se reinició solo el servidor ficticio previamente autorizado para cargar el código nuevo. Arrastre táctil real y geometría de puertas físicas no evaluados.

## SAL-09 — Distribución de la imagen aplicada a la sala local

Inspección acotada mediante `work/sala036_inspeccionar_configuracion.py`: un único propietario activo de inventario habilitado para farmacia, sin sala ni ubicaciones previas. Se consultaron únicamente identidad mínima del propietario y metadatos de sala; no nombres de medicamentos, lotes, recetas, contraseñas, .env ni medios. El ID operativo queda en el manifiesto privado, no se convierte en constante del proyecto.

`work/sala036_aplicar_referencia.py` define los 13 elementos de la imagen y admite propietario/versión explícitos. Se creó respaldo consistente con SQLite backup API y origen de solo lectura; se ensayó primero sobre una copia independiente del respaldo con el servicio `guardar_sala`. El script concilia muebles por nombre/tipo preservando IDs/filas/columnas compatibles, exige versión vigente y compara ubicaciones antes/después dentro de la transacción.

Resultados del ensayo y aplicación: **1100 × 900 cm, 13 elementos, versión 1, cero ubicaciones previas conservadas y quick_check=ok**. Comparación exacta de todos los campos de geometría/nombres/tipos del resultado contra la referencia. Cuatro estantes superiores, mesón de igual ancho total debajo, pizarra izquierda, seis mesas en dos columnas por tres filas y Entrada a X=1010/Y=700, orientación 90°. Se aplicó exclusivamente la distribución local; no se copiaron usuarios, medicamentos, stock o recetas de la demo. No se aplicaron migraciones ni se alteró código de la interfaz en SAL-09.

Respaldo privado: `.test-artifacts/sala036-distribucion/db.sqlite3.before-distribucion-20261124T170651076565Z`, **843776 bytes**, SHA-256 `30b3e098ed2756bab135c4515afcc5f96b777a7e05d52ca45d7d969fb5edab00`. Metadatos/resultados en `operacion.json`; ensayo junto a ese respaldo. Ambos permanecen ignorados por Git.

```powershell
.venv/Scripts/python.exe work/sala036_inspeccionar_configuracion.py
.venv/Scripts/python.exe work/sala036_aplicar_referencia.py ensayar --propietario <id-local> --version 0
.venv/Scripts/python.exe work/sala036_aplicar_referencia.py aplicar --propietario <mismo-id> --version 0
.venv/Scripts/python.exe manage.py check --settings=core.local_runtime
```

Check local sin incidencias. No se repitieron tests de código ni navegador por una carga de configuración: la UI y geometría ya se verificaron en SAL-08 y la referencia coincide con los datos persistidos. Revisión humana en la sala habitual pendiente. Recuperación: detener escrituras, preservar cambios posteriores y restaurar respaldo/código compatibles; no sobrescribir nuevas actividades o asignaciones sin revisión.

## Publicación autorizada en valentina

La usuaria solicitó commit/push de los cambios realizados a valentina. Comprobación previa: rama local valentina, origin en el repositorio del equipo, remoto actualizado y sin commits remotos pendientes respecto de HEAD. Se publican sala/entrada, áreas docentes necesarias, skills proporcionadas, migraciones, estilos, pruebas, documentación pertinente y scripts de reproducción de la distribución. Diagramas y preparación separada de Render permanecen pendientes; sus partes de documentos compartidos se separan solo en el índice, preservando el árbol de trabajo.

Verificación final con core.test_settings: **130 pruebas Django, 129 correctas y una omitida por PostgreSQL; 10 JS correctas; check sin incidencias y sin migraciones pendientes de generar**. La selección candidata tiene 250 archivos/28,25 MB antes de normalización de Git, sin rutas de bases, .env, medios, respaldos o exportaciones; búsqueda acotada de patrones de credenciales sin coincidencias. No equivale a auditoría exhaustiva. Los datos y configuración guardados en SQLite no se publican; el script de referencia permite reproducir la geometría en otra base expresamente seleccionada y respaldada.

Estado del commit/push: verificar por coincidencia de HEAD con origin/valentina al ejecutar la publicación. Sin despliegue ni integración automática a main.
