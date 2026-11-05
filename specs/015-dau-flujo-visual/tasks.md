# Tareas — 015

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Código local autorizado por la petición explícita de la usuaria de ajustar DAU a las capturas.

- [x] T-015-01 — Añadir datos de paciente SIM a casos y entidad separada de atención DAU/procedimientos.
  - RF: 015-02/04/05. Hecho cuando: migración aditiva y múltiple historial por caso/alumno.
- [x] T-015-02 — Hacer formulario docente para configurar paciente ficticio y validar código SIM único.
  - RF: 015-02. Hecho cuando: nuevos casos requieren ficha SIM; casos antiguos sin esos campos no se exponen en la búsqueda DAU.
- [x] T-015-03 — Construir acceso por código SIM, sesión, curso y consulta del paciente.
  - RF: 015-01/07. Hecho cuando: el estudiante solo encuentra pacientes ficticios de cursos publicados y propios.
- [x] T-015-04 — Construir panel de signos, cálculos, procedimientos y cierre del DAU.
  - RF: 015-03/04/05. Hecho cuando: cálculos redundantes en servidor; eventos persistentes; estado final bloqueado.
- [ ] T-015-05 — Crear historial personal y PDF/impresión identificados como simulación.
  - RF: 015-06. Hecho cuando: atenciones previas se conservan y PDF se inspecciona.
- [ ] T-015-06 — Ajustar navegación y estilos responsive/accessibles.
  - RF: 015-08. Hecho cuando: navegador escritorio/móvil/teclado.
- [x] T-015-07 — Verificar checks/cotejo/carga básica y actualizar documentación; aceptación humana sigue pendiente.
  - RF: 015-01–08. Hecho cuando: solo resultados reales quedan documentados; aceptación humana pendiente.

## Autorización y ejecución

| Fecha | Tarea | Resultado |
|---|---|---|
| 2026-11-04 | Solicitud visual | Autorizada implementación local del flujo DAU, dentro de la simulación y usando datos inventados. |
| 2026-11-04 | Corrección de formulario docente | La usuaria señaló que los controles estaban desordenados. Se sustituyó el flujo en línea por secciones numeradas, cuadrículas y estilos dedicados; requiere recarga forzada y revisión visual final. |

No autorizado: push, despliegue, uso de datos reales.
