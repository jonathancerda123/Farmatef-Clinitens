# Validación — 031

Fecha: 2026-11-18. Verificado con Django 5.2.18, `core.test_settings`, SQLite ficticio y Chrome.

| Requisito | Resultado |
|---|---|
| RF-031-01 | Chrome comparó ambas entradas a 1440, 768 y 390 px. Coincidieron la anchura y posición horizontal del buscador y la cuadrícula. Las tarjetas quedan debajo del buscador, en dos columnas a 1440/768 px y una a 390 px. |
| RF-031-02 | La entrada usa los estilos comunes. Chrome confirmó `dau.css?v=031` en el registro. Se reinició la demo 8025 sobre `.test-artifacts/farmacia-025-fixture.sqlite3`. El inicio de sesión y ambas hojas de estilos respondieron con HTTP 200. |
| RF-031-03 | Se comprobó el orden de los nueve códigos simulados, el foco, el error por código inválido, la apertura, la recuperación de borrador, el cierre, el historial, el PDF y los permisos. Las escrituras del recorrido se hicieron en una copia. |
| Demo en uso | La pestaña de Chrome con sesión estudiantil mostró el buscador centrado, el historial arriba y las dos primeras tarjetas en paralelo después de recargar. |

- `node.exe .test-artifacts/dau-031/browser.cjs` pasó con una copia ficticia y el puente Django de 030. Las capturas están en `.test-artifacts/dau-031/`.
- `manage.py test --settings=core.test_settings` pasó 94 pruebas y omitió una por requerir PostgreSQL. El check de la suite informó cero problemas.

Próxima revisión: abrir un registro desde una tarjeta de práctica en la demo 8025.
