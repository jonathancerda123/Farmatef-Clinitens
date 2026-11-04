# Tareas — 013 / Etiquetado de lotes para FarmaTEF

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Solicitud explícita autorizó implementación local; no implica commit/push/despliegue.

- [x] T-013-01 — Documentar alcance y aceptación verificable.
  - RF: RF-013-01–05. Archivos: paquete documental 013.
  - Hecho cuando: spec, plan, tareas y validación creados antes del código.
- [x] T-013-02 — Crear formulario y vista de impresión con permisos por actor, selección coherente y límites estrictos.
  - RF: RF-013-01–05. Archivos: `FarmaTEFApp/forms.py`, `views.py`, `urls.py`, template.
- [x] T-013-03 — Integrar acceso desde la portada FarmaTEF.
  - RF: RF-013-01. Archivo: `templates/pages/farmatef/farmatef.html`.
- [x] T-013-04 — Ejecutar comprobaciones básicas y actualizar trazabilidad/estado.
  - RF: RF-013-01–05. Evidencia y límites registrados en `validation.md`.
- [x] T-013-05 — Adaptar la distribución, vista previa y presets a las referencias aportadas.
  - RF: RF-013-06/07/08. Archivos: `templates/pages/farmatef/etiquetado.html`, `spec.md` y `plan.md`.
  - Hecho cuando: diseño de dos columnas adaptable, cuatro presets, medidas editables y escala/acción de impresión visibles.
- [x] T-013-06 — Aclarar el selector de lote y evitar medidas que recorten el contenido.
  - RF: RF-013-03/09. Archivos: `FarmaTEFApp/forms.py`, `templates/pages/farmatef/etiquetado.html` y documentación 013.
  - Hecho cuando: opciones muestran código/vencimiento/stock, la diferencia medicamento/lote se explica y ancho/alto tienen mínimos legibles.
- [x] T-013-07 — Filtrar los lotes por medicamento y conservar el rechazo de combinaciones inválidas en servidor.
  - RF: RF-013-10. Archivos: `FarmaTEFApp/forms.py`, `templates/pages/farmatef/etiquetado.html`.
  - Hecho cuando: al elegir medicamento solo quedan opciones de sus lotes y el servidor rechaza la relación cruzada.

## Autorización / ejecución

2026-11-04: la usuaria solicitó agregar el apartado de Etiquetado. Implementación local autorizada; sin persistencia, migración ni publicación.

## Reanudación y aceptación

Implementación local terminada. Aceptación humana, revisión de interfaz y calibración con impresora pendientes.
