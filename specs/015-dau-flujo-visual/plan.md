# Plan técnico — 015 / Flujo DAU

Spec: [spec.md](spec.md). La usuaria autorizó el trabajo local al pedir que el DAU quede como las capturas. No incluye push, despliegue ni datos de pacientes reales.

## Base inspeccionada

Se extiende `CliniTensSimulacionApp`; rutas actuales ya filtran casos publicados y matrícula para prácticas. `CasoSimulacion` ya pertenece a curso. `IntentoSimulacion` se mantiene para laboratorio/Kardex. Se usan `core.permissions`, ReportLab existente, `base.html`, tokens y hoja de estilos de CliniTENS. No consultar `.env`, `db.sqlite3` ni `media/` para diseñar o poblar contenido.

## Integración

| RF | Archivos | Cambio | Evidencia |
|---|---|---|---|
| 015-01/02 | `models.py`, `forms.py`, `views.py`, `urls.py`, form docente | Código y ficha de paciente ficticio; acceso DAU por curso | Migración y verificación de URL/permisos |
| 015-03 | `models.py`, `forms.py`, `views.py`, `dau.js` | Signos guardados; PAM/IMC recalculados en servidor | Valores automáticos/casos incompletos en entorno ficticio |
| 015-04/05 | `ProcedimientoDAU`, `AtencionDAU`, vistas/forms | Eventos append-only y cierre inmutable | Flujo de POST y estado cerrado |
| 015-06 | `views.py`, PDF ReportLab, `dau_historial.html` | Historial propio e impresión/PDF simulado | PDF revisado visualmente, sin datos reales |
| 015-07/08 | plantillas autónomas `base.html`, estilos fuente y JS | Diseño responsive similar a referencia | Navegador escritorio/móvil/teclado |

## Persistencia y recuperación

Campos paciente nuevos son opcionales en esquema para conservar casos existentes; formulario docente exige valores sintéticos y código SIM. La nueva atención se separa del intento genérico para permitir historial sin cambiar la unicidad de IntentoSimulacion. Procedimientos no se modifican ni eliminan; se añaden nuevos eventos. Antes de aplicar migraciones a la base local: respaldo verificable, `migrate --plan`, aplicación solo de la app DAU y `showmigrations`. Mantener copia en `.test-artifacts/backups/`; no exponer o leer los registros durante el respaldo.

## Interfaz

Página DAU de ancho completo sobre `base.html` (sin navegación lateral), cabecera corta, botón Nuevo paciente/Salir; panel de identificación; ficha de paciente; panel de signos en rejilla; procedimientos con historial; panel DAU; barra de acciones e historial. En pantallas estrechas, cuadrícula pasa de 4 a 2/1 columnas. Usar identidad de tokens existentes con acento azul solo si compatible con escala de marca, y no copiar datos/screens de terceros.

## Verificación y límites

`core.test_settings`, migración en memoria, checks Django, cotejo de migración, carga/resolución de plantillas/rutas, y revisión visual del PDF y navegador. La implementación solo demuestra registro educativo ficticio; no acredita triage oficial, calidad clínica ni uso asistencial.
