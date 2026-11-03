# Decisiones — CliniTENS

## Acuerdos de esta entrega

| ID | Fecha | Decisión | Fuente / motivo | Estado |
|---|---|---|---|---|
| D-001 | 2026-10-07 | Escanear y adaptar Markdown sin corregir implementación | Petición del usuario y fase documental de AGENTS | Aplicada |
| D-002 | 2026-10-07 | Renombrar OBSERVACIONES_BASE a OBSERVACIONES_PROYECTO | Usuario permitió renombrarlo; identifica el informe real | Aplicada |
| D-003 | 2026-10-07 | Registrar spec 001 como alcance documental y línea base observada | Evitar convertir código actual o hallazgos en requisitos aprobados | Aplicada; aceptación pendiente |
| D-004 | 2026-10-07 | Verificar con configuración efímera y datos ficticios | Preservar .env, base y medios del usuario | Aplicada |

## Acuerdos de implementación — 2026-10-08

| ID | Decisión | Fuente / estado |
|---|---|---|
| D-005 | Implementar correcciones OBS-001 a OBS-023 | Autorización explícita del usuario; spec 002 |
| D-006 | MANAGER por autor; ADMIN/superusuario global | Respuesta del usuario: «Separar por docente; ADMIN/superusuario global» |
| D-007 | Envío con identificación y 13 secciones completas/No aplica | Respuesta del usuario: «Exigir identificación y 13 secciones completas o No aplica» |
| D-008 | Proteger root por is_superuser; sin depender de PK de cargo | Intención del usuario en OBS-004; vistas y admin implementados |
| D-009 | Código con curso exige matrícula; sin curso compatibilidad abierta | Propuesta respondida por usuario; FK aditiva, sin reasignación de datos |
| D-010 | Versiones CAS y borrador independiente de publicación | Decisión técnica para SQLite/rúbrica; regresiones correctas |
| D-011 | Tokens efímeros, un uso/10 min; contraseña temporal 24 h/cambio obligatorio | Decisión técnica de corrección de credenciales; sin envío a terceros |
| D-012 | Retirar base/media del índice, conservar local/historia | Corrección autorizada; purga histórica excluida |
| D-013 | Conservar Tailwind 3, actualizar dependencias compatibles y servir JS local | Convención explícita del proyecto; 8 avisos de build restantes en OBS-024 |

## Decisiones visuales — 003

| ID | Decisión | Fuente / estado |
|---|---|---|
| D-014 | Rediseñar todas las pantallas de producto conservando flujos y priorizando computador | Petición explícita del usuario, con las tres skills locales; implementada/verificada, aceptación visual humana pendiente |
| D-015 | Una estructura común, petróleo/verde clínico, tipografía local y marca de ficha | Elección de diseño documentada antes de implementar; tokens y guía visual, sin nuevas dependencias |
| D-016 | Conservar Django/Tailwind 3 frente a instrucciones genéricas de Tailwind 4 en frontend-design | Stack e instrucciones reales del proyecto prevalecen; skills del usuario preservadas |

## Decisiones operativas pendientes

Aplicación respaldada de migraciones, hosting/SMTP/proxy privado/caché compartida, tratamiento de historia/remotos y resolución de dependencias de build. La verificación no sustituye aceptación pedagógica ni autorización de despliegue.

## Actualización autorizada — 004

| ID | Decisión | Fuente / estado |
|---|---|---|
| D-017 | Migrar a Tailwind 4.3.3/CLI y actualizar bibliotecas | Petición explícita del usuario supersede D-013/D-016 para este alcance; historial conservado |
| D-018 | Django 5.2.18 LTS frente a 6.1.2 última rama | Soporte prolongado, compatibilidad y regresiones; allauth/Axes adaptados |
| D-019 | Probar en target separado, conservar .venv y datos recibidos | Skill validar-produccion-sdd; auditor separado, sin migración real |
| D-020 | Overrides watcher 2.6.0/parser 7.1.6 y fuentes CSS explícitas | Elimina avisos del lock; build/regresiones/UI correctos; sin --force |
| D-021 | Mantener wrapper CKEditor último estable y registrar aviso del bundle | No sustituir integración por un build no validado; HTML inseguro no habilitado; cierre requiere proveedor/build corregido |
| D-022 | Conservar AutoField del paquete de sesiones y formularios MFA defaults | Compatibilidad sin migración correctiva; TOTP y sesiones comprobados |

Los pendientes operativos actuales se detallan en VALIDACION_PREPRODUCCION.md, incluyendo runtime parcheado, bundle editor y custodia de semillas MFA. El cierre de OBS-024 corresponde al lock npm del tema.

## Modales con Tailwind 4 — 006 / 2026-10-21

| ID | Decisión | Fuente / estado |
|---|---|---|
| D-023 | Entregar documentación y detenerse antes de implementación | El pedido menciona implementación menor al inicio, pero cierra con prohibición de código e instrucción de esperar revisión posterior. Aplicada a esta entrega; código pendiente de instrucción posterior |
| D-024 | Abrir 006 por alcance transversal y proponer corrección mínima sobre consumidores reales | 06-cambios distingue ajuste pequeño de cambio transversal; existen patrones distintos en cuentas/pacientes. No modificar retrospectivamente evidencia 003/004 ni ampliar 005. Documentación aplicada; solución técnica propuesta, pendiente de reproducción/revisión |

La falta de margen automático en `dialog.account-dialog` es hipótesis técnica, no diagnóstico confirmado. No se decide una unificación global de modales ni actualizar dependencias. La ausencia de `.git` impide verificar diferencias con commits históricos; se preservan los archivos presentes. No cambian constitución ni reglas de permisos.

### Ejecución posterior de 006 — 2026-10-21

| ID | Decisión | Fuente / estado |
|---|---|---|
| D-025 | Implementar 006 después de revisión documental | Usuario: «ya revisé, puedes implementar». Resuelve la espera de D-023; no autoriza despliegue/commit/push/datos recibidos |
| D-026 | Centrado acotado en cuentas y diálogo nativo solo para el consumidor de pacientes | Cuentas en (0,0) y foco detrás de pacientes reproducidos en navegador. Implementado; no se activa el componente sin uso ni se impone cambio global |
| D-027 | Invalidar consultas previas y conservar error/cierre dentro del diálogo de pacientes | Cuatro regresiones fallaron antes del parche y pasan después; evita datos viejos o cierre de una consulta nueva. Cinco pruebas específicas finales incluyendo clic exterior |

El párrafo de hipótesis anterior corresponde a la documentación inicial; la reproducción y evidencia nuevas están en [validación 006](../specs/006-modales-tailwind4/validation.md). Python instalado + paquetes locales permitió pruebas aisladas sin reparar el launcher anterior. Zoom 200%/emulación de movimiento reducido y aceptación final siguen pendientes; no se trasladan resultados a 005 ni a preparación productiva.
