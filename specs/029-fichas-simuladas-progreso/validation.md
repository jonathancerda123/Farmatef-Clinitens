# Validación — 029

Fecha: 2026-11-18. Entorno: demo ficticia 8025 y copias de ensayo y revisión con `core.test_settings`, Python 3.12.0 y Django 5.2.18. Carga aplicada. Revisión docente pendiente.

| Requisito | Resultado comprobado |
|---|---|
| RF-029-01 | Ficha 4 `FCE-APS028-01`: 13/13, pendiente de calificación. Se agregaron dos recontroles a las 15:00 y 15:15. Doce secciones tienen datos clínicos simulados. Dispositivos invasivos quedó como «No aplica», con ausencia de dispositivos documentada en evolución. La columna numérica de presión en recontroles contiene la sistólica y el registro de cuidados conserva cada presión completa. |
| RF-029-02 | Ficha 5 `FCE-APS028-02`: 6/13, borrador. Identificación, tratamiento habitual, signos, necesidades, plan y exámenes completos. Siete secciones pendientes. |
| RF-029-03 | Ficha 3 `FCE-INT-03`: 3/13, borrador. Identificación, antecedente farmacológico y signos de ingreso completos. Diez secciones pendientes. |
| RF-029-01 a RF-029-03 | 59 solicitudes de prueba por entorno en ensayo y copia de la demo aplicada. Se verificaron las 13 secciones de cada ficha, los contadores en Seguimiento en vivo, el bloqueo de la ficha enviada, los envíos incompletos y el acceso ajeno denegado. Las escrituras de prueba se revirtieron. |
| Integridad | La transacción comparó todas las fichas y conservó el estado, la evaluación, la identidad y los vínculos. Solo cambiaron contenido, versión y fecha de actualización de las tres fichas objetivo. SQLite `quick_check` y `foreign_key_check` correctos. La repetición hizo cero escrituras. |

El caso respiratorio completo conserva los signos de ingreso del DAU, el hemograma y el informe de tórax ya preparados. El caso de control cardiovascular conserva los signos del DAU, la HbA1c y el ECG ficticios. Las referencias orientaron el contexto de asma y técnica inhalatoria; los valores y registros son simulados. [Recomendaciones de asma, MINSAL](https://diprece.minsal.cl/garantias-explicitas-en-salud-auge-o-ges/asma-bronquial/recomendaciones/) · [Uso de inhaladores, ISP](https://ispch.cl/anamed/farmacovigilancia/informacion-para-la-comunidad/uso-correcto-de-inhaladores/).

- Se ejecutaron `cargar.py ensayo`, `verificar.py ensayo`, `cargar.py demo`, `verificar.py demo` y `cargar.py repeticion` desde `.test-artifacts/fichas-029` con el intérprete `.test-artifacts/clinica-019-env/Scripts/python.exe`.
- Chrome a 1920×1000 comprobó la tabla de recontroles con valores y bloqueo, los tratamientos de los borradores y los tres recuentos. `verificar_chrome.cjs` cargó respuestas Django y activos locales mediante interceptación en una copia de la demo. La conectividad HTTP desde el entorno de trabajo no se confirmó.
- `manage.py check` y `makemigrations --check --dry-run` con `core.test_settings` correctos. Suite aislada: 93 pruebas correctas y una omitida por requerir PostgreSQL.
- Respaldo SQLite verificado en `.test-artifacts/fichas-029/demo-antes-20261118T185911941230Z.sqlite3` para recuperar la fixture de la demo siguiendo el [plan](plan.md).

Próxima revisión docente: abrir los recontroles de la ficha 4 en Estudiantes y consultar el avance de los dos borradores por su código en Seguimiento en vivo.
