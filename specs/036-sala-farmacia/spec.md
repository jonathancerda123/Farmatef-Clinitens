# 036 — Sala de farmacia y localización después de dispensar

Implementación autorizada por solicitud explícita de la usuaria del 2026-11-24, verificada localmente con datos ficticios. La autorización posterior «autorizo» permitió crear/verificar el respaldo y aplicar únicamente FarmaTEF.0011 a la base local; operación completada. Aceptación docente y configuración de la sala pendientes. Sustituye 033; preserva inventario, recetas, entregas e historial. Sin autorización de despliegue, commit o push. Se usa 036 porque otro chat creó 035-demo-render-gratuita durante este trabajo; sus documentos se conservan.

## Observado

033 está integrada: distribuye automáticamente productos en cuatro muebles y presenta envases ilustrados. No persiste distribución física ni permite configuración docente. La práctica registra una dispensación atómica antes de volver al resultado; `responder_receta` devuelve la respuesta. La matrícula y el creador de la receta delimitan el inventario consultable. Existen cambios locales de 033/034 y otras tareas que se preservan.

## Decisión de producto

Apartado propio «Sala de farmacia» dentro de FarmaTEF, con acceso docente desde su portada y enlace desde Inventario. No crear una app Django separada ni mezclar la distribución física con las operaciones de stock. Una sala por propietario del inventario en esta entrega; varios muebles por sala. Los alumnos de un curso consultan por separado las salas de los creadores de sus recetas, conservando la política de 033. Un colaborador de recetas no adquiere permiso sobre la sala/inventario ajenos. ADMIN/superusuario activos tienen gestión global explícita por propietario.

## Requisitos y aceptación

- SAL-01: docente Farmacia/Ambos configura ancho/largo de sala (2–30 m), posición, orientación en cuartos de vuelta y dimensiones de hasta 30 muebles. Seis tipos: estante deslizante, cajonera, mesa simple, pizarra, mesón con equipos de referencia y mesa con seis sillas. Medidas en cm; huella 2D con frente marcado y sillas incluidas. Sin escritura en pizarra ni dibujos de medicamentos.
- SAL-02: estante con tres columnas traseras/dos móviles, filas ajustables 1–12; cajonera con filas 1–12 y columnas 1–8. Los compartimentos se identifican establemente por mueble y clave. La interfaz frontal permite selección directa y descubre el fondo. Los demás tipos no admiten medicamentos.
- SAL-03: asignación por ID del medicamento registrado, mueble y compartimento; varios productos por compartimento y una ubicación por producto. Stock vigente calculado desde lotes; cero conserva ubicación y muestra «Sin stock». Producto sin asignación muestra «Ubicación pendiente»; no se reparte automáticamente por alfabeto. Inactivos no se presentan al alumno.
- SAL-04: guardar sala y asignar ubicaciones requiere autorización en servidor, CSRF y versión CAS. Rechazar muebles ajenos, asignaciones cruzadas, claves inválidas, medidas/tipos no válidos, fuera de límites, eliminación o reducción que invalide asignaciones. Un fallo no deja cambios parciales. Las superposiciones se advierten; no se implementa navegación ni cálculo de pasillos.
- SAL-05: alumno RESTRICTED activo consulta solo cursos matriculados e inventarios de creadores de sus recetas. No modifica configuración por POST ni URL directa. Mantener consulta opcional y tabla alternativa sin JS.
- SAL-06: después de una respuesta correcta con dispensación efectivamente registrada, redirigir automáticamente al localizador de esa dispensación propia; resaltar producto, mueble y compartimento. Recetas de varios productos permiten recorrer los medicamentos realmente entregados. Errores/rechazos no abren el localizador ni cambian stock. URL repetida es GET y no vuelve a dispensar. Si falta sala/ubicación, explicarlo y mantener acceso al resultado/comprobante/etiquetas. La entrega docente conserva su recorrido existente; la entrada automática corresponde a la práctica estudiantil solicitada.
- SAL-07: retirar vista/recursos de envases 033 y enlaces antiguos, conservando una redirección GET de compatibilidad hacia la sala estudiantil. Integrar layouts/tokens de FarmaTEF. SVG local de Anatomy, sin Three.js, WebGL ni dependencias de red; dibujar en 3D solo el mueble activo. Accesibilidad por teclado, adaptación móvil y movimiento reducido.

## Ampliación autorizada — zona de entrada / 2026-11-24

SAL-08: el docente puede añadir una zona «Entrada», ubicarla, orientarla y ajustar su ancho/fondo desde la distribución existente; el alumno la ve rotulada como referencia. Máximo una zona de entrada por sala, opcional para conservar las distribuciones previas. Mismos permisos, versiones y límites de sala; no admite asignaciones de medicamentos ni vista de mueble 3D. Se puede retirar si se cambia la distribución. No introduce cálculo de rutas ni modelado arquitectónico de puertas.

La zona se guarda como elemento `entrance` en MuebleFarmacia, reutilizando campos y tablas actuales. El campo de altura existente conserva un valor técnico y no se edita para esta zona. Añadir una opción a choices genera una migración de estado declarativa (0012); no agrega columnas ni transforma datos y la función usa el esquema 0011 ya activo. No aplicar nuevas migraciones a la base habitual bajo la autorización anterior limitada a 0011.

## Persistencia y exclusiones

### SAL-09 — aplicar distribución de la referencia

Autorizado por la solicitud explícita de dejar la sala del proyecto como la imagen adjunta. Referencia: sala de 1100 × 900 cm; cuatro estantes de 140 cm alineados arriba, mesón de 560 cm debajo, pizarra lateral izquierda, seis mesas en dos columnas/tres filas y zona Entrada junto a la pared inferior derecha. Conservar IDs de muebles compatibles y sus asignaciones de medicamentos; sin copiar recetas, stock, usuarios o contenido de la fixture. Aplicar solo a la sala/inventario local identificado, con respaldo verificado y servicio transaccional/versionado existente. No modificar otras salas ni aplicar migraciones.

Nuevas entidades SalaFarmacia, MuebleFarmacia y UbicacionMedicamento, migración aditiva 0011 sin datos iniciales automáticos. No se modifica ningún stock ni se mueve un dato histórico. Sala vacía hasta que el docente la configure. Migración probada en memoria/fixtures y aplicada a la base local después de respaldo y autorización separados; evidencia en validation.md. No se incorpora venta monetaria: se enlaza al flujo existente de dispensación simulada. Sin editor arquitectónico, paredes/puertas físicas, múltiples salas por inventario, importación de fotos o documentos, algoritmos de rutas ni aceptación de producción.
