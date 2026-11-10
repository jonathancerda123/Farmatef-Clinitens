# 021 — Datos originales y acceso local recuperable

Fecha: 2026-11-10. El usuario solicita usar las cuentas y datos originales, desconoce credenciales y autoriza cuentas adicionales de prueba. Autoriza revisar una copia de la base identificada en su mensaje y preparar uso local. No se cambia el archivo fuente ni las contraseñas originales. No se hace commit/push automáticamente.

RF-021-01: respaldo consistente SQLite desde origen en modo lectura; comprobar integridad y conservar otra copia antes de migrar. Destino operativo `db.sqlite3` ignorado en la carpeta de trabajo, inicialmente inexistente.
RF-021-02: inventariar cuentas por username/cargo/estado sin consultar ni mostrar contraseñas/hashes; conservar usuarios y registros originales y revisar migraciones antes de aplicarlas al destino respaldado.
RF-021-03: configuración local explícita que usa el destino original restaurado, hashers normales y permisos actuales, sin importar test_settings ni leer .env. Sesión/cookie distinta del servidor ficticio. Solo localhost; no es configuración productiva.
RF-021-04: crear cuentas nuevas ADMIN, MANAGER y RESTRICTED claramente identificadas de prueba, sin privilegio superusuario, con contraseñas aleatorias temporales de 24 h/cambio obligatorio. Entrega privada local, fuera de HTML/Git. No reasignar cursos ni datos originales a esas cuentas.
RF-021-05: verificar autenticación, cambio obligatorio, gestión/búsqueda de cuentas, perfil y visibilidad por curso/propiedad; prueba destructiva solo en memoria/base sintética. Sin cargar datos originales en fixtures, capturas o archivos versionados.

El paciente Juan de la base demo no se copia a la original. Usuarios ADMIN ven global según política actual; docentes acceden a sus cursos/datos, alumnos a matrícula propia. Que un docente no vea alumnos ajenos no es un fallo de búsqueda. Los medios originales no se copian ni abren; verificar disponibilidad separadamente con el usuario.
