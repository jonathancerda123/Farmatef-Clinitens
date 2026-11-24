# Plan — 036

SAL-09: identificar el propietario de la sala local mediante metadatos mínimos; preparar geometría exacta de la referencia (11 × 9 m), conciliar muebles por nombre/tipo conservando IDs/asignaciones, respaldar y ensayar sobre copia, aplicar con CAS y verificar coordenadas/conservación de ubicaciones. No transferir datos ficticios de la demo ni actualizar stock.

Ampliación SAL-08: reutilizar el registro de elementos de la sala para la zona de entrada; configurar ancho/fondo/posición/orientación, dibujar zona rotulada en plano, omitir frontal 3D y asignaciones, validar unicidad/límites y probar guardado/restauración. No modificar la migración 0011 ya aplicada. Preparar 0012 de choices sin aplicarla a la base habitual; no requiere columnas nuevas para su funcionamiento.

1. Inspeccionar estado Git, 033/034, inventario, permisos y retorno de dispensación. Documentar decisión y límites antes de código.
2. Persistencia normalizada y servicios de validación/CAS atómicos. Usar IDs estables y stock derivado de lotes, sin catálogo duplicado.
3. Vistas docente/administrador y consulta estudiantil, límites de propietario/curso. Destino de dispensación propia con selección de productos entregados; compatibilidad GET de vitrina.
4. Integrar plano 2D y mueble frontal aprobado con Anatomy local; formularios con CSRF/versiones, tabla alternativa, estados vacíos y ausencia de asignación. El docente edita y guarda; el alumno consulta.
5. Sustituir navegación y retirar la implementación gráfica antigua, preservando documentos históricos. Incorporar acceso desde inventario y resultado de dispensación.
6. Validar rutas directas, stock, transacciones, versiones, asignaciones, migración en memoria, JS, build y navegador ficticio; registrar evidencia y límites.

Diseño: fondo/superficie/texto y jade proceden de tokens.css; Segoe UI/Trebuchet del sistema. Plano dominante con controles docentes plegables y vista frontal del mueble activo; lista de medicamentos sin envases. Pintado SVG con profundidad y contraste entre fondo/móviles, sin bucles de animación en reposo. No añadir ilustración de todos los muebles en 3D simultáneamente.

Recuperación: migración aditiva sin carga ni transformación del inventario. 0011 se aplicó a la base local tras respaldo y autorización explícita; ubicación/hash registrados en validation.md. Para recuperar tras uso, detener escrituras y restaurar copia compatible y versión de código conjuntamente, preservando asignaciones nuevas mediante exportación/revisión; no revertir tablas a ciegas ni perder escrituras posteriores sin revisión.
