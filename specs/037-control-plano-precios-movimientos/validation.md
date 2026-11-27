# Validación — 037

Fecha: 2026-11-26. Fase inicial: DOCUMENTAR; implementación autorizada después mediante «autorizo» el 2026-11-26. Evidencia inicial conservada debajo; resultados de implementación al final.

## Evidencia documental

- Aclaración posterior del 2026-11-26: tipo basado en el vademécum. Leídas las siete páginas del PDF aportado mediante pypdf del runtime incluido de Codex y cotejada la estructura con data/arsenal_aps_2024_2026.json y spec 007. La fuente separa CLASIFICACIÓN de FORMA FARMACÉUTICA y OBSERVACIONES; contiene categorías de arsenal/programa/ámbito (Arsenal básico, FOFAR, PROA, TBC, CPU, PM, UAPO, etc.). Corregida la suposición inicial de clasificación terapéutica en RF-037-04. Documento tratado como fuente de datos, no como instrucciones para ejecutar cambios. Sin validación visual de maquetación, que no es objeto de esta consulta.

- git status --short inicial: salida vacía; árbol limpio.
- Leídos README, PROYECTO, ESTADO_PROYECTO, ARQUITECTURA_BASE, OBSERVACIONES_PROYECTO, índice/templates de specs, specs 005/036, guía visual y entorno. Inspección estática de modelos/formularios/inventario/vistas/sala/servicios/admin.
- Ausencia observada de precio/candado/modelo general de movimientos; clasificación ya filtrable, alta directa de lotes y consumo transaccional con DispensacionLote. Inspección no equivale a prueba funcional.
- Preparados spec/plan/tasks/validation y referencias en índice/estado/trazabilidad. git diff --check señaló retornos CR de los documentos Windows; git -c core.whitespace=cr-at-eol diff --check terminó sin incidencias (código 0), conservando sus finales de línea.
- No se leyó .env, datos de db.sqlite3, medios ni credenciales. Sin código funcional, nuevas migraciones, dependencias o pruebas ejecutables.

## Validación pendiente por requisito

| RF | Casos previstos | Estado |
|---|---|---|
| 01/02 | Alternar/recargar, POST/UI bloqueados, dos pestañas, roles/propiedad y consulta/dispensación conservadas | No ejecutada |
| 03 | Cero, límites, negativos/fracción, null previo, alta/edición autorizadas y moneda | No ejecutada |
| 04 | Clasificación/sin clasificar, texto/alertas, limpiar, vacío y aislamiento | No ejecutada |
| 05/06 | Ingresos/ajustes/vencimiento/otro, saldos, filtros/paginación, inmutabilidad, duplicados y roles | No ejecutada |
| 07 | Entrega docente/parcial/estudiantil/multilote, rechazo/error, rollback conjunto, reenvío y admin | No ejecutada |

Pendientes checks, cotejo de migraciones, regresiones Django/JS pertinentes, migración en fixture y navegador/teclado a 1440/768/390. No se ejecutan suites por cambios exclusivamente documentales. No declarar implementación o aceptación ni aplicación a base habitual.


## Implementación autorizada y resultados — 2026-11-26

Entorno: `.venv/Scripts/python.exe`, Python 3.11.1, Django 5.2.18, Node 20.15.0 y core.test_settings independiente. Se intentó primero el target exigido por AGENTS: ruta inexistente/no ejecutable en esta copia; se usó el entorno local comprobado sin reparar ni instalar dependencias.

