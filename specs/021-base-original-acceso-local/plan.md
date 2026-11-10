# Plan — 021

Usar sqlite3 backup API con conexión fuente URI mode=ro. Consultar en la copia esquema, migraciones aplicadas, cuentas (sin password) y conteos de tablas funcionales. Crear respaldo inmutable y destino local sin sobreescribir archivos existentes. Comparar conteos/identidades antes y después de migrar y mantener secretos fuera de informes Git.

Añadir configuración local optativa sobre settings normales, permitiendo omitir read_env; secreto nuevo local ignorado, debug solo localhost y cookies diferenciadas. No reutilizar MD5/test_settings con registros originales. Revisar hashers y recuperación/cambio de contraseña actuales; reutilizar los formularios y vistas existentes en lugar de duplicar gestión.

Ensayar migraciones en una copia descartable del respaldo antes de aplicarlas al destino local. Reversión: detener servidor local y restaurar respaldo verificado tras conservar cualquier trabajo posterior. No eliminar datos automáticamente ni tocar el archivo de OneDrive.
