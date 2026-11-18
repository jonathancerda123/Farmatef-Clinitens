# Validación — 028

Fecha: 2026-11-18. Entorno: demo 8025 y copia de ensayo, Python 3.12, Django 5.2.18 y `core.test_settings`.

Se observaron 364 productos, 359 con mínimo 0, siete lotes previos, dos cursos con alumnado inscrito, cinco recetas existentes y cuatro escenarios clínicos publicados. La carga se aplicó el mismo día a la demo tras ensayar sobre una copia. Aceptación docente pendiente.

| Requisito | Evidencia |
|---|---|
| RF-028-01 | Los 364 productos tienen mínimo y saldo positivo. Se agregaron 467 lotes simulados, para 474 en total. Hay 21.822 unidades registradas y 21.662 disponibles al 18 de noviembre. |
| RF-028-01 | Se detectaron 45 productos con stock bajo, 55 con vencimiento próximo y 19 con lotes vencidos. Las alertas pueden coincidir en un producto. Quedaron 266 sin alertas. |
| RF-028-02 | `APS028-01` a `APS028-05` quedaron pendientes. Farmacia QA tiene tres nuevas y Práctica clínica integrada tiene dos. En el ensayo, una presentación incorrecta habilitó un segundo intento, dos dispensaciones descontaron solo los lotes elegidos y tres rechazos conservaron el saldo. |
| RF-028-03 | `SIM-APS028-01` a `SIM-APS028-05` publicados, con `FCE-APS028-01` a `FCE-APS028-05` activos. Se agregaron cinco pacientes, diez resultados diagnósticos, dos fichas de ejemplo, dos DAU, dos RAE, dos órdenes y dos revisiones de CAD de práctica. |
| RF-028-02 y RF-028-03 | 73 solicitudes verificadas en el ensayo y 54 en una copia de la demo cargada. Se probaron las rutas de docente y estudiante, la denegación sin matrícula, el acceso administrador, las órdenes, las etiquetas, el comprobante y el cierre DAU/RAE. Se revirtieron las transacciones de prueba. |
| RF-028-01 a RF-028-03 | SQLite `quick_check` y `foreign_key_check` correctos. La carga conserva los registros previos. Un reintento reconoció la carga anterior sin volver a agregar casos. |

## Recorridos incorporados

| Nº | Caso clínico | Receta de práctica | Curso de la receta |
|---|---|---|---|
| 01 | Tos y sibilancias en urgencia | Salbutamol en aerosol y comparación con la presentación para nebulización | Farmacia QA |
| 02 | Control cardiovascular y retiro FOFAR | Retiro de metformina y amlodipino en dos líneas | Práctica clínica integrada |
| 03 | Síntomas urinarios y trazabilidad de muestra | Nitrofurantoína con stock vigente insuficiente | Farmacia QA |
| 04 | Lesión interdigital y revisión de receta | Clotrimazol tópico con receta vencida | Farmacia QA |
| 05 | Prurito persistente e indicaciones incompletas | Cetirizina con indicaciones ilegibles | Práctica clínica integrada |

Las referencias orientaron el contexto de FOFAR y la selección de muestras educativas. Saldos, valores y personas son ficticios. [FOFAR, MINSAL](https://saludresponde.minsal.cl/fondo-de-farmacias-fofar/) · [Cartera de exámenes, Hospital San Juan de Dios](https://hsjd.redsalud.gob.cl/wp-content/uploads/2026/04/Cartera-Examenes-Laboratorio-Clinico-2026.-V2.pdf) · [Instructivo de laboratorios clínicos, ISP](https://www.ispch.cl/wp-content/uploads/2024/07/Instructivo-para-evaluacion-del-Manual-Estandar-GENERAL-aCREDITACION-LAB-CLINICOS-V-9.1.pdf) · [Manual de laboratorio, Hospital San Camilo](https://www.hospitalsancamilo.cl/pdf/2013/manual_laboratorio.pdf).

## Entorno y recuperación

- Ejecutados `precargar.py ensayo`, `verificar.py ensayo`, `precargar.py demo`, `verificar.py demo` y `precargar.py verificar-reintento` en `.test-artifacts/demo-028` con `.test-artifacts/clinica-019-env/Scripts/python.exe`.
- Verificados `manage.py check` y `manage.py makemigrations --check --dry-run`, ambos con `--settings=core.test_settings`. La suite Django aislada obtuvo 93 pruebas correctas y una omitida por requerir PostgreSQL.
- `node.exe .test-artifacts/demo-028/verificar_chrome.cjs` comprobó inventario, lista de recetas, receta FOFAR y CAD a 1440×920. Chrome renderizó las respuestas de Django y sus recursos locales por interceptación de solicitudes sobre una copia de la demo. Se guardaron cuatro capturas. Conectividad HTTP en vivo fuera de esta verificación.
- Respaldo verificado en `.test-artifacts/demo-028/demo-antes-20261118T184323115887Z.sqlite3`. Para recuperar la demo anterior, detener 8025 y restaurar la copia en `.test-artifacts/farmacia-025-fixture.sqlite3`.

Próxima revisión docente: abrir `APS028-02` y luego recorrer el mismo escenario con `SIM-APS028-02` o `FCE-APS028-02`.
