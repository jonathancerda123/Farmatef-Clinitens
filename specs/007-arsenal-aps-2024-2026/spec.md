# 007 — Catálogo de arsenal APS 2024–2026

Fecha: 2026-11-03. Estado: implementación local preparada; reemplazo de datos pendiente de confirmación final. Fuente: solicitud explícita de actualizar FarmaTEF desde el PDF provisto por la usuaria y preservar datos simulados. Código autorizado: sí. Reemplazo persistente autorizado para preparar, no ejecutar hasta confirmación final.

## Problema y resultado

El catálogo local de FarmaTEF contiene 109 presentaciones derivadas del Vademécum comercial 2023. El equipo docente entregó el Arsenal Farmacoterapéutico APS 2024–2026 con 363 presentaciones genéricas, clasificación y observaciones. El prototipo debe usar la fuente docente prioritaria y distinguir los datos simulados de inventario de existencias reales.

## Alcance

- Añadir al modelo medicamento clasificación, observaciones y fuente documental; marcar lotes simulados.
- Conservar una copia inactiva del catálogo previo de 109 productos.
- Preparar un comando explícito y acotado al usuario responsable para añadir las 363 presentaciones y un lote ficticio por cada una.
- No tocar cuentas, perfiles, cursos, otros medicamentos, datos personales ni medios.
- No ejecutar el reemplazo persistente hasta que la usuaria revise y confirme el resumen final.

## Datos y reglas

- La fuente contiene 363 filas válidas con nombre genérico, forma, concentración, clasificación, observaciones y página.
- Presentación del catálogo: nombre genérico más concentración y forma, para satisfacer unicidad por responsable.
- Sin existencias reales: stock mínimo de demostración 10; unidades ficticias deterministas de 1–40 por presentación; vencimientos ficticios de 20–719 días desde la carga; número de lote prefijado `SIM-APS-2024-2026-`.
- Cada lote queda marcado `es_simulado=True`; la pantalla lo identifica como simulado. Se conserva su clasificación y observación del PDF.
- Reemplazar significa desactivar el catálogo anterior, sin borrarlo físicamente, para conservar reversión e historial. No se modifica ninguna fila que no coincida con el conjunto de 109 nombres previos del usuario indicado.

## Requisitos y aceptación

- RF-007-01: El catálogo nuevo conserva los cinco atributos fuente y su página.
- RF-007-02: La migración de esquema añade campos aditivos sin cargar ni borrar registros.
- RF-007-03: El comando en modo vista previa no escribe; requiere `--apply` para operar.
- RF-007-04: El comando solo actúa sobre el usuario elegido y aborta si no encuentra 109 registros previos ni cero, o si ya hay importación de la fuente.
- RF-007-05: La operación es atómica; conserva antiguos inactivos, crea 363 presentaciones y 363 lotes marcados simulados.
- RF-007-06: La interfaz indica que stock y vencimientos son simulados.

## Límites

Los nombres del catálogo comercial 2023 no se equiparan uno a uno con genéricos sin revisión profesional. No se recomienda uso para prescripción ni decisiones clínicas. El inventario nuevo es sintético y solo para demostración académica.
