# Tareas — 017 / Flujos DAU, laboratorio y CAD

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Autorizado por petición explícita de la usuaria el 2026-11-05; no implica despliegue, commit/push o migración de base recibida.

- [x] T-017-01 — Añadir esquema aditivo para órdenes, documentos CAD, tubos recolectados y documentos revisados.
  - RF: 02, 03, 05. Archivos: `CliniTensSimulacionApp/models.py`, migración nueva. Hecho cuando: defaults vacíos y relaciones históricas intactas; migración verificada en memoria.
- [x] T-017-02 — Crear formularios docentes estructurados para órdenes y resultados CAD.
  - RF: 02, 03. Archivos: `forms.py`, `views.py`. Hecho cuando: IDs/categorías/límites validados sin aceptar JSON arbitrario.
- [x] T-017-03 — Completar práctica de laboratorio tubo a tubo y etiqueta de impresión individual.
  - RF: 02. Archivos: `views.py`, `urls.py`, plantillas y CSS/JS local si hace falta. Hecho cuando: cada tubo guarda su propio estado y etiqueta muestra SIM, muestra y exámenes.
- [x] T-017-04 — Implementar Centro de Apoyo Diagnóstico docente/estudiante y revisión individual.
  - RF: 03. Archivos: `views.py`, `urls.py`, plantillas. Hecho cuando: cuatro clases de resultado se separan y cada revisión queda en intento propio.
- [x] T-017-05 — Sustituir la presentación vigente de Kardex por CAD sin eliminar el historial legado.
  - RF: 04, 05. Archivos: portada, módulos, rutas/etiquetas y documentación. Hecho cuando: recorridos visibles dicen CAD y Kardex histórico queda intacto.
- [x] T-017-06 — Verificar técnica y registrar evidencia/pendientes.
  - RF: 01–05. Hecho cuando: checks y carga de templates/rutas se registran literalmente; no se atribuye prueba funcional no ejecutada.

## Registro de ejecución

| Fecha | Tarea | Evidencia | Resultado |
|---|---|---|---|
| 2026-11-05 | T-017-01 | `core.test_settings`; `migrate --noinput` en base en memoria | Migración 0005 aplicada en memoria; base habitual intacta |
| 2026-11-05 | T-017-02 a 05 | `manage.py check`; plantillas/rutas cargadas | Formularios, pantallas y rutas conectados; matriz HTTP no ejecutada |
| 2026-11-05 | T-017-06 | `check`, `makemigrations --check --dry-run`, carga de 7 plantillas y 7 reverses | Sin errores técnicos; revisión visual detenida por limitación de Computer Use |

## Reanudación y aceptación

Fase: implementación local completada. No tocar base normal ni `media/`, secretos o datos de usuarios. Próximo paso: revisar con perfiles docente/estudiante, comprobar impresión a tamaño 60 × 40 mm y, si se desea usar en la base local, hacer primero un respaldo y aplicar migración 0005. Aceptación humana pendiente.
