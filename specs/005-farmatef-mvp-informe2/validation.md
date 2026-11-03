# Validación — 005

2026-10-17. Revisión documental y primer incremento de inventario implementado; validación funcional pendiente.

## Fuentes revisadas

- `Informe 1 - Jonathan Cerda, Valentina Román.docx`: objetivos, MVP, restricciones, RF/RNF y plan de 7 sprints/560 horas.
- `TIHI84_U2_EF2_GUÍA_ABPro.docx`: requisitos de etapa formativa/sumativa y escala de apreciación.
- `TIHI84_U2_ES2_Plantilla_informe_Guía_ABPro.docx`: estructura obligatoria del informe ES2.
- `docs/PROYECTO.md`, `docs/ESTADO_PROYECTO.md`, `docs/ARQUITECTURA_BASE.md`, `docs/OBSERVACIONES_PROYECTO.md`, `docs/ENTORNO_Y_VERIFICACION.md` y specs 001–004.

## Hallazgos verificables

- La guía Unidad 2 pide comparación cualitativa/cuantitativa y factibilidad; componentes; tres procesos BPMN; casos de uso, componentes, modelo/diccionario, topología, infraestructura y arquitectura; KPI SMART y SLA; pruebas y normas; plan de implementación; ajuste de cronograma.
- La plantilla ES2 contiene secciones I–X: introducción, tecnología, arquitectura, KPI/SLA, pruebas/calidad, implementación, cronograma, conclusiones, referencias y anexos.
- El repositorio describe CliniTENS y mantiene FarmaTEF como pendiente. Los límites operativos y de seguridad actuales están documentados en `docs/VALIDACION_PREPRODUCCION.md`.
- El equipo confirmó: preinforme 2026-11-04; entrega completa EVS2 2026-11-25; presentación del informe y prototipo EVS3 2026-12-02 y 2026-12-09; defensa EVS4 2026-12-16 y 2026-12-23. Las pautas completas de estas evaluaciones no están adjuntas.
- Se redactó un borrador de contenido del preinforme en `docs/borradores/PREINFORME_EVS2_FARMATEF_CLINITENS_2026.md`, alineado con la estructura I–X de la plantilla ES2 y etiquetando datos propuestos/pendientes.
- El intento obligatorio de `render_docx.py` sobre la plantilla se detuvo porque no hay LibreOffice en PATH. Se intentó exportación con Word COM (la plantilla abrió y reportó 5 páginas), pero la conversión se bloqueó durante más de 60 segundos sin producir PDF. La plantilla original no se modificó; no se creó DOCX final ni se hizo revisión visual de páginas.
- Desde el 2026-10-17 hasta ES2 hay unas 5,6 semanas/220 horas; hasta la segunda fecha EVS4, unas 9,6 semanas/380 horas al ritmo declarado de 40 horas semanales, frente a 560 horas/14 semanas del Informe 1.
- Se añadieron `FarmaTEFApp`, los modelos Medicamento/LoteInventario, formularios de alta, listado docente, portada y migración inicial `0001_initial`.
- El intento de generar la migración con `.test-artifacts/dependencias-004/target/Scripts/python.exe` falló antes de cargar Django: el launcher busca `C:\Users\Fernando\AppData\Local\Programs\Python\Python312\python.exe`, que no existe en este equipo. La migración se escribió manualmente a partir del modelo y queda pendiente cotejo automático.

## Pendiente

No se ejecutaron pruebas ni `manage.py check` para este cambio. No hay aceptación del docente ni rúbricas EA3/EA4 completas; sí se confirmaron las fechas EVS3/EVS4. Reglas específicas de dispensación e integración real de IA siguen pendientes. Las métricas/SLA son propuestas hasta obtener mediciones y aprobación. El borrador existe solo en Markdown; revisión visual de la plantilla e informe como documentos no realizada. Los originales no se modificaron y la migración no se aplicó a ninguna base.


## Carga autorizada de catálogo Vademécum 2023 — 2026-10-31

Tras revisar la tabla extraída de las fichas pp. 8–55, el usuario confirmó la base habitual y la cuenta valita, e indicó «Solo preparar cantidades; no crear lotes todavía». Se verificó exclusivamente identidad/rol activo de valita, esquema/migración y catálogo/lotes necesarios para esta operación, sin leer contraseñas, .env ni media. La autorización puntual permite esta carga en la base habitual; no habilita otras lecturas o migraciones.

Se crearon 109 medicamentos bajo valita (cuenta activa ADMIN/superusuario). El catálogo estaba vacío: no se actualizaron existentes. Para nombres repetidos se añadió concentración y forma al nombre, conforme a la restricción existente por responsable, sin cambiar modelos. Datos ausentes o contradictorios no se completaron: Diclac conserva concentración vacía y Tronsalan forma vacía, con evidencia en manifiesto. Los 11 suplementos no se cargaron.

Las cantidades ficticias de 1 a 40 (2.465 unidades propuestas para medicamentos) permanecen solo en el archivo de preparación. No se crearon lotes ni vencimientos ni códigos de barras. El stock mínimo conserva el valor predeterminado del modelo (0); el stock de los nuevos medicamentos es 0. No se modificó código, configuración, dependencias ni migraciones.

Plan, recuperación, preparación y manifiesto con IDs/páginas/notas: `output/farmatef/vademecum-2023-plan-carga.json`, `vademecum-2023-preparacion.md`, `vademecum-2023-preparacion.json` y `vademecum-2023-carga.json`. Respaldo SQLite previo en `.test-artifacts/farmatef-vademecum-2023/` (ruta exacta en manifiesto); no compartirlo como artefacto público.

Comandos ejecutados mediante bloques Python por stdin con `C:/Users/jonat/AppData/Local/Programs/Python/Python312/python.exe`, paquetes del target por sys.path: inspección acotada SQLite en modo lectura; `settings.configure` mínimo para auth/contenttypes/FarmaTEFApp sin importar settings normales ni core.test_settings; `full_clean` de los 109 modelos; respaldo SQLite e integrity_check; ensayo de las 109 altas en transaction.atomic con rollback obligatorio; carga atómica; reapertura y comparación de campos/autor/valores predeterminados; cotejo de lotes antes/después mediante instantánea y SHA-256; integrity_check final. Resultados correctos, 109 altas, 0 actualizaciones, lotes 0 antes/0 después. Python 3.12.0, Django 5.2.18. Launcher target sigue roto; no se reparó.

Límites: no se ejecutó navegador, URLs ni suite funcional completa; esta verificación respalda la carga de datos, no certifica permisos de vistas ni dispensación/descuento. No hubo migraciones, despliegue, commit/push. Próximo paso: revisar catálogo visible con valita; antes de cargar otro PDF comparar los cuatro campos y reportar nuevos/existentes/diferencias, sin sobrescritura automática ni cambios de lotes/existencias. Crear lotes o probar descuentos requiere una solicitud posterior.
