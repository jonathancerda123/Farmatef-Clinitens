# Identidad y alcance del producto — CliniTENS

## Resumen

CliniTENS es una aplicación web para que una organización gestione actividades de simulación clínica, sus usuarios, materiales de trabajo y resultados. FarmaTEF es el módulo en desarrollo para organizar inventario farmacéutico simulado y recorridos de validación y dispensación.

El sistema está construido con Django y una interfaz renderizada en servidor. Reutiliza los componentes de identidad, permisos, fichas y gestión docente existentes en el repositorio. La instalación y sus servicios externos no se consideran productivos hasta que se completen las verificaciones operativas documentadas.

## Usuarios y responsabilidades

| Perfil | Responsabilidad prevista |
|---|---|
| Usuario participante | Acceder a sus actividades asignadas y registrar su propio trabajo dentro de los permisos concedidos |
| Gestor | Mantener actividades, materiales y participantes bajo su responsabilidad; revisar los resultados asociados |
| Administrador | Administrar usuarios y acceder globalmente a las funciones habilitadas |
| Responsable operativo | Acordar reglas de uso, catálogos, conservación de datos, niveles de servicio y aceptación de entregas |

Los nombres técnicos de cargos existentes son RESTRICTED, MANAGER y ADMIN. Los permisos se aplican en el servidor; la presencia de una opción en el menú no concede autorización. Los usuarios inactivos y anónimos no acceden a funciones protegidas.

## Capacidades existentes

- Gestión de cuentas, perfiles y cargos, con cambio obligatorio de contraseña inicial cuando corresponde.
- Gestión de actividades, códigos de acceso, cursos, participantes y materiales por parte de usuarios autorizados.
- Fichas estructuradas con estados de borrador, envío y calificación, guardado parcial y control de versiones.
- Revisión de fichas y publicación consistente de resultados y retroalimentación.
- Acceso a resultados y archivos condicionado por propiedad, rol, publicación y asociación con la actividad.
- Importación de participantes desde planillas y seguimiento de actividad en la aplicación.
- Interfaz común para los módulos CliniTENS y FarmaTEF.

Los detalles de acceso y restricciones se encuentran en el código y las especificaciones. La existencia de estas capacidades no certifica su preparación para una operación productiva.

## Alcance en desarrollo: FarmaTEF

FarmaTEF incluye gestión de inventario y recetas simuladas. El responsable del curso puede agregar docentes MANAGER activos como colaboradores para compartir la revisión y gestión de recetas FarmaTEF asignadas al curso. La colaboración no concede acceso a matrículas, fichas clínicas, resultados ni inventario ajeno. El docente puede asignar un caso al curso y configurar una pista visible y una clave reservada para evaluar la decisión estudiantil. Los estudiantes activos inscritos revisan la receta y eligen dispensar o rechazarla con motivo. Una decisión correcta de dispensación en un caso válido descuenta inventario simulado de forma atómica; los rechazos y errores no modifican el stock. El historial permite retirar recetas sin actividad; las respuestas y dispensaciones quedan protegidas.

La siguiente entrega funcional propuesta debe completar y demostrar un recorrido coherente de inventario y dispensación con datos ficticios:

1. Buscar o registrar un producto y sus lotes.
2. Consultar disponibilidad, vencimiento y alertas.
3. Asignar una receta de práctica a un curso y entregar al estudiante pistas verificables sin revelar la respuesta esperada.
4. Registrar la decisión y el motivo de rechazo; mostrar retroalimentación después de responder.
5. Descontar de forma atómica solo cuando una respuesta válida corresponda a dispensar; preservar el stock en rechazos o respuestas incorrectas.
6. Consultar el resultado; comprobante o etiqueta claramente identificado como simulado permanece pendiente.

La secuencia, las reglas de sustitución, cantidades, vencimientos, permisos y comprobantes requieren revisión con las personas responsables del producto antes de considerarse aceptadas.

## Límites y exclusiones

