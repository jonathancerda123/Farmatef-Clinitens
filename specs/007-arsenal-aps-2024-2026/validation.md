# Validación — 007

Fecha: 2026-11-03. Fuente: PDF Arsenal Farmacoterapéutico APS 2024–2026, siete páginas.

| Verificación | Resultado | Estado |
|---|---|---|
| Extracción de tabla | 363 presentaciones únicas; encabezados/notas excluidos | Preparada |
| Base local en modo solo lectura | 109 medicamentos, propietario interno 9 (`valita`), cero lotes | Observado |
| Código de presentación/migración | `makemigrations --check --dry-run --settings=core.test_settings`: sin cambios pendientes tras generar migración 0002 | Correcto |
| Configuración aislada | `manage.py check --settings=core.test_settings`: sin problemas | Correcto |
| Migración de esquema en base local | `manage.py migrate --noinput`: no había migraciones pendientes; esquema 0002 ya estaba aplicado | Correcto |
| Vista previa del reemplazo | Responsable `valita`, 109 registros antiguos, 363 presentaciones; no escribió datos | Correcto |
| Aplicación del reemplazo | 109 antiguos inactivos; 363 nuevas presentaciones y 363 lotes simulados | Correcto |
| Integridad y conteos posteriores | `integrity_check=ok`; nuevos 363 activos, antiguos 109 inactivos; 363 lotes, 7.434 unidades, todos simulados; campos fuente completos | Correcto |
| Suite funcional / navegador | No ejecutados | Pendiente |

Inventario de demostración: 363 lotes, 7.434 unidades deterministas en total, stock mínimo 10 por medicamento, 82 presentaciones bajo el mínimo; fechas de vencimiento del 2026-11-23 al 2028-10-22. El lote y el modelo marcan estos datos como simulados. Respaldo previo en `.test-artifacts/arsenal-007/`.
