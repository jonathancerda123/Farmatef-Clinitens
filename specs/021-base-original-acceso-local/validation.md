# Validación — 021

Fecha: 2026-11-10. Rama jonathan. Autorización explícita del usuario para usar datos originales y crear cuentas de prueba. No commit/push.

- Fuente SQLite abierta en modo lectura con backup API. Respaldo original consistente, copia previa de migración y copia de ensayo en `.test-artifacts/original-021`, todas ignoradas. Destino operativo `db.sqlite3` inicialmente inexistente; no se reemplazó un archivo previo. quick_check=ok.
- Inventario privado: 10 cuentas originales (4 activas), dos casos clínicos tradicionales, dos pacientes, cinco fichas, un curso. No se consultaron hashes/contraseñas originales ni semillas MFA; conteo MFA cero. Datos e inventario de cuentas no versionados. Estados, nombres y privilegios originales conservados.
- Plan de migración: únicamente `CliniTensSimulacionApp.0007_atencionenfermeria`. Aplicada primero al ensayo; conteos de todas las tablas funcionales originales conservados. Después aplicada al destino respaldado. Origen OneDrive intacto, sin aplicación de migraciones allí.
- Configuración nueva `core.local_runtime`: usa settings normales, sin read_env, DB de trabajo, hashers normales, secreto generado local ignorado, localhost y cookies distintas del demo. No importa core.test_settings; la variable CLINITENS_TEST_DATABASE no selecciona la base operativa. Debug local no es configuración productiva.
- Tres cuentas nuevas ADMIN/MANAGER/RESTRICTED sin superusuario, con credenciales aleatorias temporales 24 h y cambio obligatorio. Contraseñas y nombres de cuentas originales entregados en archivo local ignorado; no aparecen en HTML ni documentación Git. No se reasignaron cursos, pacientes o historiales.
- Login allauth por POST con cada cuenta nueva: 302; navegación lleva a cambio obligatorio y formulario responde 200. RequestFactory verifica búsqueda/gestión ADMIN y rechazo de MANAGER/RESTRICTED. No se afirma que el docente nuevo vea datos de otro responsable.
- En la copia de ensayo, usuarios exclusivamente sintéticos: alta mediante Register, búsqueda por username, activación/desactivación, edición del perfil propio y cambio de contraseña; obligación se elimina tras cambio correcto. Primer intento del harness asumió paginator sobre un queryset y falló; comprobación corregida y recorrido correcto. No se alteraron las contraseñas originales para probarlo.
- Check Django local sin incidencias; 66 regresiones Django con core.test_settings correctas. Comprobación final operativa: todos los conteos funcionales previos permanecen iguales salvo auth_user/Profile (+3); integridad ok. Las sesiones e EmailAddress nuevos son auxiliares del acceso de prueba.

## Límites y recuperación

No se inspeccionaron ni copiaron medios recibidos; adjuntos/avatar referenciados en SQLite necesitan el almacenamiento original para mostrarse. Base e imágenes son artefactos diferentes. Juan y los escenarios demo no se mezclaron con el destino. La base original no contiene casos del nuevo recorrido; deben prepararse con curso y matrícula.

No se arrancó un servidor persistente ni se revisaron registros originales en navegador; los checks de acceso se hicieron con cliente Django local. No se enviaron correos ni se probaron SMTP, red productiva, todas las búsquedas clínicas o todos los registros heredados. Las funciones de edición son las existentes (perfil propio y gestión de acceso por ADMIN); no se añadió edición administrativa global ni recuperación de contraseñas por pantalla nueva.

Para recuperar: detener el servidor local, conservar una copia de cualquier trabajo nuevo y restaurar el respaldo compatible en `db.sqlite3`; revisar cambios posteriores antes de reemplazarlo. No ejecutar reversión de esquema destructiva. El archivo recibido permanece disponible como fuente intacta.
