# Validación — 004

2026-10-08, main/e56913c inicialmente limpio; actualización explícitamente autorizada. [Informe global](../../docs/VALIDACION_PREPRODUCCION.md), [inventario](../../docs/INVENTARIO_DEPENDENCIAS.md) y [manifiesto de evidencia](../../docs/evidencias/004-dependencias/revision-manifiesto.json). Herramientas/fixtures en .test-artifacts, ignoradas; .venv anterior conservado. Sin lectura de .env/base/media recibidos, despliegue ni commit/push.

## Diagnóstico inicial

47 regresiones aprobadas en 0.569 s con entorno anterior. Django 5.1.2 fuera de soporte, allauth 0.62.1/Axes 6.4.0/Tailwind 3.4.19. pip-audit 2.10.1 sobre cincuenta pins instalados, sin pip/herramientas: 118 registros en diez paquetes, 66 avisos distintos al unir alias. npm: ocho paquetes afectados, cinco altos/tres moderados. JSON inicial preservado; exit inicial no conservado independientemente del comando posterior, no deducirlo de aquel conjunto.

## Actualización y compatibilidad

Django 5.2.18 LTS, allauth[mfa] 65.19.7, Axes 8.3.1 y bibliotecas candidatas actuales compatibles: 54 pins instalados/resueltos. Tailwind 4.3.3/CLI, seis directas exactas/lock, retiradas herramientas antiguas y overrides watcher/parser. Cero CDN externos; Alpine/DOMPurify ya actuales.

Adaptaciones: login/signup fields actuales (signup cerrado), formularios MFA defaults en lugar de rutas internas antiguas, AppConfig AutoField original de sesiones, argumentos Django/CLI, import/source/config y utilidades v4. El sandbox producía CSS incompleto con exit cero: control previo al reemplazo/regresión conservan salida anterior. Build final con lectura de templates correcto. Ninguna migración propia generada.

## Verificación final ejecutada

| Control | Resultado |
|---|---|
| Check / dry-run / pip check | Exit 0; sin incidencias ni cambios de modelos |
| Suite Django | 47 aprobadas, cero fallidas/omitidas, 0.541 s |
| JS/build | 4 aprobadas, cero fallidas/omitidas |
| Build integrado | Tailwind 4.3.3, exit 0/131 ms; componentes/utilidades servidos |
| Auditoría final | 54 pins Python/lock npm tema sin avisos conocidos, ambos exit 0; bundle CKEditor un aviso distinto moderado |
| Seguridad normal replicada | 13 controles correctos, incluye activación y desafío TOTP, Axes y sesiones |
| Check deploy réplica | W004 HSTS=0; perfil HSTS ficticio sin avisos; destino real no comprobado |
| Migración sintética | Base vacía aplicada; copia fixture anterior conserva cinco usuarios/dos fichas tras siete migraciones proveedor |
| Navegador | Login/logout/caso CKEditor/ficha/menu/Escape/SVG; 1440/768/390 sin desbordamiento del documento |
| Exportaciones | PDF actual dos páginas/identificación/12 No aplica y revisión visual completa; Excel dos filas/cuatro columnas/literales; visual 002 vigente por código/openpyxl sin cambios |

[Comandos/logs](../../docs/evidencias/004-dependencias/comprobaciones.json), [seguridad](../../docs/evidencias/004-dependencias/integracion-produccion-ficticia.json), [migración](../../docs/evidencias/004-dependencias/migracion-fixture-previa.json), [UI](../../docs/evidencias/004-dependencias/interfaz.json), [exports](../../docs/evidencias/004-dependencias/exportaciones.json).

## Límites y conclusión

Bibliotecas/manifiestos y compatibilidad implementados/verificados en target aislado. .venv sigue anterior: instalar manifests actuales en entorno parcheado antes de operación normal. No se probó runtime nuevo ni se migraron datos recibidos.

**Con bloqueadores para producción usando Python 3.12.0 actual**, más evidencia insuficiente del destino. Node patch LTS, bundle CKEditor 47.5.0 con aviso moderado condicionado, custodia MFA y operación pendientes en PRE-005 a PRE-009. Wrapper 0.2.20 ya es último estable; configuración no habilita HTML inseguro, sin explotación demostrada. Cero avisos del tema/Python no incluye bundle/runtime.

Sin aceptación humana ni permiso de despliegue. Próximo paso: runtime parcheado/revalidación y bundle corregido, después migraciones sobre copia/operación conforme al informe. Tareas marcadas reflejan trabajo ejecutado; pendientes no se convierten en pruebas aprobadas.
