# Validación documental actual — spec 003, 2026-10-08

[Spec 003](../specs/003-redisenio-integral/spec.md), plan, tareas terminadas y [validación](../specs/003-redisenio-integral/validation.md) corresponden al rediseño autorizado. 001 conserva el escaneo y 002 las correcciones/políticas confirmadas.

| Control | Resultado |
|---|---|
| Alcance | Rediseño de producto con prioridad escritorio y adaptación móvil; Django admin, despliegue y persistencia excluidos |
| Requisitos / tareas | RF-003-01 a 07 trazados a componentes y evidencia; checklist terminado, aceptación humana pendiente |
| Auditoría | Defectos de navegación, formularios, móvil, cuentas y texto corregidos; decisiones estéticas distinguidas |
| Contexto técnico | Guía visual, AGENTS/README/arquitectura/estado actualizados; plantillas SDD corrigen referencias históricas a ausencia de tests/relación curso-código |
| Coherencia | Revisión final de 41 Markdown, enlaces relativos y fences; sin errores |
| Evidencia | 47 Django/3 JS, build, 91 HTML, GET por roles y navegador ficticio; límites explícitos |
| Preservación | .codex/ del usuario intacto; datos recibidos/secretos sin lectura; sin migraciones nuevas ni despliegue |

Próximo paso: revisión visual del usuario sobre capturas/diff. Guía de mantenimiento en [PERSONALIZACION_VISUAL](PERSONALIZACION_VISUAL.md); OBS-024/operación previa siguen pendientes.

---

# Registro documental de spec 002 — 2026-10-08

[Spec 002](../specs/002-correcciones-observaciones/spec.md) registra autorización y reglas confirmadas; plan, tareas y [validación](../specs/002-correcciones-observaciones/validation.md) corresponden al código implementado. La spec 001 se conserva como escaneo histórico.

| Control | Resultado actual |
|---|---|
| Alcance y reglas | Separación por docente, ADMIN/superusuario global; identificación y 13 secciones completas o No aplica |
| Trazabilidad | RF-002 enlazados a tareas, módulos y evidencia; OBS-001 a OBS-023 actualizadas individualmente |
| Contexto técnico | AGENTS/README/docs/prompts describen test_settings independiente, migraciones disponibles, medios privados y permisos reales |
| Estado y límites | Verificación local terminada; aceptación humana y migración/operación real pendientes; OBS-024 nueva registrada |
| Coherencia documental | 36 Markdown, enlaces locales y fences sin errores |
| Evidencia funcional | 47 tests Django y 3 JS; navegador y exportaciones ficticias revisados |

No se modifica la constitución académica ni se implementan módulos pendientes de portadas. Procedimiento de respaldo/recuperación y próximo paso en [entorno](ENTORNO_Y_VERIFICACION.md) y [estado](ESTADO_PROYECTO.md).

---

# Registro histórico de spec 001

El siguiente resultado es del 2026-10-07, previo a la autorización de implementación. Sus restricciones y cifras describen esa fase documental, no el estado actual.

# Validación documental SDD — CliniTENS

Fecha: 2026-10-07. Alcance: [spec 001](../specs/001-linea-base-clinitens/spec.md). Fase DOCUMENTAR; revisión del agente sobre petición del usuario y código en main/4126cc7.

| Control | Resultado / evidencia | Límite |
|---|---|---|
| Contexto y tecnología reales | README, PROYECTO y ARQUITECTURA describen apps/rutas/modelos existentes y Tailwind 3 | Descripción técnica; aprobación institucional pendiente |
| Requisitos y exclusiones | RF-001-01 a 05 y aceptación de spec documental | No son requisitos aprobados para arreglar aplicación |
| Plan y tareas coherentes | Solo inspección/Markdown/verificación; tareas vinculadas a RF | No hay implementación autorizada |
| Roles y datos | Matriz observada y relaciones reales; inconsistencias enlazadas a observaciones | Sin validar solicitudes directas ni reglas académicas |
| Hallazgos separados de acuerdos | 23 observaciones; propuestas en roadmap y decisiones pendientes | Riesgos estáticos sin explotación/reproducción |
| Estado/trazabilidad | ESTADO, TRAZABILIDAD, VERIFICACION y validation de spec | Aceptación del usuario pendiente |
| Referencias obsoletas | Se eliminó dependencia de contexto genérico ausente y comandos de core.test_settings | Menciones de ausencia son explicativas |
| Enlaces y preservación de código | 32 Markdown y 101 enlaces locales revisados, sin errores; Git conserva solo eliminación previa del RAR en archivos seguidos | Markdown originales sin seguimiento; no se compararon versiones históricas de esos documentos |

Checks técnicos en [VERIFICACION.md](VERIFICACION.md): 58 Python sin errores, 85 plantillas compiladas, check correcto, dry-run sin diferencias y **0 tests**. No confundir estos resultados con una validación de funciones clínicas o permisos.

Conclusión: kit adaptado a CliniTENS y hallazgos documentados. Revisión y aceptación humanas pendientes; correcciones requieren alcance explícito.
