# Entorno, verificación y recuperación — CliniTENS

Este documento describe cómo preparar un entorno aislado, verificar cambios y proteger los datos antes de operar el producto. Distingue la línea base previamente verificada de los cambios recientes que todavía no se han podido ejecutar.

## Estado del entorno actual

- La línea base 004 registró Django 5.2.18, allauth 65.19.7, Tailwind 4.3.3 y una suite de 47 pruebas Django y 4 pruebas JavaScript. Es evidencia de esa línea base, no de los cambios de FarmaTEF.
- El entorno de dependencias actual está en `.test-artifacts/dependencias-004/target`; el `.venv` anterior se conserva con dependencias antiguas.
- El ejecutable Python del entorno target no inicia en este equipo: busca una instalación bajo `C:\Users\Fernando\...` que no existe. No se han ejecutado `manage.py check`, pruebas ni cotejo de migraciones para FarmaTEF.
- `FarmaTEFApp.0001_initial` fue escrita manualmente para las tablas de medicamentos y lotes. El cotejo automático está pendiente y no se aplicó a la base recibida ni a otro entorno persistente.
- No se leyeron `.env`, `db.sqlite3` ni contenido de `media/`. La base y los medios recibidos no se modificaron.

## Preparación de entorno aislado

Antes de validar cambios:

1. Instalar un runtime de Python soportado y parcheado en una ruta local válida.
2. Crear o reparar un entorno virtual dentro del área de trabajo autorizada, sin reemplazar el `.venv` conservado.
3. Instalar las dependencias exactas de `requirements.txt` y ejecutar `npm ci` en `theme/static_src`.
4. Usar `core.test_settings` y una base/medios ficticios dentro de `.test-artifacts`.
5. Comprobar que la configuración aislada no acceda a `.env`, a la base recibida ni a `media/`.
6. Ejecutar las comprobaciones y registrar comandos, entorno, resultados y limitaciones en la validación de la spec correspondiente.

`core.test_settings` usa recursos temporales y no es una configuración de operación. No debe usarse para un despliegue real.

## Comandos de verificación

Cuando exista un intérprete válido, ejecutar desde la raíz del proyecto y con configuración aislada:

~~~powershell
<python-del-entorno> manage.py check --settings=core.test_settings
<python-del-entorno> manage.py makemigrations --check --dry-run --settings=core.test_settings
<python-del-entorno> manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp --settings=core.test_settings
<python-del-entorno> -m pip check
<python-del-entorno> manage.py tailwind --settings=core.test_settings build
node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs
~~~

El marcador `<python-del-entorno>` debe sustituirse por la ruta real comprobada. No copiar el launcher actual si continúa apuntando a la instalación inexistente. La sintaxis de Tailwind requiere que `--settings` aparezca antes del subcomando `build`.

Para la nueva app, revisar también las migraciones generadas, alta y consulta de medicamentos/lotes, cálculos de stock y alertas, y permisos permitidos/denegados por URL directa. Registrar los resultados antes de marcar requisitos como verificados.

## Datos ficticios y revisión de interfaz

Las pruebas funcionales y demostraciones deben emplear cuentas, medicamentos, lotes, recetas y movimientos ficticios. Mantener la base y los medios temporales dentro de `.test-artifacts`; confirmar antes de migrar que la ruta de destino está bajo esa carpeta.

Revisar la interfaz con los perfiles de usuario previstos, incluidos casos permitidos y denegados. Si se modifican PDF, planillas u otros documentos, verificar visualmente los archivos generados. Las pruebas de backend no demuestran por sí solas la correcta interacción visual.

## Migraciones y recuperación

La migración FarmaTEF es aditiva por diseño, pero aún debe cotejarse con el modelo usando el runtime correcto. Antes de ensayarla:

1. Usar una base vacía o fixture aislada dentro de `.test-artifacts`.
2. Revisar `showmigrations` y `migrate --plan` antes de aplicar cambios.
3. Respaldar la fixture y verificar que se puede restaurar.
4. Aplicar la migración únicamente a esa fixture.
5. Comprobar tablas, restricciones, altas y consultas; registrar evidencia.
6. Si falla el ensayo, detener las escrituras y restaurar la fixture desde el respaldo.

No aplicar, revertir ni probar migraciones contra la base recibida. Un futuro entorno persistente requiere una copia respaldada, evaluación de compatibilidad, plan de recuperación y autorización explícita de la persona responsable.

Para revertir una versión de código, identificar primero los archivos afectados, preservar cambios ajenos y restaurar conjuntamente código, configuración y respaldo compatible. No usar operaciones Git globales destructivas ni revertir migraciones a ciegas.

## Configuración de servicios para una instalación

- **Correo:** el backend local puede escribir en consola. SMTP requiere credenciales privadas, TLS, dirección de remitente y pruebas de entrega/recuperación de cuenta.
- **HTTPS y proxy:** configurar hosts, redirección HTTPS, cookies seguras y HSTS según la topología real. No confiar cabeceras de proxy que no estén verificadas.
- **Archivos:** `MEDIA_ROOT` debe permanecer privado. El servidor frontal puede exponer estáticos, pero no debe publicar directamente los medios protegidos.
- **Caché:** los tokens de uso único funcionan con caché local en un solo proceso; varios workers requieren caché compartida y operación atómica. No se ha validado un backend externo.
- **Base de datos:** SQLite corresponde al entorno local documentado. Seleccionar y probar el motor de producción según volumen, concurrencia, respaldo y recuperación requeridos.
- **Operación:** definir logs, alertas, límites, timeouts, señales de salud, respaldo y restauración antes de aceptar uso persistente.

No se han probado correo real, proxy de producción, almacenamiento compartido, restauración operativa, carga ni escenarios de caída de servicios.

## Límites conocidos

- La auditoría de dependencias de la línea base no cubre automáticamente el runtime del sistema ni todos los bundles de terceros.
- `pip check` comprueba consistencia de paquetes, no ausencia de vulnerabilidades.
- La suite existente no equivale a cobertura completa, pruebas de carga ni validación de reglas operativas de farmacia.
- Validación de extensión, tamaño o firma no reemplaza antivirus ni análisis de archivos maliciosos.
- Las métricas de disponibilidad y rendimiento deben medirse en un entorno definido; no son compromisos actuales.

## Referencias

- [Estado actual](ESTADO_PROYECTO.md)
- [Arquitectura](ARQUITECTURA_BASE.md)
- [Trazabilidad](TRAZABILIDAD.md)
- [Validación de FarmaTEF](../specs/005-farmatef-mvp-informe2/validation.md)
- [Inventario de dependencias](INVENTARIO_DEPENDENCIAS.md)
- [Preparación operativa](VALIDACION_PREPRODUCCION.md)
