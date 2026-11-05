# 017 — Flujos diferenciados: DAU, laboratorio y Centro de Apoyo Diagnóstico

Fecha: 2026-11-05. Estado: autorizado para implementación local por solicitud explícita de la usuaria. Revisión humana pendiente. Área: `CliniTensSimulacionApp` y portada CliniTENS.

## Problema y resultado

La preparación docente y la práctica no expresan todavía procesos distintos. La usuaria define tres módulos: DAU con signos vitales/procedimientos y cierre; Laboratorio con órdenes y etiquetas individuales por tubo; y Centro de Apoyo Diagnóstico (CAD), en reemplazo visible del Kardex, para resultados de laboratorio, imágenes diagnósticas, ECG e informes.

## Alcance y exclusiones

- Diferenciar las páginas docentes y de estudiante, conservando DAU y sus registros existentes.
- Estructurar órdenes de laboratorio por examen, muestra y tubo; agrupar órdenes por tubo para registrar recolección y emitir/imprimir una etiqueta educativa tubo a tubo.
- Permitir al docente preparar resultados ficticios CAD de las categorías laboratorio, imagen, ECG e informe; el estudiante revisa cada elemento y registra su revisión.
- Renombrar portada y navegación de Kardex a CAD. Mantener los modelos/eventos Kardex históricos sin borrarlos ni reutilizarlos como resultados.
- Mantener curso, matrícula, propietario, bloqueo de casos publicados y datos exclusivamente ficticios. Sin interpretación clínica automática, datos reales, carga de imágenes de pacientes, despliegue, commit/push ni migración de la base recibida.

## Permisos por acción

| Acción | Anónimo | RESTRICTED | MANAGER | ADMIN/superusuario activo | Propiedad/curso |
|---|---|---|---|---|---|
| Preparar órdenes/resultados | Denegado | Denegado | Permitido | Permitido | Cursos visibles; borrador propio o autorizado |
| Publicar caso | Denegado | Denegado | Permitido | Permitido | Caso de curso visible |
| Registrar tubos/revisión CAD | Denegado | Permitido | Denegado | Denegado | Caso publicado con matrícula propia |
| Ver intentos estudiantiles | Denegado | Solo propio según rutas existentes | Permitido | Permitido | Cursos visibles; revisar alcance existente |

## Flujo, datos y reglas

1. El docente crea caso base ficticio y configura DAU, órdenes de laboratorio y resultados CAD desde accesos independientes.
2. Una orden tiene identificador estable, nombre del examen, tipo de muestra y tipo/color de tubo. Órdenes del mismo tubo se agrupan en una sola etiqueta; el avance y la etiqueta pertenecen al estudiante/caso.
3. Etiquetas muestran solo código SIM, identificador de tubo, muestra y exámenes asociados; se imprimen en tamaño fijo legible con marca educativa.
4. CAD separa resultados por categoría y contenido textual ficticio. No interpreta valores ni exige que el alumno infiera un diagnóstico. Imágenes se representan como material educativo ficticio sin fotografías de personas.
5. Se valida en servidor IDs, número de filas y longitudes. Casos publicados quedan bloqueados. Se conservan intentos/eventos y contenido histórico.

## Requisitos y aceptación

- RF-017-01: DAU sigue mostrando registro de signos vitales, procedimientos acumulables, cierre e historial/PDF educativos.
- RF-017-02: el laboratorio muestra órdenes estructuradas, agrupadas por tubo; el alumno puede registrar cada tubo y obtener su etiqueta individual.
- RF-017-03: CAD presenta resultados diferenciados de laboratorio, imágenes, ECG e informes; el alumno puede registrar la revisión individual.
- RF-017-04: portada, navegación, gestión docente y práctica estudantil usan el nombre Centro de Apoyo Diagnóstico y no presentan Kardex como tercer módulo vigente.
- RF-017-05: propietario, publicación, matrícula y privacidad se validan en servidor; el esquema es aditivo y no modifica la base recibida.

| RF | Dado / cuando | Entonces | Caso negativo |
|---|---|---|---|
| 01 | Abrir práctica DAU | Signos, procedimientos y cierre disponibles | Caso ajeno/no matriculado denegado |
| 02 | Caso con varios exámenes por tubo | Se ve una etiqueta por tubo agrupado y su avance propio | ID manipulado o tubo inexistente rechazado |
| 03 | Caso CAD con las cuatro categorías | Cada elemento aparece agrupado y admite revisión propia | Alumno no inscrito y docente sin rol estudiante denegados |
| 04 | Abrir portada y páginas docentes | Nombres y recorridos específicos coinciden con el módulo | Ruta antigua no reutiliza contenido CAD como Kardex |
| 05 | Migración y guardado | Valores por defecto conservan compatibilidad histórica | No se aplican migraciones a base normal/recibida |

## Compatibilidad, decisiones y revisión

La decisión de manejar imagen diagnóstica como descripción/representación educativa evita subir datos de pacientes y medios. Los eventos Kardex ya guardados se conservan como historia y quedan fuera del nuevo CAD. Los cambios persistentes previstos son JSON aditivos con migración nueva; backup y reversión se documentan, y la migración se ensaya solo en la base en memoria de `core.test_settings`. Aceptación de uso y revisión docente quedan pendientes.