- FarmaTEF opera con catálogo, recetas, personas y transacciones ficticias. No procesa recetas reales ni realiza dispensación farmacéutica real.
- No se integra con farmacias, sistemas clínicos, servicios de identidad institucional ni proveedores externos.
- La integración de inteligencia artificial no está implementada. Cualquier generación asistida deberá tener proveedor, condiciones de privacidad, costo, trazabilidad y aprobación definidos. Una simulación debe identificarse expresamente.
- Las métricas de disponibilidad, rendimiento y servicio no están medidas ni comprometidas.
- Despliegue, operación productiva, migración de datos reales, respaldo operativo y aceptación del cliente requieren tareas y aprobación separadas.
- No se reasignan vínculos históricos de responsables, cursos, participantes o datos personales sin análisis específico.

## Datos y seguridad

El desarrollo y las demostraciones deben usar datos ficticios. Los permisos deben comprobarse en servidor para cada consulta y modificación, incluidas las rutas directas. Los archivos protegidos solo deben servirse tras comprobar la autorización sobre el objeto asociado.

No incluir secretos, tokens, contraseñas, datos personales reales ni contenido de bases locales en documentación, fixtures o capturas. Antes de operar con datos persistentes se debe acordar clasificación, acceso, conservación, respaldo y recuperación.

## Arquitectura y estado técnico

La aplicación usa Django 5.2.18 LTS, SQLite en el entorno local documentado y Tailwind 4.3.3 para estilos. El detalle de componentes, rutas, persistencia, permisos y límites de infraestructura se mantiene en [ARQUITECTURA_BASE.md](ARQUITECTURA_BASE.md).

FarmaTEF dispone de migraciones versionadas para inventario y recetas. Las migraciones 0003–0007 se aplicaron a la base local con respaldos documentados; no se aplicaron a producción. Los cambios 008–010 tienen checks básicos, pero falta verificar el recorrido funcional y visual con perfiles docentes y estudiantiles.

## Corrección transversal: modales

El 2026-10-21 se documentó el reporte de problemas en modales después de migrar a Tailwind 4. Tras revisión y autorización posterior, la [spec 006](../specs/006-modales-tailwind4/spec.md) corrigió el centrado de cuentas, reproduciendo antes su posición en (0,0), y sustituyó el overlay de pacientes por un diálogo nativo tras comprobar que el foco alcanzaba controles del fondo. Las consultas de pacientes descartan respuestas antiguas y muestran errores recuperables. Componente/helper sin consumidor localizado intactos; sin cambio de permisos o datos.

Pasaron 35 pruebas Django, 9 JS, build 4.3.3 y matriz de permisos; navegador a 1440/768/390 px. [Evidencia y límites](../specs/006-modales-tailwind4/validation.md): zoom 200%/emulación de movimiento reducido y aceptación funcional pendientes. Este cambio no sustituye ni valida el alcance FarmaTEF de 005. El launcher anterior sigue roto; 006 usó un Python instalado y paquetes locales con settings independientes, sin reparar entornos.

## Entrega funcional y aceptación

El siguiente hito es disponer de una versión demostrable para revisión de una organización usuaria. Antes de fijar fecha o declararla lista, se debe acordar:

- El recorrido prioritario y los perfiles que lo ejecutan.
- Reglas de inventario, receta, dispensación, comprobante y manejo de errores.
- Criterios de aceptación observables y datos de prueba.
- Entorno de demostración, respaldo y procedimiento de recuperación.
- Indicadores operativos que se medirán y responsables de aprobar el resultado.

Una entrega se considera aceptada cuando las personas responsables revisan el recorrido acordado y queda registrada la evidencia de los criterios cumplidos y los pendientes.

## Documentos relacionados

- [Estado actual y siguiente paso](ESTADO_PROYECTO.md)
- [Trazabilidad de requisitos](TRAZABILIDAD.md)
- [Arquitectura actual](ARQUITECTURA_BASE.md)
- [Especificación activa](../specs/005-farmatef-mvp-informe2/spec.md)
- [Plan de trabajo](../specs/005-farmatef-mvp-informe2/plan.md)
- [Tareas](../specs/005-farmatef-mvp-informe2/tasks.md)
- [Validación y límites](../specs/005-farmatef-mvp-informe2/validation.md)
- [Entorno y verificación](ENTORNO_Y_VERIFICACION.md)
