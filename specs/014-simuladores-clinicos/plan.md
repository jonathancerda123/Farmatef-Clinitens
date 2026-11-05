# Plan técnico — 014 / Simuladores clínicos

Spec: [spec.md](spec.md). Base actual inspeccionada; ejecución de código autorizada por petición explícita de 2026-11-04, limitada a simulaciones educativas ficticias y sujeta a aceptación académica.

## Base inspeccionada

- `homeApp/` presenta Área clínica y todavía muestra los tres módulos como pendientes.
- `CliniTensDocenteApp.models.Curso` incluye responsable, colaboradores y matrícula de estudiantes.
- `core.permissions` ofrece `es_docente`, `es_administrador` y `cursos_visibles_para_docente`.
- `CliniTensFichaApp` maneja fichas y resultados existentes; no se reutilizará para guardar notas clínicas nuevas ni se reasignarán sus datos.
- `components/Layout/app_shell.html`, adaptadores de páginas y tokens de `static/css/tokens.css` son la base visual.
- Se preservan íntegramente los cambios locales sin seguimiento `docs/diagramas/` y `work/`; no forman parte de este cambio.

## Integración propuesta

Una app Django `CliniTensSimulacionApp` para compartir permisos, cursos, estados de publicación y aislamiento de intentos sin duplicar identidad/cursos ni tocar fichas actuales. Modelos separados para caso educativo, etapas publicadas, intento del estudiante y eventos de DAU/laboratorio/Kardex. Relación con curso obligatoria para evitar contenido abierto/ambiguo. Los datos de muestra se crearán como fixtures de pruebas/documentación, no se cargarán en la base recibida.

| RF | Archivos | Cambio | Verificación prevista |
|---|---|---|---|
| 014-01 | `templates/pages/clinitens/clinitens.html`, `homeApp/views.py`, `homeApp/urls.py` | Tarjetas y portadas de módulo | Rutas y revisión visual |
| 014-02/03 | Nueva app, `core/settings.py`, `core/urls.py`, migraciones | Casos por curso, publicación y acceso de alumno | GET/POST por rol, matrícula/propiedad y estados |
| 014-04 | Formularios/vistas/plantillas de laboratorio | Valores libres con unidad, sin clasificación automática | Preservación literal y acceso denegado |
| 014-05 | Modelos/servicios/vistas/plantillas Kardex | Eventos inmutables de administrado/omitido/corrección | Duplicado/ID ajeno no cambia eventos |
| 014-06/07/08 | Bases compartidas y documentación | Ámbito de curso, rótulos de simulación y trazabilidad | URLs directas, móvil/teclado y fixture aislada |

## Datos, contratos y permisos

Cada caso pertenece a un curso visible para el docente; publicar/editar se limita al responsable o colaborador habilitado. Un intento único por estudiante/caso. Las rutas consultan curso y matrícula antes de leer o escribir. El estudiante no puede cambiar campos preparados por docente ni enviar IDs de eventos ajenos. Eventos Kardex tienen estado/actor/fecha del servidor y corrección por nueva anotación vinculada al original. No habrá cálculos terapéuticos, referencias clínicas sugeridas ni integración con `FarmaTEFApp`.

## Interfaz y estilos

Páginas en `templates/pages/clinitens/simulacion/`, dentro del layout existente; accesos discretos en portada siguiendo el patrón `module-entry`. Formularios con labels, errores y mensajes del sistema; navegación con H1 de `page_title`, subsecciones H2/H3, tablas desplazables y controles accesibles. Añadir fuentes Tailwind explícitas solo si se incorporan archivos de app nuevos fuera de fuentes ya escaneadas; compilar el CSS oficial si cambia la fuente.

## Migraciones, compatibilidad y reversión

Migración aditiva en la nueva app, sin cambios en esquemas existentes. No aplicarla a la base local recibida ni a otra base persistente. Antes de migrar en un entorno futuro, generar respaldo y comprobar restauración según `docs/ENTORNO_Y_VERIFICACION.md`. Reversión: revertir únicamente archivos nuevos y la integración de portada/URLs/settings; cualquier esquema ya aplicado requerirá plan de reversión y respaldo propio.

## Pruebas y riesgos

Verificar estados borrador/publicado, matrículas, curso ajeno, rol inactivo/sin perfil, acceso cruzado a intentos, formularios inválidos y repetición de evento. Revisar 1440/768/390 px, teclado, mensajes y estados vacíos. Ejecutar comandos solo con configuración aislada; no leer `.env`, `db.sqlite3` ni `media/`. Riesgo principal: el usuario puede confundir un simulador con un sistema clínico; cada pantalla repetirá la advertencia y no incluirá directrices de atención real.

## Documentos afectados

`specs/README.md`, esta spec, `docs/PROYECTO.md`, `docs/ESTADO_PROYECTO.md`, `docs/ARQUITECTURA_BASE.md`, `docs/TRAZABILIDAD.md`, `docs/VERIFICACION.md`, `AGENTS.md` solo si cambia el siguiente paso técnico. Se deja el «Perfil administrador de módulos» como futuro separado.
