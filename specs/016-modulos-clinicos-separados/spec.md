# 016 — Recorridos y preparación diferenciada para DAU, laboratorio y Kardex

Fecha: 2026-11-04. Estado: alcance documentado y autorizado por la petición explícita de distinguir funcionalidades y evitar que las tres tarjetas abran la misma preparación. Área: `CliniTensSimulacionApp`. La usuaria también indicó que urgencias debe seguir el proceso de sus capturas. Datos y ejemplos solamente ficticios.

## Problema y resultado esperado

Las tarjetas de DAU, laboratorio y Kardex dirigen al docente a una misma página que crea un caso integrado. Esto hace parecer que los módulos son iguales. Cada entrada debe abrir una vista de gestión identificada con su módulo y permitir preparar/actualizar su contenido propio dentro de los casos de curso. El estudiante debe abrir una práctica diferente por módulo: DAU con registro de atención, laboratorio con solicitud/resultados ficticios y Kardex con eventos cronológicos.

## Alcance

- Añadir una vista docente por módulo, filtrada por los cursos que el actor puede gestionar. Cada vista presenta sus datos específicos, ofrece actualizar el bloque correspondiente en casos existentes y enlaza a creación del caso base cuando aún no exista.
- DAU docente: mostrar y mantener paciente SIM (nombre, sexo, edad, nacimiento, comuna, antecedentes) y escenario DAU. No solicitar ni aceptar RUT.
- Laboratorio docente: mantener instrucciones ficticias del caso para preparar solicitudes/resultados; sin rangos de referencia clínicos inventados ni interpretación.
- Kardex docente: mantener indicaciones ficticias como lista de actividades de registro; sin dosis ni órdenes terapéuticas.
- Mantener el caso integrado y el control actual de publicación; no cambiar ni reasignar los cursos de casos existentes.
- Las tarjetas de área clínica para docentes llevan a rutas distintas. La práctica estudiantil mantiene el flujo DAU de spec 015, laboratorio y Kardex conservan formularios/eventos propios.
- Incorporar navegación de vuelta al módulo, resultados del docente e indicación clara del estado publicado/borrador.

## Seguridad y datos

Solo MANAGER propietario/colaborador autorizado y ADMIN/superusuario activo pueden cambiar contenido del caso dentro de los cursos visibles. Cada POST vuelve a comprobar pertenencia. Las páginas de estudiante siguen exigiendo publicación, matrícula y datos ficticios. No se permite alterar módulo/caso ajenos con una URL directa. No se accede a `.env`, a la base recibida ni a `media/` para preparar ejemplos.

## Aceptación

- RF-016-01: Las tres tarjetas docentes abren títulos y URLs diferentes para DAU, laboratorio y Kardex.
- RF-016-02: Cada vista muestra y actualiza solo los campos pertinentes a su módulo, conserva los demás bloques del caso y muestra errores junto al campo.
- RF-016-03: El acceso de escritura se valida por curso/propiedad en el servidor; anónimo, estudiante, curso no visible o caso ajeno no pueden actualizar.
- RF-016-04: La DAU estudiantil conserva flujo de identificación SIM, signos vitales, procedimientos, cierre, historial e impresión según spec 015.
- RF-016-05: Laboratorio estudiantil conserva solicitud y resultados ficticios independientes; Kardex conserva el historial de eventos y correcciones.
- RF-016-06: Las vistas se diferencian visualmente y se adaptan a móvil; revisarlas en navegador antes de aceptar.

## Límites

No se cambia el esquema de base si basta con formularios/vistas; no se modifica el estado global de publicación ni se crean cursos, casos o datos de pacientes por semilla. No se despliega, hace commit/push, ni se aceptan reglas clínicas. La aceptación visual/pedagógica queda pendiente de la usuaria y su docente.
