# Revisión de preparación operativa — CliniTENS

## Resumen ejecutivo

La línea base de CliniTENS tiene evidencia técnica de pruebas y compilación en un entorno aislado. Esa evidencia cubre el conjunto de cambios de las specs 002–004 y no valida el incremento actual de FarmaTEF.

El sistema no está listo para una instalación productiva. El runtime Python configurado no inicia en este equipo; la migración de FarmaTEF aún requiere cotejo; y no se han verificado servicios reales de correo, proxy, almacenamiento, caché compartida, respaldo o restauración. No se realizaron despliegues ni migraciones sobre la base recibida.

Este informe es una revisión interna de preparación. No constituye certificación de seguridad, aceptación de usuarios ni autorización de despliegue.

## Alcance revisado

La línea base técnica incluye cuentas y perfiles, permisos, actividades, cursos, importación, fichas, rúbricas, resultados, archivos y frontend. FarmaTEF comenzó con inventario docente de medicamentos y lotes; recetas, dispensación, comprobantes y etiquetas todavía no están implementados.

No se inspeccionaron datos reales ni secretos. No se verificaron hosting público, correo SMTP real, almacenamiento externo, respaldo/restauración operativos, carga, integración clínica ni operación con usuarios reales.

## Entornos y límites del procedimiento

- El objetivo de dependencias está en `.test-artifacts/dependencias-004/target`; el `.venv` anterior se conserva con versiones antiguas y no debe usarse para ejecutar el código actualizado.
- El ejecutable Python del target apunta a una instalación inexistente bajo `C:\Users\Fernando\...`. Por este motivo, no se pudo ejecutar la validación técnica del incremento FarmaTEF.
- La línea base 004 registró Django 5.2.18, allauth 65.19.7, Axes 8.3.1, django-tailwind 4.5.0 y Tailwind 4.3.3.
- La configuración `core.test_settings` usa base/correo/caché en memoria y medios temporales. Está destinada exclusivamente a pruebas.
- Las comprobaciones de integración de la línea base usaron configuración y datos ficticios. No representan configuración del entorno destino.
- No se leyeron `.env`, `db.sqlite3` ni el contenido de `media/`.

## Evidencia de la línea base 004

| Control | Resultado registrado | Límite |
|---|---|---|
| Suite Django | 47 pruebas aprobadas | No cubre la totalidad del sistema ni valida FarmaTEF |
| Suite JavaScript | 4 pruebas aprobadas | No certifica todos los navegadores |
| `manage.py check` y dry-run de migraciones | Correctos en el entorno aislado | No se repitieron para el incremento FarmaTEF |
| `pip check` | Sin conflictos registrados | Comprueba consistencia, no vulnerabilidades |
| Compilación de Tailwind | Build final correcto en la línea base | No prueba la instalación actual del equipo |
| Auditorías Python/npm del conjunto inventariado | Sin avisos conocidos en los pins auditados | No incluye automáticamente runtime y bundle de CKEditor |
| Integración de autenticación | Se registraron 13 controles normales correctos | SMTP, proxy y destino real no probados |
| Migraciones de proveedores | Ensayadas sobre base ficticia | No revela conflictos de datos del destino |
| Navegador y documentos | Se revisaron flujos y exportaciones con datos ficticios | Matriz limitada de navegadores y tamaños; no es aceptación de usuarios |

Los registros detallados de la línea base están bajo `docs/evidencias/004-dependencias/` y en la [validación de la spec 004](../specs/004-actualizacion-dependencias/validation.md). No usar estos resultados para declarar validado el incremento actual.

## Hallazgos que requieren atención

| Hallazgo | Estado | Acción requerida |
|---|---|---|
| Runtime Python configurado no disponible | Bloquea la verificación del código actual | Instalar un runtime soportado/parcheado, crear un entorno aislado válido y repetir instalación, checks y suite |
| Migración `FarmaTEFApp.0001_initial` escrita manualmente | Pendiente de cotejo automático | Generar/cotejar la migración con el runtime correcto y aplicarla únicamente a una base ficticia aislada |
| Incremento FarmaTEF sin pruebas | No verificado | Probar altas, consultas, cálculos de stock/alertas y accesos permitidos/denegados, incluidos URLs directas |
| Bundle de CKEditor | La revisión 004 registró un aviso moderado condicionado en el bundle del proveedor | Actualizar a un bundle corregido y mantener auditoría separada; evitar habilitar configuración HTML amplia mientras tanto |
| Protección de semillas MFA | El adaptador predeterminado no cifra las semillas en la base | Definir protección en reposo y custodia de claves antes de usar datos persistentes |
| Proxy, TLS y HSTS | Topología y configuración destino no verificadas | Confirmar HTTPS, hosts, cabeceras de proxy confiables, cookies seguras y HSTS en el entorno elegido |
| Correo y recuperación de cuentas | SMTP real no probado | Configurar credenciales fuera del repositorio y probar entrega, expiración y recuperación |
| Caché de credenciales temporales | Solo caché local ensayada | Si hay varios procesos, configurar caché compartida con TTL y operación atómica; validar uso único y expiración |
| Archivos privados | El diseño requiere servir medios mediante autorización Django | Confirmar que el proxy no exponga `MEDIA_ROOT`; probar descargas permitidas y denegadas |
| Respaldo y restauración | No se hizo ensayo real | Definir responsables, frecuencia, retención y ejecutar una restauración controlada |
| Revisión de historia Git | No fue posible verificar el estado Git de este workspace | Revisar historia y remotos antes de distribuir el repositorio; no se afirma que haya ocurrido una exposición |

La referencia de seguridad de dependencias y sus fuentes están en [INVENTARIO_DEPENDENCIAS.md](INVENTARIO_DEPENDENCIAS.md). Los avisos de runtime, paquetes y bundles deben mantenerse diferenciados; una auditoría sin avisos en un conjunto no cubre los componentes excluidos.

## Criterios previos a una instalación persistente

Antes de proponer una instalación con datos persistentes, se debe contar con evidencia de lo siguiente:

1. Runtime compatible y parcheado, dependencias instaladas desde manifiestos y build reproducible.
2. `check`, dry-run de migraciones, pruebas automatizadas y pruebas funcionales de FarmaTEF ejecutadas en entorno aislado.
3. Migración cotejada y aplicada solo a una base ficticia, con revisión de esquema y plan de reversión.
4. Permisos por perfil y propiedad probados para solicitudes válidas e inválidas, incluidas rutas directas.
5. HTTPS, proxy, cookies, correo, caché y archivos configurados y comprobados en el entorno objetivo.
6. Respaldo y restauración demostrados, más registro, alertas y procedimiento de incidentes acordados.
7. Revisión de seguridad de los flujos implementados y resolución o aceptación explícita de los hallazgos abiertos.
8. Criterios de aceptación revisados por las personas responsables del producto y evidencia de una entrega funcional acordada.

La revisión debe realizarse sobre una copia respaldada y con autorización del responsable del entorno. No ejecutar migraciones, publicar ni cambiar datos reales como parte de una revisión documental.

## Referencias

- [Inventario de dependencias](INVENTARIO_DEPENDENCIAS.md)
- [Entorno, verificación y recuperación](ENTORNO_Y_VERIFICACION.md)
- [Arquitectura actual](ARQUITECTURA_BASE.md)
- [Estado del proyecto](ESTADO_PROYECTO.md)
- [Trazabilidad](TRAZABILIDAD.md)
- [Validación del incremento FarmaTEF](../specs/005-farmatef-mvp-informe2/validation.md)
