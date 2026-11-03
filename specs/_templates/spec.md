# <NNN> — <Cambio de CliniTENS>

Plantilla para solicitud futura; no representa alcance aprobado. Fecha: <real>. Estado: borrador. Fuente: <pedido>. Área: <UsuarioApp / homeApp / CliniTensDocenteApp / CliniTensFichaApp / transversal>. Código autorizado: NO hasta instrucción explícita. Revisión humana: pendiente.

## Problema, actores y resultado

<Necesidad observable y flujos a conservar. Consultar PROYECTO, ARQUITECTURA y OBSERVACIONES_PROYECTO; no transformar automáticamente hallazgos en requisitos.>

## Alcance y exclusiones

<Incluido, excluido, cambios de reglas y dependencias. Distinguir comportamiento actual de resultado deseado.>

## Permisos por acción/dato

| Acción | Anónimo | RESTRICTED | MANAGER | ADMIN | Superusuario | Propiedad/curso |
|---|---|---|---|---|---|---|
| <acción real> | <decidir> | <decidir> | <decidir> | <decidir> | <decidir por operación> | <filtro servidor> |

Considerar inactivo, sin perfil/cargo, acceso directo y archivos. Política 002: MANAGER por autor, ADMIN/superusuario activo global en panel; ficha estudiantil siempre propia. No inventar una excepción global.

## Flujo, datos y reglas

<Pasos, errores, tipos/límites, relaciones, unicidad, persistencia/auditoría. Si aplica ficha: 13 secciones y BORRADOR/ENVIADA/CALIFICADA; conservar esquema/completitud y versiones de 002. Código tiene curso opcional y exige matrícula si está asignado. Si afecta UI, leer PERSONALIZACION_VISUAL y reutilizar la estructura de 003. No incluir registros reales.>

## Requisitos y aceptación

- RF-<NNN>-01: CUANDO <evento>, EL SISTEMA <resultado verificable>.

| RF | Dado / cuando | Entonces | Caso negativo/límite |
|---|---|---|---|
| <ID> | <escenario> | <resultado> | <rechazo/recuperación> |

## Compatibilidad y no funcionales

<Flujos reales preservados, privacidad, usabilidad, volumen razonable y precisión acordada; no inventar SLA/certificaciones.>

## Decisiones y revisión

<Supuestos reversibles, decisiones críticas, observaciones relacionadas, fecha/motivo de cambios. No marcar aceptación ni autorización sin evidencia.>
