# 027 — Arsenal APS en el inventario de la demo FarmaTEF

Fecha: 2026-11-18. Fuente: solicitud de incorporar el PDF Arsenal Farmacoterapéutico APS 2024–2026 al inventario de la captura y reemplazar las coincidencias. Destino identificado por sus medicamentos y lotes: demo ficticia 8025. Operación de datos solicitada. Revisión humana pendiente.

## Alcance y reglas

- RF-027-01: Incorporar las 363 presentaciones del PDF para el responsable del inventario mostrado. Usar los campos existentes de Medicamento, Clasificación, Stock, Mínimo, Lotes y Estado.
- RF-027-02: Actualizar la clasificación y presentación de las coincidencias en su registro original. Identificar por nombre genérico, concentración y forma. Una forma específica coincide cuando está enumerada como alternativa en esa presentación del PDF. Conservar la forma específica registrada, el identificador, los vínculos, el mínimo y los lotes. Si la coincidencia es ambigua, abortar la carga.
- RF-027-03: Las nuevas presentaciones empiezan con el mínimo predeterminado de 0 y sin lotes. La vista obtiene el stock y el estado con sus reglas actuales. El PDF aporta nombre, concentración, forma y clasificación. Sus observaciones se excluyen de la carga.

## Aceptación verificable

| Dado / cuando | Resultado esperado |
|---|---|
| Se comparan las siete páginas con las filas fuente existentes | Coinciden las 363 presentaciones y sus clasificaciones. |
| Se aplican las coincidencias al catálogo de cinco registros | Se actualizan cuatro, se agregan 359 y queda el producto ficticio ajeno al arsenal. |
| Se revisan lotes, receta y dispensación antes y después | Las referencias y existencias conservan sus valores. |
| Se repite la conciliación y se consulta el inventario | Cero altas o cambios adicionales. Se ven las seis columnas existentes y se mantienen los permisos. |

## Límites

La operación corresponde a la demo ficticia y al propietario de los registros de la captura. Sin alteraciones de esquema ni aplicación a la base habitual.
