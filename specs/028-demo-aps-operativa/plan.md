# Plan — 028

1. Inspeccionar catálogo, lotes y matrícula de la demo. Respaldar con SQLite, comprobar integridad y usar una copia de ensayo con `core.test_settings`.
2. Asignar cantidades y mínimos por tipo de envase de práctica, con una distribución de vigencias y ejemplos deliberados de baja existencia. Verificar con las propiedades existentes de inventario.
3. Cargar las recetas y escenarios con modelos y formularios existentes. Mantener la identidad ficticia entre Ficha Clínica, DAU, RAE, Laboratorio y CAD. Registrar ejemplos individuales para la cuenta de estudiante simulada y preservar casos disponibles para iniciar.
4. Validar en la copia las rutas directas, la matrícula, las decisiones de dispensación y los historiales. Aplicar al destino respaldado y comprobar el resultado visible.

Para recuperar la demo previa, detener su servidor y restaurar el respaldo documentado sobre la fixture. No se requieren migraciones.
