# Plan técnico — 017 / Flujos DAU, laboratorio y CAD

Spec: [spec.md](spec.md). Código autorizado por petición explícita del 2026-11-05. Solo entorno local y ficticio.

## Base inspeccionada

Se conserva `CliniTensSimulacionApp` existente: `CasoSimulacion`, `IntentoSimulacion`, `AtencionDAU`, `ProcedimientoDAU`, `EventoKardex`; acceso docente/estudiante y plantillas compartidas. Spec 015 ya implementa DAU individual. Spec 016 ofrece pantallas docentes separadas pero laboratorio y Kardex aún son texto/actividades simples.

## Integración

| RF | Archivo | Cambio | Verificación |
|---|---|---|---|
| 01 | `views.py`, `dau_*`, `models.py` | Preservar DAU actual | Check, rutas/plantillas |
| 02 | `models.py`, `forms.py`, `views.py`, `urls.py`, plantillas lab | Órdenes/tubos, recolección por intento, etiqueta imprimible | migración en memoria, render de etiqueta y reverses |
| 03 | `models.py`, `forms.py`, `views.py`, plantillas CAD | Resultados categorizados y revisión por intento | migración en memoria, render de cada categoría |
| 04 | `clinitens.html`, páginas docente/estudiante | Renombrar Kardex vigente a CAD, rutas propias | búsquedas de referencias y render |
| 05 | migración aditiva y docs | Preservar históricos; documentar recuperación | check/makemigrations dry-run y migrate memoria |

Los datos estructurados usan JSON con listas limitadas y claves validadas contra el caso; formularios normales sin entrada JSON cruda. Cada orden lleva un ID opaco estable. Las órdenes se agrupan por tipo de tubo para presentar una sola etiqueta por tubo. CAD conserva registros de historial; revisión solo escribe el intento propio del estudiante. Las rutas docentes filtran cursos mediante `cursos_visibles_para_docente`, los casos publicados no se editan y el alumno requiere inscripción activa.

## Migraciones y reversión

Añadir campos JSON con `default=list` a caso e intento en migración siguiente a 0004; no borrar ni cambiar `indicaciones_kardex`, `EventoKardex` ni datos de intentos antiguos. Ensayar en `core.test_settings` con DB en memoria, sin abrir ni migrar `db.sqlite3`. Antes de aplicar en una instalación con datos: hacer backup, verificar restauración, registrar `migrate --plan`, aplicar y validar. Reversión: volver a versión previa y restaurar backup si ya hubo escrituras; campos JSON son aditivos.

## Interfaz y riesgos

Usar estructura base existente y guía `docs/PERSONALIZACION_VISUAL.md`; formularios por módulo, estados vacíos y notas “simulación educativa”. Etiqueta CSS de impresión en mm. Evitar interpretación clínica y mantener la apariencia de imagen como ilustración esquemática genérica/no diagnóstica.

## Validación

Ejecutar solo `manage.py check`, `makemigrations --check --dry-run`, chequeo de migración en memoria, reverses y carga de plantillas con `core.test_settings`; no ejecutar la suite funcional ni migrar base normal. La inspección de navegador y aceptación de docente/estudiante quedarán como pendientes si no se realizan en esta sesión.
