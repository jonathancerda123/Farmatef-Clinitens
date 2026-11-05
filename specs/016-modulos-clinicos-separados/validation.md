# Validación — 016 / Módulos clínicos diferenciados

Fecha: 2026-11-04. Implementación local; comprobaciones con `core.test_settings`. No se inspeccionó ni migró la base local habitual. No se ejecutó suite de pruebas.

| RF | Verificación | Resultado esperado | Estado |
|---|---|---|---|
| 016-01 | Rutas `docente_dau`, `docente_laboratorio`, `docente_kardex`, enlaces distintos | DAU, laboratorio y Kardex abren gestión propia | `reverse()` correcto; plantilla de portada cargó en check Django |
| 016-02 | ModelForms acotados para DAU/laboratorio; formulario por líneas para Kardex | Guardado toca solo campos del módulo | Revisión estática del código; no se ejecutó POST |
| 016-03 | `DocenteMixin`, filtro `cursos_visibles_para_docente`, comprobación de borrador antes de guardar | Solo docente autorizado cambia borrador en curso visible; publicados no se alteran | Código revisado; matriz de peticiones directas no ejecutada |
| 016-04/05 | Carga de plantillas docentes, estudiante, DAU; reverse de rutas | Interfaz de gestión y práctica separadas | Correcto con `core.test_settings` |
| 016-06 | CSS específico y reglas responsive | Secciones legibles y operables en desktop/móvil | Revisión estática; navegador/teclado pendiente |

Comandos ejecutados con `.venv\Scripts\python.exe` y `core.test_settings`:

- `manage.py check --settings=core.test_settings` — correcto, cero problemas.
- `manage.py makemigrations --check --dry-run --settings=core.test_settings` — correcto, no hay cambios de esquema pendientes.
- Carga de seis plantillas y `reverse()` para tres rutas docentes, DAU, laboratorio, Kardex y resultados — correcto.

No se ejecutaron pruebas funcionales ni peticiones con perfiles ficticios. No se revisó el navegador. La revisión visual y del flujo en cada rol queda pendiente.
