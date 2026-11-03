# Plan — 004

1. Capturar inventarios y auditorías del commit e56913c; ejecutar regresiones iniciales con core.test_settings. Evidencia en docs/evidencias/004-dependencias.
2. Consultar registros/documentación oficiales. Instalar herramientas de auditoría separadas; resolver candidatas en .test-artifacts/dependencias-004/target, conservando .venv. Frontend candidato aislado antes de modificar instalación de theme.
3. Actualizar pins/lock, migrar CLI/CSS/config de Tailwind 4 y adaptar settings allauth/Axes/interfaces que cambien. No tocar reglas/modelos ni ampliar features.
4. Ejecutar suite, check, dry-run, migraciones sobre base sintética, check de despliegue con settings normales aislados sin read_env y overrides explícitos. Recorrer navegador y revisar exportaciones ficticias.
5. Auditar conjunto final y documentar inventario completo, seguridad, compatibilidad, migraciones/recuperación y pendientes. No declarar operación productiva aprobada.

La prohibición anterior de migrar Tailwind automáticamente queda reemplazada para este alcance por el pedido explícito del usuario. Diagnóstico y actualización se registran por separado, conforme a la skill; el escaneo previo no se modifica retrospectivamente.
