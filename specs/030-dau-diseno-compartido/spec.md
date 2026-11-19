# 030 — Diseño compartido para Registro de Atención de Urgencia

Fecha: 2026-11-18. El usuario solicitó reorganizar y unificar el aspecto del DAU. Las capturas muestran la entrada estudiantil, hoy centrada en una columna angosta y con una paleta azul distinta. Se intervienen la entrada, el registro y el historial del mismo recorrido estudiantil.

- RF-030-01. Usar el encabezado, navegación, tipografía y colores de CliniTENS. La entrada reúne búsqueda por código SIM y pacientes de práctica en un mismo nivel en escritorio, con búsqueda primero en pantallas estrechas. El listado conserva acciones por paciente y ordena los códigos SIM.
- RF-030-02. Organizar el registro en identificación, signos vitales, procedimientos y cierre. Mantener visibles el estado, el acceso al historial y las acciones correspondientes. El historial muestra cada paciente, fecha, estado y acciones con la misma presentación.
- RF-030-03. Conservar permisos, rutas, POST con CSRF, recuperación de borradores, validación, cálculos, cierre, PDF e impresión. Los formularios con errores deben conservar lo ingresado y mostrar cómo corregirlo.

La aceptación se verifica en Chrome a 1440, 768 y 390 px, con foco de teclado y contenido dentro del ancho disponible. No se requieren migraciones. La pantalla de preparación docente usa el diseño común desde antes de este cambio.
