# 004 — Actualización de dependencias y validación preproducción

2026-10-08. Autorización explícita del usuario: revisar y actualizar dependencias, incluidos Tailwind 3 a 4, allauth y recursos CDN, usando validar-produccion-sdd. Base main/e56913c, árbol inicialmente limpio. No autoriza despliegue, cambios de negocio, commit/push ni operación sobre datos recibidos.

## Resultado y alcance

Diagnóstico independiente del estado inicial; después actualización acotada en aislamiento. Conservar flujos, identidad de 003, permisos/estados de 002 y .venv anterior. Resolver versiones soportadas y avisos conocidos, fijar manifiestos/locks y registrar compatibilidad/evidencia antes y después. Revisar toda la aplicación implementada con OWASP Top 10:2025 y controles ASVS pertinentes, sin certificar cumplimiento completo.

## Requisitos verificables

- RF-004-01: inventario completo declarado/instalado/resuelto, versiones estables consultadas, candidatas compatibles y decisión por paquete; recursos externos identificados.
- RF-004-02: Tailwind 4 con fuentes acotadas HTML/Python/JS, CSS y assets locales reproducibles; conservar salida previa ante fallo, diseño y navegación/animación de 003.
- RF-004-03: framework soportado y autenticación/dependencias actualizadas; settings/interfaces adaptados sin abrir signup ni cambiar permisos/políticas. Suite y recorridos de login/logout/password/MFA compatibles.
- RF-004-04: auditorías Python/npm inicial y final, pip check, integración/migraciones/estáticos y exportaciones ficticias; defectos críticos y límites registrados con resultados reales.
- RF-004-05: informe global, inventario, trazabilidad y recuperación actualizados; conclusión distingue bloqueadores, evidencia insuficiente y pendientes de operación.

## Compatibilidad

Django 5.2 LTS preferido por soporte prolongado, con último parche compatible consultado; Python 3.12 se conserva. Tailwind 4 implica Chrome 111+, Safari 16.4+, Firefox 128+, conforme a guía oficial; no se garantiza compatibilidad con navegadores anteriores. Allauth y Axes pueden añadir migraciones de proveedor: ensayar en SQLite sintética y documentar su plan, sin aplicarlas a base recibida. No generar migraciones correctivas propias.

Sin nuevas funciones, despliegue, secretos, datos reales, envío a terceros ni purga histórica. La aceptación humana sigue pendiente.
