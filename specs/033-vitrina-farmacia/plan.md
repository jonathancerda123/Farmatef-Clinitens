# Plan técnico — 033

Implementación autorizada el 2026-11-19. Base inspeccionada: vistas/mixin estudiantil, servicios de dispensación, inventario, plantillas, shell y tokens. Cambios locales iniciales: `docs/diagramas/` y `work/` sin seguimiento, se preservan.

| RF | Archivos | Cambio y comprobación |
|---|---|---|
| 01, 05 | FarmaTEFApp/views.py, urls.py, vitrina.py | GET protegido por EstudianteFarmaMixin, curso matriculado y creador autorizado; pruebas de URL directa |
| 02, 03 | vitrina.py | Agregación vigente y distribución española/natural en 140 espacios; pruebas de ceros, vencimiento, volumen y descuento real |
| 03, 04 | templates/pages/farmatef/vitrina.html, static/js/vitrina.js, static/css/vitrina.css | Layout compartido; controles locales, dos muebles por vista, consulta segura y fallback sin JS |
| 01 | práctica/portada/shell | Enlaces de consulta, acceso contextual tras dispensación |
| Todos | tests_vitrina.py, static/js/vitrina.test.cjs, validation.md | Pruebas aisladas, build y navegador con datos ficticios; registrar límites |

Sin persistencia nueva ni paquetes. Recuperación: retirar únicamente archivos/enlaces de 033 y recompilar; no restaurar bases. La vitrina no modifica transacciones ni la política de dispensación. Orden y posiciones derivados del catálogo, no equivalen al almacenamiento físico validado.
