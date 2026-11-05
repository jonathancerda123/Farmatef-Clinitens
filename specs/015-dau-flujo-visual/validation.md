# Validación — 015 / Flujo DAU

Fecha: 2026-11-04. Implementación local terminada. Checks y migración se ejecutaron exclusivamente con `core.test_settings`; no se abrió ni migró la base local habitual.

| RF | Verificación | Esperado | Resultado |
|---|---|---|---|
| 015-01/02 | Formularios/rutas y hoja `simulacion-docente.css`; carga de `docente.html` | Formulario agrupa datos generales, paciente SIM y escenarios | Plantilla cargada tras corrección; falta revisar interacción y validación funcional |
| 015-03 | `DatosDAUForm`, cálculo servidor y JS de vista previa | Servidor recalcula PAM/IMC; rangos de entrada acotados | Check Django pasó; no se ejecutó POST |
| 015-04/05 | Modelos de atención/procedimiento y acciones de guardado/cierre | Procedimientos se acumulan y DAU cerrado queda solo lectura | Migración aditiva aplicada en SQLite en memoria; no se ejecutó flujo de navegador |
| 015-06 | Historial propio y generador ReportLab con marca educativa | PDF y listado solo de cuenta matriculada | Rutas reversibles y plantilla cargada; PDF no generado ni inspeccionado |
| 015-07/08 | Querysets vuelven a comprobar inscripción/publicación; CSS adaptable | Accesos acotados y distribución para escritorio/móvil | Inspección estática; no se ejecutaron perfiles HTTP ni revisión visual/teclado |

## Comandos y resultado

Entorno: `.venv\Scripts\python.exe` con `core.test_settings` (SQLite en memoria, sin `.env`/base/media normal).

- `manage.py check --settings=core.test_settings` — correcto, cero problemas.
- `manage.py makemigrations --check --dry-run --settings=core.test_settings` — correcto, sin cambios pendientes después de generar migraciones 0003/0004.
- `manage.py migrate --settings=core.test_settings --noinput` — esquema completo aplicado en la base de memoria; incluye DAU 0003/0004.
- Carga de `dau_inicio.html`, `dau_registro.html`, `dau_historial.html`, `docente.html` y `reverse()` de las cuatro rutas DAU — correcto.

No se ejecutaron pruebas funcionales, pruebas de permisos, navegador, impresión física ni inspección del PDF. Migraciones 0003/0004 aún no aplicadas a la base local de la usuaria. La revisión visual/pedagógica por usuaria y docente sigue pendiente.

No ingresar RUT ni datos de pacientes reales. Para usarlo en la base local normal, verificar primero `migrate --plan`, crear respaldo en `.test-artifacts/backups/` y aplicar únicamente las migraciones nuevas de `CliniTensSimulacionApp`.
