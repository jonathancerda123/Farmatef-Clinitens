# Tareas — 018 / Flujo de laboratorio por pasos

Autorizado por solicitud explícita, 2026-11-05. Alcance local. Sin commit/push ni migración a la base habitual.

- [x] T-018-01 — Agregar modelo de orden emitida con instantáneas y migración aditiva.
- [x] T-018-02 — Implementar wizard autenticado paciente/exámenes/resumen con validación de catálogo, curso y propiedad.
- [x] T-018-03 — Añadir emisión, historial propio y acceso a una orden emitida.
- [x] T-018-04 — Crear presentación confirmada, PDF de orden y etiquetas educativas tubo a tubo.
- [x] T-018-05 — Actualizar acceso desde práctica estudiantil y estilos responsivos.
- [x] T-018-06 — Verificar técnicamente con settings aislados, documentar límites y recuperación.

## Registro

2026-11-05: migración `0006_solicitudlaboratoriosimulada` generada; `check`, cotejo de migraciones y aplicación en base en memoria correctos; tres templates y cuatro rutas cargaron/revirtieron. Tras petición explícita, también se aplicó a la base local después de respaldo verificado en `.test-artifacts/lab-018/`. No se ejecutaron tests, navegador, matriz de permisos HTTP ni impresión física.
