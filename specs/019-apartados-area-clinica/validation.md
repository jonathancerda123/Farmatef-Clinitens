# Validación — 019

Fecha local: 2026-11-09 (America/Santiago). Base Git `df23932`; rama `jonathan`, upstream `origin/jonathan`. Implementación local autorizada, sin commit nuevo; aceptación humana pendiente.

| RF | Comprobación | Resultado actual |
|---|---|---|
| 01/02 | Matriz HTTP Django de portada: estudiante, MANAGER, ADMIN, superusuario sin perfil y cuenta sin perfil | Siete apartados en orden, 35 opciones cotejadas y 25 destinos permitidos con 200. Opciones restringidas sin enlace. [Matriz](../../docs/evidencias/019-apartados/permisos-portada.json) |
| 03 | `node build.cjs` desde `theme/static_src`; navegador Chrome con Playwright | Tailwind 4.3.3 correcto. Portada 1440/768/390 con 3/2/1 columnas; H1 único y ancho documento igual al viewport. [Reporte](../../docs/evidencias/019-apartados/navegador.json) |
| 04 | 14 nuevas pruebas RAE y recorrido de navegador | Búsqueda, borrador parcial, finalización, cierre de solo lectura, historial paginado, nuevo ejercicio y aislamiento correctos. Campos/acciones autorizados por confirmación del usuario |
| 05 | Git y revisión de archivos | Rama original `jonathan` y upstream conservados, cambios sin staging/commit/push. Base habitual, `.env` y medios no consultados ni modificados |
| 06 | Preparación docente en navegador y tests | Paciente de caso borrador actualizado; formularios reutilizan validación SIM y conservan escenario DAU, laboratorio, órdenes e informes. Publicado no admite edición; ajeno denegado |

## Entorno y límites

El target de AGENTS y `.venv` no existen en esta copia. Se creó `.test-artifacts/clinica-019-env` con Python 3.12.0 e instalación exacta de `requirements.txt`: Django 5.2.18/allauth 65.19.7. El primer intento falló por red del sandbox; el reintento con acceso de red instaló el archivo sin cambiar versiones. `pip check`: sin dependencias rotas. Runtime usado para pruebas, no validado para operación productiva.

Comandos ejecutados desde raíz, con intérprete `.test-artifacts/clinica-019-env/Scripts/python.exe`:

```powershell
<python> manage.py check --settings=core.test_settings
<python> manage.py makemigrations CliniTensSimulacionApp --settings=core.test_settings
<python> manage.py makemigrations --check --dry-run --settings=core.test_settings
<python> manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp CliniTensSimulacionApp --settings=core.test_settings
<python> -m pip check
node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs
```

Resultados: check sin incidencias; migración aditiva `0007_atencionenfermeria.py`; cotejo sin cambios pendientes; **61 pruebas Django correctas**, incluidas 14 nuevas RAE, y **4 JS correctas**. Tras reforzar la comprobación de conservación de otros bloques del caso se repitieron las 14 RAE, correctas. El build se ejecutó mediante `node build.cjs` desde `theme/static_src` después de instalar el lock con npm ci (npm obtenido mediante pnpm del runtime); no se cambió package/lock. Un primer intento de build desde raíz falló por directorio incorrecto y se corrigió. Los recursos vendor regenerados no presentan diferencias de contenido.

`git diff --check` se comprobó con `core.whitespace` incluyendo `cr-at-eol`: algunos archivos ya están versionados con CRLF; se conservaron sus finales de línea. No se reformatearon archivos ajenos ni se cambió configuración de Git.

## Permisos y concurrencia

Las pruebas nuevas ejecutan GET/POST permitidos y denegados: estudiante inscrito, ajeno, sin matrícula, caso borrador, matrícula revocada/publicación retirada, MANAGER/ADMIN/superusuario en ruta de estudiante, inactivo, sin perfil y anónimo. Preparación docente prueba propietario, ajeno, ADMIN/superusuario sin perfil y bloqueo publicado. Anónimo en práctica devuelve 403 conforme al mixin existente; portada redirige al login.

Texto excedido, acción desconocida, versión ausente/inválida y cierre sin cuidados no persisten. Contenido se escapa al renderizar. Versión obsoleta devuelve 409, conserva el texto enviado y no cambia el registro. Restricción de base impide dos borradores del mismo alumno/caso. Son pruebas de colisión lógica, no benchmark de concurrencia o carga.

## Navegador y evidencia visual

El lanzamiento de Edge dentro del sandbox falló; al ejecutarlo fuera, la conexión loopback seguía bloqueada. Se usó Chrome sin ventana y un puente de pruebas por stdio que entrega las respuestas del cliente Django sobre `.test-artifacts/clinica-019.sqlite3`, con comprobaciones CSRF activadas y recursos estáticos reales. No se modificó el código de la aplicación para el puente. La revisión no acredita red HTTP real ni un despliegue. Algunos intentos de redirección fallaron transitoriamente por loopback; una ejecución completa del puente terminó correctamente y quedó registrada en `navegador.json`. Un reintento sobre la misma fixture llegó al historial y falló en el selector del harness porque ya había dos atenciones finalizadas; se corrigió ese selector sin cambiar producto.

Se ejecutó el recorrido docente de completar paciente; el estudiante abrió RAE desde portada, buscó un código inexistente (valor preservado), abrió el SIM publicado, intentó finalizar sin cuidados (observaciones preservadas), guardó borrador, abrió dos pestañas, guardó una y rechazó la antigua con texto preservado, finalizó, consultó historial e inició otra atención vacía. H1 único y sin desbordamiento del documento en portada/registro a 1440/768/390; historial móvil desplaza su tabla. Se verificaron ancla, Tab y movimiento reducido. No se verificó zoom real 200%, otros motores, impresora ni toda la navegación por teclado.

Revisadas visualmente [portada escritorio](../../docs/evidencias/019-apartados/portada-1440.png), [portada móvil](../../docs/evidencias/019-apartados/portada-390.png), [registro escritorio](../../docs/evidencias/019-apartados/rae-1440.png) y [registro móvil](../../docs/evidencias/019-apartados/rae-390.png). Otras capturas y reporte se conservan en `docs/evidencias/019-apartados/`; solo identidades sintéticas. Scripts, sesiones sintéticas, entorno y base ficticia permanecen ignorados en `.test-artifacts`.

## Migración y uso en la instalación

0007 se aplicó al esquema de pruebas en memoria y a una fixture nueva bajo `.test-artifacts`; no se abrió ni migró una base habitual. Para activar RAE en la instalación del usuario, preparar el entorno normal, respaldar su base si existe y verificar recuperación, revisar `migrate --plan` y aplicar la migración de `CliniTensSimulacionApp` con autorización específica para ese destino. No ejecutar esas operaciones sobre datos recibidos solo por copiar este documento. El acceso estudiantil necesita caso publicado y matrícula; la publicación conserva los requisitos existentes de DAU/laboratorio/CAD.

RAE es una primera versión educativa acordada, no una copia comprobada de las pantallas interiores de la referencia. No se añadieron protocolos, diagnósticos, tratamientos ni interpretación automática. No se modificaron PDF/Excel. Las pruebas de navegación no equivalen a validar flujos clínicos completos. Aceptación visual/pedagógica pendiente; próximo paso: revisión con el usuario y preparación de migración en su instalación. Sin despliegue, commit ni push.
