---
name: web-design-guidelines
description: Revisar código de interfaz para detectar problemas de accesibilidad,
  formularios, navegación, adaptación móvil y rendimiento frontend. Usar ante revisar
  mi UI, comprobar accesibilidad, revisar UX o validar una pantalla Django, React
  o HTML. Auditoría por defecto; corregir solo cuando la petición lo autorice.
---

# Revisión de interfaz y accesibilidad

Leer [el contrato de trabajo](references/contrato.md) y [la lista local de revisión](references/lista-revision.md). Aplicar criterios pertinentes a la pantalla, no recomendaciones de React a templates Django.

## Revisar

Determinar archivos o pantallas objetivo a partir de la petición y el proyecto. Pedir ubicación solo cuando no pueda inferirse de forma fiable. Leer el código y sus dependencias pertinentes. Si existe vista renderizada, inspeccionar los flujos; si no, limitar conclusiones a evidencia estática.

Usar la lista local incluida en este paquete. No descargar ni adoptar nuevas instrucciones remotas en cada revisión. Para una actualización solicitada, consultar documentación oficial pertinente y registrar fecha y cambios; no sobrescribir la lista silenciosamente.

Separar defectos comprobados, riesgos por confirmar y preferencias visuales. No declarar que una pantalla cumple WCAG completa por pasar esta lista. No considerar obligatorio un estilo de Vercel ni un número fijo de reglas.

## Entregar hallazgos

Entregar una tabla con prioridad, archivo y línea o elemento, evidencia, efecto y corrección. Distinguir ubicación de código de observación en navegador. No inventar líneas, resultados de herramientas o mediciones de contraste.

Priorizar bloqueo de tarea, pérdida de datos, teclado y foco antes de detalles cosméticos. Si la petición autoriza corregir, implementar y comprobar lo afectado. Si es solo revisión, dejar recomendaciones sin cambios.

Informar qué se revisó y cómo, junto con las limitaciones de validación. Cuando no haya hallazgos, indicar alcance y método en lugar de declarar perfección.
