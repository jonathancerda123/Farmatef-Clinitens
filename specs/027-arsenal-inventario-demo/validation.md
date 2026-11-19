# Validación — 027

Fecha: 2026-11-18. Entorno: demo ficticia 8025, `core.test_settings`, SQLite, Python 3.12.0 y Django 5.2.18 en `.test-artifacts/clinica-019-env`. Aceptación humana pendiente.

| Requisito | Comprobación | Resultado |
|---|---|---|
| RF-027-01 | Extracción de tablas con `pdfplumber` y cotejo de nombre, forma, concentración y clasificación | 363 de 363 filas concordantes en siete páginas. PDF SHA-256 `6F30150792F992B05BBDAC332754C2C172E99F8327FB6F02F4A2F635EBE75247`. |
| RF-027-02 | Coincidencia de la captura con la demo ficticia | Cuatro lotes identificados por número, unidades y vencimiento. |
| RF-027-01 a RF-027-03 | `conciliar.py ensayo` y `conciliar.py demo`, en `.test-artifacts/arsenal-027` | Ambos actualizaron Paracetamol, Ibuprofeno, Loratadina y Amoxicilina en sus filas originales, incorporaron 359 presentaciones y conservaron Solución de simulación. Inventario final de 364 registros. |
| RF-027-02 | Comparar filas relacionadas antes y después, más `quick_check` y `foreign_key_check` | Se conservaron 7 lotes, 5 recetas, 5 líneas, 3 dispensaciones, 3 usos de lote y 5 respuestas. Integridad correcta. |
| RF-027-03 | Verificar las 359 altas y repetir la planificación en la misma transacción | Cero unidades y lotes, mínimo 0. La repetición reconoce las 363 presentaciones y propone cero escrituras. |
| RF-027-01 a RF-027-03 | `verificar_vista.py` sobre copia de la demo cargada | URL directa: docente propietario 200, estudiante 403 y anónimo 302. La tabla devuelve 364 filas, la búsqueda por Ibuprofeno 400 mg devuelve una y la búsqueda filtrada de Ácido Fólico devuelve tres. |
| RF-027-01 a RF-027-03 | `node.exe .test-artifacts/arsenal-027/verificar_chrome.cjs` | Chrome 1440×900. Se comprobaron los seis encabezados, los filtros, una coincidencia con su lote y tres altas sin lotes. Capturas `ibuprofeno.png` y `presentaciones-nuevas.png` en la misma carpeta. Chrome renderizó las respuestas de Django con los recursos estáticos locales mediante interceptación de solicitudes. Conectividad HTTP en vivo sin verificar. |

`manage.py check --settings=core.test_settings` y `manage.py makemigrations --check --dry-run --settings=core.test_settings` correctos. `manage.py test --settings=core.test_settings` encontró 94 pruebas: 93 pasaron y una quedó omitida porque requiere PostgreSQL.

El respaldo verificado es `.test-artifacts/arsenal-027/demo-antes-20261118T182833740630Z.sqlite3`. El destino es `.test-artifacts/farmacia-025-fixture.sqlite3`. La hoja de recuperación está en el [plan](plan.md). Próximo paso de revisión: abrir Inventario en la demo 8025 con el perfil docente y validar una presentación del arsenal.
