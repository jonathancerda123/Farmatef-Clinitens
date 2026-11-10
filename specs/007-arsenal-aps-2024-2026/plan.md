# Plan técnico — 007

## Integración

| RF | Archivo | Cambio | Verificación prevista |
|---|---|---|---|
| 007-01/02 | `FarmaTEFApp/models.py`, migración 0002 | Campos fuente y simulación | `makemigrations --check`, `check` aislado |
| 007-01 | `FarmaTEFApp/data/arsenal_aps_2024_2026.json` | Filas extraídas del PDF, conserva página/categoría | conteo, unicidad, longitudes |
| 007-03/04/05 | `FarmaTEFApp/management/commands/reemplazar_arsenal_aps.py` | Vista previa y reemplazo explícito transaccional por usuario | revisión de modo vista previa; migración/carga solo tras confirmación |
| 007-06 | formulario, admin e inventario | Mostrar fuente, clasificación y etiqueta simulada | `manage.py check` aislado; revisión estática |

## Migración, reversión y respaldo

La migración 0002 es aditiva de esquema. El comando no se ejecuta como parte de `migrate`; requiere `--apply` y usuario explícito. Antes de ejecutarlo se hará una copia SQLite en `.test-artifacts/arsenal-007/`. Los 109 registros previos se desactivan, no eliminan. El comando y datos requieren revisión final de la usuaria.

## Inventario sintético

Un lote por presentación. Unidades con secuencia determinista 1–40; mínimos 10. Vencimiento relativo al día de carga, 20–719 días a futuro. La interfaz y `es_simulado` impiden presentar el dato como stock real.
