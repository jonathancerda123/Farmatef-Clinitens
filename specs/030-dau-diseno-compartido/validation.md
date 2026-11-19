# Validación — 030

Fecha: 2026-11-18. Verificación con `core.test_settings`, SQLite ficticio, Python 3.12.0, Django 5.2.18 y Chrome. Revisión del usuario pendiente.

| Requisito | Resultado |
|---|---|
| RF-030-01 | Tres pantallas con encabezado, navegación y colores compartidos de CliniTENS. En escritorio la búsqueda y la lista quedan al mismo nivel. En pantallas estrechas se apilan. Nueve pacientes de la demo ordenados por código SIM y acción de apertura por paciente. |
| RF-030-02 | Identificación y estado juntos, enlaces por sección, cálculos agrupados, acciones de guardado y cierre visibles según el estado. Historial con etiquetas de borrador y finalizado y acciones coherentes. |
| RF-030-03 | Recorrido con CSRF en Chrome: código inválido conservado y anunciado, apertura desde la lista, búsqueda del mismo código, PAM e IMC, guardar signos, agregar un procedimiento, guardar borrador, finalizar y consultar en modo lectura. Se verificaron las respuestas PDF para descarga e impresión. |
| RF-030-03 | DAU devuelve 403 al usuario anónimo y al docente. Un alumno ajeno recibe 404 en el registro y en el PDF. Estados vacíos de inicio e historial comprobados. Regresión Django para los tres formularios inválidos con errores asociados y valores conservados. |

- `manage.py check` y `manage.py makemigrations --check --dry-run`, con `--settings=core.test_settings`, correctos. En `manage.py test --settings=core.test_settings` pasaron 94 pruebas y una se omitió por requerir PostgreSQL.
- `node.exe .test-artifacts/dau-030/browser.cjs` probó las tres pantallas a 1440, 768 y 390 px, enfoque con teclado, un H1 por vista y ausencia de scroll horizontal de página. Capturas en `.test-artifacts/dau-030/`, incluidas `entrada-1440.png` y `entrada-390.png`.
- Chrome se comunicó con el cliente Django mediante un puente local. Las escrituras del recorrido ocurrieron en una copia de 8025. La prueba no comprobó el servidor HTTP en ejecución ni una impresora física.
- Los estilos específicos se cargan desde `static/css/dau.css` y usan los tokens, botones y controles compartidos ya compilados. El cambio prescinde de dependencias y migraciones.

Próxima revisión: abrir el DAU como estudiante en 8025 y recorrer búsqueda, registro e historial.

## Recuperación del puerto local

El 2026-11-18, tras un reporte de tiempo de espera, Windows mostró dos procesos Django de la misma demo en `127.0.0.1:8025`. Se verificó el ejecutable y los argumentos antes de reiniciar solo esa demo. Una instancia quedó escuchando con `core.test_settings`, `.test-artifacts/farmacia-025-fixture.sqlite3` y `manage.py runserver 127.0.0.1:8025 --settings=core.test_settings --insecure --noreload`. El inicio de sesión y el CSS actual del DAU respondieron con HTTP 200. El navegador integrado cargó el inicio de sesión después del reinicio. El DAU requiere una sesión de estudiante para abrirse.
