# 002 — Corrección de observaciones de CliniTENS

Fecha: 2026-10-08. Implementación y validación autorizadas explícitamente por el usuario para todas las observaciones. Se conserva la spec 001 como escaneo histórico.

## Problema y alcance

Resolver OBS-001 a OBS-023 con controles de servidor, pruebas ficticias y documentación actualizada. No desplegar, aplicar migraciones sobre la SQLite recibida, leer secretos/medios, hacer commit/push ni reescribir historial Git. No construir los módulos solamente anunciados en portadas: identificarlos como pendientes, sin enlaces engañosos.

## Reglas confirmadas

- MANAGER gestiona sus propios casos, códigos, pacientes y cursos; ADMIN y superusuario activos tienen acceso global.
- Si un código tiene curso, el estudiante debe estar matriculado. Código sin curso conserva compatibilidad para actividades abiertas. Docente asignado corresponde al creador del código y no puede reasignarse a voluntad.
- Para enviar: identificación del paciente y contenido en las 13 secciones; las otras 12 pueden declararse explícitamente No aplica. Se preservan borradores incompletos.
- Proteger superusuarios por atributo is_superuser, nunca por PK de un cargo. Administración de cuentas/cargos administrativos reservada a ADMIN/superusuario. MANAGER puede importar/matricular estudiantes en sus cursos, sin gestionar privilegios globales.

## Requisitos / aceptación

| RF | Resultado requerido | Observaciones |
|---|---|---|
| RF-002-01 | Migraciones disponibles, base/medios ignorados y retirados del índice sin borrar datos; historia previa documentada | 001/002 |
| RF-002-02 | Settings aislados, tests de permisos/datos/estados/imports y reproducción de fallos antes de corregir | 003 |
| RF-002-03 | Cuentas protegidas; catálogo/curso filtrado en vistas, formularios y descargas; superusuario coherente | 004/005/006/012 |
| RF-002-04 | Esquema JSON, secciones/tipos/límites, completitud y guardado sin sobrescritura silenciosa | 007/008 |
| RF-002-05 | Rúbrica estricta y borrador separado; publicación completa/atómica; datos publicados consistentes | 009 |
| RF-002-06 | Archivos validados por servidor y resultados diagnósticos publicados/habilitados visibles en caso y descargas privadas | 010/013/018 |
| RF-002-07 | Importación valida identidad/errores; credenciales de descarga únicas/caducables desde servidor; cambio obligatorio de contraseña; Excel literal | 011/015 |
| RF-002-08 | Actividad sin procesar imagen ni N+1; métricas reales; seguimiento periódico seguro | 014/019/020 |
| RF-002-09 | Tailwind incluye fuentes reales y build conserva salida si falla; portadas distinguen pendiente; textos en español | 016/017/021 |
| RF-002-10 | Logout POST, configuración de correo/seguridad explícita, HTML clínico sanitizado, notificaciones como texto | 018/023 |
| RF-002-11 | Cada OBS actualizada con evidencia/límites, trazabilidad y recuperación; 022 conserva solución documental | 022 y todas |

Validar acceso anónimo/inactivo/sin perfil, estudiante, MANAGER propietario/ajeno, ADMIN y superusuario. Ninguna cuenta ajena modifica superusuario desde gestión o admin Django. JSON/archivos/puntajes incorrectos no cambian persistencia. Guardados obsoletos devuelven conflicto; envío bloquea posteriores cambios. Borrador de rúbrica no modifica publicación previa. Resultados ocultos no se descargan por URL directa. Importación fallida no deja perfiles/cargos alterados. Credenciales manipuladas/expiradas/reutilizadas se rechazan.

## Compatibilidad y límites

Cambios de esquema aditivos: curso opcional en código, habilitación diagnóstica, versión de ficha, borrador de evaluación y marca/caducidad de contraseña temporal. No hay migración de datos personales ni borrado. Se generarán migraciones para revisión/aplicación posterior respaldada. El retiro de archivos del índice no elimina copias históricas; purgarlas requiere decisión específica posterior.
