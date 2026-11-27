# 037 — Candado del plano, precios y movimientos de inventario

Fecha: 2026-11-26. Fuente: cambios solicitados por el profesor mediante la usuaria. Estado: implementación local autorizada por «autorizo» de la usuaria el 2026-11-26. Validación automática completada; navegador pendiente por fallo de conexión local. Aceptación docente pendiente.

## Observado

La sala 036 guarda geometría mediante CAS, sin bloqueo persistente. Medicamento tiene clasificación y forma farmacéutica, sin precio. InventarioView ya filtra por clasificación; el buscador incluye forma y principio activo. RegistroInventarioView crea lotes directamente. services._registrar_consumo_stock registra DispensacionLote al descontar, dentro de transacciones de entrega/respuesta. No existe un historial general de movimientos. Django admin permite editar unidades: debe protegerse para evitar cambios sin trazabilidad.

## Propuesta y supuestos revisables

Ampliar FarmaTEF existente, sin nuevas apps/dependencias. Aclaración de la usuaria del 2026-11-26: «el tipo es en base al vademecum», adjuntando Arsenal Farmacoterapéutico APS 2024–2026, Servicio de Salud Arica, siete páginas. El filtro debe usar los valores de su columna CLASIFICACIÓN, reutilizando clasificacion del catálogo importado por 007. Ejemplos: Arsenal básico, FOFAR, PROA, TBC, CPU, Teledermatologia, UAPO, PM Cardiovascular y PM Epilepsia; conservar también clasificaciones combinadas de urgencias tal como figuran en la fuente. No inferir grupos terapéuticos ni reclasificar por nombre o forma farmacéutica. Las columnas de forma, concentración y observaciones siguen separadas. Precio unitario propuesto en pesos chilenos (CLP). «Ingresos» se interpreta como entradas de unidades; no contabilidad financiera. Estos dos últimos supuestos siguen revisables.

## Permisos

MANAGER Farmacia/Ambos gestiona su sala/inventario y consulta su historial; ADMIN/superusuario activos tienen alcance global explícito por propietario. Enfermería, inactivos y usuarios sin cargo autorizado no gestionan. Anónimo requiere autenticación. Colaborador de recetas conserva dispensación autorizada sin adquirir ajustes/historial del inventario ajeno. Alumno conserva consulta de sala y entrega propia por matrícula, sin candado, ajustes o historial general. Comprobar GET/POST directo en servidor.

## Requisitos y aceptación

| ID | Resultado esperado | Negativo/límite |
|---|---|---|
| RF-037-01 | Botón con candado y texto Bloquear/Desbloquear plano; estado persiste tras recargar. Bloqueado impide mover, añadir, retirar, girar o redimensionar muebles y modificar medidas. | Rechazar también POST directo y formulario abierto antes del bloqueo. Alternar requiere CSRF, propiedad y versión CAS; sin cambios parciales. |
| RF-037-02 | Salas existentes empiezan desbloqueadas. Bloqueo protege geometría; consulta, selección de compartimentos, asignación de medicamentos y dispensación siguen disponibles. | Alumno/ajeno no alternan. Dos pestañas no sobrescriben estado: cambio de versión exige recarga. |
| RF-037-03 | Alta/edición autorizada permite precio CLP entero entre 0 y 999999999; listado muestra moneda. Productos anteriores quedan Sin precio hasta completarlos. | Obligatorio en nuevas altas. Rechazar negativos, fracciones y valores inválidos/fuera de límite. Cero es distinto de no informado; no inventar precios para catálogo previo. |
| RF-037-04 | Filtro Tipo de medicamento usa la columna CLASIFICACIÓN del arsenal adjunto y los valores importados en clasificacion; combina texto/alertas, permite limpiar y ofrece Sin clasificar. | Opciones solo del inventario visible; selección sin coincidencias muestra estado vacío; conservar clasificaciones combinadas sin dividirlas o reinterpretarlas. Forma farmacéutica y observaciones permanecen separadas. |
| RF-037-05 | Cada movimiento muestra fecha/hora, actor, medicamento/lote, entrada/salida, cantidad positiva, saldo anterior/posterior, motivo y observación; despacho enlaza dispensación. Historial paginado con filtros por medicamento/lote/motivo/fechas. | Inmutable en interfaz/admin; proteger borrado de objetos con historia. Corregir mediante movimiento compensatorio. No inventar operaciones anteriores a la activación. |
| RF-037-06 | Docente registra ingresos, ajustes de entrada/salida y retiros por vencimiento. Motivos: ingreso de inventario, ajuste de inventario, venta simulada, dispensación simulada, vencimiento y otro con explicación obligatoria. | Cantidad entera positiva; salida no supera saldo; vencimiento exige lote vencido. Paso del tiempo no descuenta automáticamente. Reenvío no duplica operación. |
| RF-037-07 | Alta de lote con unidades genera entrada; consumo docente/estudiantil genera salida por lote en la misma transacción. Receta usa Dispensación simulada; Venta simulada solo para salida manual expresamente seleccionada. | Error de historial revierte stock/entrega/respuesta y viceversa. Rechazo/error no genera salida. Reenvío no duplica. Admin no permite editar unidades saltándose el registro. |

## Persistencia y límites

Proponer bloqueo en SalaFarmacia, precio nullable para productos previos y MovimientoInventario con relaciones protegidas, identificador de operación y restricciones de cantidad/saldos. Conservar existencias; historial comienza en la activación y debe indicarlo. No fabricar saldos iniciales históricos ni redescontar dispensaciones anteriores. Precio histórico de venta, contabilidad, cobros, impuestos y cambios en PDF/etiquetas quedan fuera.

Migración aditiva 0013 generada/revisada y ensayada en memoria/fixture bajo .test-artifacts; depende de FarmaTEF 0012. Ambas pendientes en la base habitual. Aplicación a base habitual requiere autorización específica, respaldo consistente verificado y recuperación coordinada de código/base preservando escrituras posteriores. Sin despliegue, commit/push ni purga histórica.
