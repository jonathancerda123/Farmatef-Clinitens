# Fuentes y trazabilidad local

Inspección estática del 2026-10-28. Sin .git: git status devolvió «not a git repository». No se inventó URL, revisión ni evidencia de commit. Las huellas SHA-256 identifican los archivos locales al documentar, no certifican su ejecución. Por ese motivo candidate.json no contiene meta.repository ni fuentes que el visor pudiera presentar como verificadas contra Git. No se pasó --repo-root: esa validación requiere un repositorio con revisión real. El diagrama es una síntesis manual del código local.

| Nodo / relación | Fuente observada | Hecho y límite |
|---|---|---|
| Navegador / presentación | templates/components/Layout/base.html:1–29; theme/static_src/package.json | HTML Django, tokens, CSS Tailwind y scripts locales Alpine/DOMPurify. theme compila estilos; no es servicio separado. |
| core / rutas | core/urls.py:7–26; core/settings.py:33–109 | Apps registradas y resolución de URL; middleware sesión, CSRF, allauth, Axes y concurrencia. No hay proxy/CDN/worker representados. |
| core / permisos | core/permissions.py:3–25; core/mixins.py:7–57 | ADMIN/superusuario activos globales, MANAGER propietario. Los filtros/mixins se aplican en las vistas, no se presupone autorización por menú. |
| UsuarioApp | UsuarioApp/models.py:21–45; UsuarioApp/urls.py; UsuarioApp/views.py | Position.permission_code y Profile uno a uno con User; gestión de cuentas y perfil. /accounts/ usa allauth, /admin/ usa Django admin. |
| homeApp | homeApp/views.py:10–48; homeApp/urls.py | Portadas, consulta ORM de usuarios/actividad según alcance. /farmatef/ exacta se resuelve por homeApp antes del prefijo de inventario. |
| Docente | CliniTensDocenteApp/models.py:21–214; CliniTensDocenteApp/urls.py | CasoClinico, CasoMultimedia, CodigoActividad, Paciente, PacienteMultimedia, ResultadoDiagnostico, Curso. Código vincula caso, autor y curso opcional; curso tiene estudiantes M2M. |
| Docente → ficha / SQLite | CliniTensDocenteApp/views.py:107 en adelante; CliniTensFichaApp/models.py:8–66 | fichas_visibles_para filtra revisión. Evaluación publicada y borrador separados. No son microservicios: el módulo docente opera sobre FichaClinica dentro del monolito. |
| Exportaciones docentes | CliniTensDocenteApp/views.py:64–65, 1011 en adelante | openpyxl para planillas; ReportLab para PDF de ficha clínica. No implica PDF de dispensación. |
| Ficha | CliniTensFichaApp/models.py:8–66; CliniTensFichaApp/views.py:33 en adelante; CliniTensFichaApp/urls.py | FichaClinica única por estudiante/código; datos y rúbricas JSON; estados y versión. EstudianteMixin exige ficha propia y comprueba matrícula cuando corresponde. Guardado condicional por versión en editor. |
| FarmaTEF | FarmaTEFApp/models.py; FarmaTEFApp/views.py:12–68; FarmaTEFApp/urls.py | InventarioView restringida; objetos_del_docente y formularios con actor. Crea medicamentos/lotes con autor fijado en servidor; calcula stock/alertas. No hay receta/dispensación en sus rutas/modelos. |
| SQLite | core/settings.py:121–126; modelos y llamadas ORM anteriores | Motor local configurado. No se abrió db.sqlite3 ni se afirma que las tablas estén migradas en ella. |
| Archivos | core/urls.py:8–9; core/media.py:31–70; FileField en modelos docentes y Profile.image | GET privado autorizado por objeto/publicación; default_storage.open con FileResponse. Upload directo CKEditor desactivado. Metadatos de adjuntos en ORM, bytes en almacenamiento. |
| Dependencias | requirements.txt; theme/static_src/package.json | Versiones declaradas, no inventario ejecutado. Django/allauth/Axes/preventconcurrentlogins; CKEditor5/nh3/Pillow/openpyxl/ReportLab; Tailwind/Alpine/DOMPurify. |
| Planificado / validación pendiente | specs/005-farmatef-mvp-informe2/spec.md; docs/ESTADO_PROYECTO.md | RF-005-07 solicita arquitectura fiel. Receta, dispensación, comprobantes, etiquetas, historial y asistencia IA no son componentes implementados. Aceptación y validación FarmaTEF permanecen pendientes. |

Los controles Archify verifican esquema, composición, artefacto y navegador. No verifican permisos de Django, URLs reales, migraciones, seguridad clínica ni preparación de producción. No se ejecutó la aplicación.
