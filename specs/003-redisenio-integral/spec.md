# 003 — Rediseño integral de CliniTENS

2026-10-08. Implementación autorizada por el pedido explícito de una lavada de cara general, usando redesign-existing-projects, frontend-design y web-design-guidelines. Prioridad computador; adaptable a tablet/teléfono. Aceptación humana pendiente.

## Problema observado y resultado

Portada con fondo oscuro/gradientes, módulos con barras azules y formularios con estilos aislados. Tres estructuras de navegación y colores incrustados impiden reconocer una sola aplicación. El objetivo es un espacio de aprendizaje clínico coherente desde el acceso hasta la ficha y evaluación.

## Alcance

Acceso/recuperación, inicio, selección de módulos, docente (dashboard/catálogos/cursos/estudiantes/seguimiento/rúbrica), estudiante (ingreso/caso/editor/resultado), cuentas/perfil, mensajes y errores. Mantener Django/Tailwind 3, URLs, campos, CSRF, validaciones, permisos, filtros, estados y datos. Módulos pendientes siguen identificados como pendientes. Sin dependencias nuevas, cambios de persistencia, despliegue, commit/push ni lectura de .env/base/medios recibidos. Django admin técnico queda fuera del producto rediseñado.

## Requisitos verificables

- RF-003-01: navegación, marca, encabezado, tipografía, fondo y acciones compartidos en inicio y módulos. Página activa identificada; acceso a inicio/perfil desde los módulos.
- RF-003-02: portada y selector priorizan actividades reales, explican el contexto educativo y distinguen funciones pendientes sin métricas inventadas ni decoraciones genéricas.
- RF-003-03: catálogos, filtros, tablas, formularios y diálogos siguen una jerarquía común; errores generales/por campo visibles y valores preservados.
- RF-003-04: ficha de 13 secciones, No aplica, guardado/envío/estado y rúbrica mantienen sus contratos; lectura y acciones cómodas en computador.
- RF-003-05: escritorio 1280–1440, tablet y teléfono 390 px sin pérdida de acciones; navegación compacta, tablas desplazables identificadas, formularios fluidos.
- RF-003-06: acceso por teclado, foco visible, labels asociados, página activa, avisos con texto y movimiento reducido. No se declara certificación WCAG.
- RF-003-07: tokens centrales, CSS compilado y guía de personalización; verificación con datos sintéticos y evidencia antes/después.

## Permisos y compatibilidad

Se conserva íntegramente la política 002: MANAGER por autor, ADMIN/superusuario global, cuentas administrativas protegidas, estudiante propio/matrícula. El menú acompaña permisos de servidor. Ninguna migración nueva. Reversión mediante restauración de templates/CSS/JS de este cambio y recompilación, sin tocar SQLite/media.
