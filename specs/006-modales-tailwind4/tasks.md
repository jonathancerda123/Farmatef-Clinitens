# Tareas — 006 / Modales con Tailwind 4

Spec: [spec.md](spec.md). Plan: [plan.md](plan.md). Fecha: 2026-10-21. Paquete revisado y ejecución autorizada por «ya revisé, puedes implementar». Implementación local realizada; T-006-06 conserva verificaciones visuales pendientes.

- [x] T-006-01 — Documentar el cambio y su impacto transversal.
  - RF: RF-006-01 a RF-006-05. Depende de: ninguna.
  - Archivos: spec.md, plan.md, tasks.md, validation.md; proyecto/estado/decisiones/trazabilidad/arquitectura e índice pertinentes.
  - Hecho cuando: inventario observado, hipótesis, límites, aceptación propuesta y punto de reanudación escritos; sin modificar implementación.
- [x] T-006-02 — Reproducir y delimitar los consumidores afectados.
  - RF: RF-006-01/02/03. Depende de: T-006-01 e instrucción posterior del usuario.
  - Archivos existentes: plantillas de cuentas/pacientes/componente compartido, static/js/modal.js, hojas fuente y salida CSS. Evidencia futura: validation.md.
  - Hecho cuando: ruta, activador, perfil ficticio, navegador, viewport, estilos computados, síntoma y resultado esperado registrados; distinguir consumidor activo de componente sin uso localizado.
  - Resultado: cuentas en (0,0) y foco detrás de pacientes reproducidos; comprobaciones aisladas con Python instalado y paquetes existentes, sin reparar el entorno anterior.
- [x] T-006-03 — Corregir el defecto confirmado del diálogo de cuentas.
  - RF: RF-006-01/02. Depende de: T-006-02.
  - Archivos existentes previstos: static/css/styles.css; usuarios_lista.html solo si necesario.
  - Hecho cuando: centrado/tamaño/scroll cumplen criterios, estado cerrado y API nativa preservados, teclado/cancelación/reapertura comprobados. Si no se reproduce, registrar y volver al diagnóstico antes de editar.
- [x] T-006-04 — Resolver únicamente defectos demostrados en los otros patrones.
  - RF: RF-006-02/03. Depende de: T-006-02.
  - Archivos existentes condicionados: pacientes.html; components/modal/modal.html y modal.js solo con consumidor identificado.
  - Hecho cuando: casos de carga/error/red/respuesta tardía y foco revisados; cada cambio tiene reproducción. Si no requiere edición, cerrar con evidencia de regresión y «sin cambio», sin activar código dormido.
- [x] T-006-05 — Verificar permisos, contratos y ausencia de escrituras al cancelar.
  - RF: RF-006-04. Depende de: T-006-03/04.
  - Archivos de referencia: UsuarioApp/views.py, CliniTensDocenteApp/views.py, core/mixins.py, core/permissions.py, URLs y pruebas existentes; regresión ejecutable futura solo si hay fallo lógico reproducido.
  - Hecho cuando: URL directa permitida/denegada, roles/propiedad, protección superusuario, POST/CSRF y cancelación verificados con fixtures. No se cambian permisos para superar una prueba.
- [ ] T-006-06 — Compilar y verificar interfaz transversal.
  - RF: RF-006-01/02/03/05. Depende de: T-006-03/04/05.
  - Archivos: fuentes/build/salida de Tailwind existentes, plantillas existentes, validation.md para evidencia.
  - Hecho cuando: build y controles pertinentes ejecutados, fallo de compilación conserva CSS, navegador 1440/768/390/zoom/teclado revisado y regresión de portadas/ficha/FarmaTEF registrada. No equivale a validar funcionalmente todo FarmaTEF.
  - Parcial: build, 9 JS, 35 Django, permisos, navegador 1440/768/390 y regresión de portadas/ingreso a ficha/inventario ejecutados. Pendientes zoom real 200% y emulación de movimiento reducido; no se marca verificación completa.
- [x] T-006-07 — Registrar cierre técnico y pendientes de aceptación.
  - RF: RF-006-01 a RF-006-05. Depende de: T-006-06.
  - Archivos: validation.md, docs/ESTADO_PROYECTO.md, docs/TRAZABILIDAD.md y arquitectura solo si cambió realmente.
  - Hecho cuando: evidencia real enlazada, bloqueos y casos no ejecutados explícitos; ninguna aceptación humana inferida.

## Autorización y ejecución

| Fecha | Tarea | Acción / entorno | Resultado y límite |
|---|---|---|---|
| 2026-10-21 | T-006-01 | Lecturas, rg/Get-Content/Get-FileHash, consulta de documentación técnica y edición Markdown | Documentado; git status no disponible por ausencia de .git. Sin ejecución funcional/build/servidor |
| 2026-10-21 | T-006-02/03/04 | Navegador + pruebas diferidas; CSS de compatibilidad y plantilla de pacientes | Cuentas centradas; pacientes con dialog nativo y solicitudes versionadas; helper sin uso intacto |
| 2026-10-21 | T-006-05 | `review.py checks` / `permissions`, settings independientes | 35 pruebas Django correctas; 21 GET y cuatro POST de permisos correctos con datos ficticios |
| 2026-10-21 | T-006-06/07 | Build CLI 4.3.3, node --test, navegador y documentación | 9 JS correctas; revisión visual parcial, evidencia guardada y pendientes explícitos |

## Reanudación

Próximo paso: completar zoom 200%/movimiento reducido y revisar funcionalmente cuentas/pacientes con el usuario. La implementación ya está autorizada y realizada; no volver a pedir permiso para ese mismo alcance. Conservar archivos presentes y evidencia; no restaurar CliniTENS.rar. No hay autorización de despliegue, migración real, commit/push ni purga histórica. Aceptación final pendiente.
