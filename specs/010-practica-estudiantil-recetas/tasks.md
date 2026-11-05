# Tareas — 010

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Código autorizado localmente por la usuaria el 2026-11-04 («me gusta, hazlo»). Sin autorización de commit/push ni despliegue.

- [x] T-010-01 Documentar y migrar el curso, pista, clave docente, retroalimentación e intentos individuales.
  - RF: 010-01/03/06/09/10. Archivos: modelos, migración, formularios y admin.
  - Hecho cuando: migración aditiva aplicada tras respaldo y cotejo sin cambios pendientes.
- [x] T-010-02 Implementar acceso docente y vistas estudiantiles por matrícula.
  - RF: 010-01/02/04/05. Archivos: vistas, URL, templates y navegación.
  - Hecho cuando: filtrado en servidor y clave ausente de salida estudiantil.
- [x] T-010-03 Integrar corrección de respuesta y descuento FEFO atómico.
  - RF: 010-07/08/09. Archivos: servicios y modelos de respuesta/dispensación.
  - Hecho cuando: intentos inválidos no cambian stock; dispensación válida registra consumo y respuesta individual.
- [x] T-010-04 Revisar documentación, checks y límites.
  - RF: todos. Archivos: validación, arquitectura, estado, índice de specs y README.
  - Hecho cuando: evidencia refleja solo comandos ejecutados; aceptación visual/funcional pendiente.

## Autorización / ejecución

| Fecha | Tarea | Archivo / comando / entorno | Resultado y límite |
|---|---|---|---|
| 2026-11-04 | T-010-01 a T-010-04 | Modelos, formularios, servicios, vistas, URLs, plantillas, navegación y docs | Implementado localmente; `0007` aplicada tras respaldo; checks limpios. Sin suite funcional/browser; aceptación pendiente. |
