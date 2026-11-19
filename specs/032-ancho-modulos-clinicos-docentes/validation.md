# Validación — 032

Verificado el 18 de noviembre de 2026 en Chrome y Django con `core.test_settings` y una copia de la demo ficticia.

- RF-032-01. En la medición inicial, el borde derecho de los cuatro módulos quedaba 304 px antes que el de la tabla de Estudiantes a 1920 px. Después del ajuste, los dos bordes de la introducción y de las diez tarjetas de cada módulo coincidieron con los de la tabla a 1920, 1440, 768 y 390 px.
- RF-032-02. Las cuatro vistas se renderizaron sin desbordamiento horizontal en los cuatro tamaños. Los accesos directos respondieron con 200 para el docente y 403 para el alumno y visitantes sin sesión. Se revisaron las capturas de DAU en escritorio y móvil.

`node.exe .test-artifacts/ancho-032/browser.cjs` completó la comparación. Las capturas de escritorio y móvil están en el mismo directorio. `manage.py test --settings=core.test_settings` con el intérprete de `.test-artifacts/clinica-019-env` registró 94 pruebas aprobadas, una omitida por depender de PostgreSQL y cero problemas en el check de Django.

La demo 8025 se reinició. El inicio y la hoja de estilos respondieron con 200 y las cuatro rutas docentes devolvieron 403 sin sesión. Aceptación del usuario pendiente.