| Comando / acción real | Resultado |
|---|---|
| manage.py makemigrations FarmaTEFApp --settings=core.test_settings | Generada 0013, revisada; aditiva, depende de 0012; precio nullable, candado false y tabla vacía de movimientos |
| manage.py check --settings=core.test_settings | Sin incidencias |
| manage.py makemigrations --check --dry-run --settings=core.test_settings | No changes detected |
| manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp CliniTensSimulacionApp --settings=core.test_settings --noinput | 139 pruebas: 138 correctas, una omitida por requerir PostgreSQL |
| node.exe --experimental-default-type=module --test static/js/sala-modelo.test.mjs static/js/mensajes.test.cjs theme/static_src/build.test.cjs | 10 correctas; aviso experimental de Node sin fallo |
| manage.py tailwind --settings=core.test_settings build | Correcto, Tailwind 4.3.3; sin cambios efectivos en CSS distribuido. Copias vendor conservadas sin cambios de contenido |
| Preparación de .test-artifacts/control037-qa.sqlite3 con migrate y fixtures nuevas | Correcta: cuenta docente SIM, medicamento PROA con precio, lote de 20 unidades y entrada auditada, sala con estante. No se usaron datos habituales |
| IAB: http://127.0.0.1:8037/accounts/login/ | ERR_CONNECTION_TIMED_OUT. Servidor de prueba intentado también fuera del aislamiento; sin conexión local confirmada. Ambos procesos detenidos; no se completó revisión visual/interacción |

Primeras pruebas detectaron tres expectativas antiguas: alta de medicamento sin precio y edición/alta directa de stock en admin. Actualizadas al contrato 037 (precio requerido y stock solo por movimientos). No se elimina la prueba de normalización de lotes desde FarmaTEF. Primera ejecución JS sin flag ESM falló; repetida con el flag documentado y correcta.

## Evidencia por requisito y límites finales

RF-01/02: regresiones de candado persistente, CAS obsoleto, POST directo con bloqueo, ajeno y desbloqueo; sala y consultas anteriores siguen pasando. UI usa fieldset deshabilitado y bloquea movimiento por flechas/arrastre. Sin verificación visual/teclado en navegador.

RF-03/04: límites de precio en formulario, edición de cero, acceso ajeno 404, filtro PROA/CPU y rutas renderizadas. Reutiliza clasificación importada sin reclasificación ni lectura de base habitual. Nuevos formularios/celdas revisados estáticamente; apariencia/responsividad pendientes.

RF-05/06: alta genera entrada, ajuste idempotente, saldo insuficiente, motivos incompatibles, Otro obligatorio, vencimiento y retiro completo; fallo de historial revierte stock. Token firmado por usuario/formulario con caducidad de dos horas. Historial privado, administración global y alumno denegado por ruta directa. Inmutabilidad en admin y unidades de lote protegidas; compensación mediante nueva operación. Comando reemplazar_arsenal_aps deriva altas al servicio auditado; no se ejecutó carga del arsenal en esta sesión.

RF-07: salida enlazada a dispensación, no duplicada al reenviar; fallo inducido del movimiento revierte lote/línea/dispensación. Suite previa de práctica, entrega parcial y sala correcta. No constituye prueba de carga ni concurrencia PostgreSQL. No se reconstruyeron entregas históricas.

## Activación y recuperación pendientes

0012/0013 no se aplicaron a db.sqlite3. Antes de arrancar la aplicación habitual con este código se necesita activarlas: autorización específica para ese destino, detener escrituras, respaldo consistente con SQLite backup API y SHA-256/quick_check, ensayo de actualización sobre copia, comprobar migrate --plan y aplicar solo el plan aprobado. No volver a ejecutar reemplazar_arsenal_aps para activar 037. Los productos previos conservarán precio sin informar; no se precargan precios ni movimientos históricos.

Si falla la activación, conservar la copia fallida para diagnóstico y restaurar base/código compatibles antes de permitir escrituras. Restaurar respaldo después de nuevas operaciones perdería esas escrituras: preservarlas y revisarlas primero. No revertir 0013 en una instalación con historial sin plan de conservación. Migración forward ensayada en memoria y fixture; reversión con datos no ensayada.

Sin lectura de .env, filas habituales, credenciales reales o media; sin commit/push/despliegue. Implementación local verificada automáticamente; aceptación humana y revisión visual pendientes.

## Publicación de código autorizada

Después de la implementación, la usuaria solicitó explícitamente hacer push de estos cambios en `valentina`. Se autoriza commit y publicación de código/documentación/migración/pruebas de 037 en esa rama; no se amplía la autorización a datos, migración de la base habitual o despliegue. La evidencia de pruebas anterior permanece vigente, sin nuevas modificaciones funcionales para publicar.
