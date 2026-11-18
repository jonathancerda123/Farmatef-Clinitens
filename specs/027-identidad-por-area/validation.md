# Validación — 027

Rama `valentina`. Entorno de verificación con `core.test_settings` y datos ficticios. Se utilizó `.venv/Scripts/python.exe` con Django 5.2.18 porque el target de 004 no está presente.

| Requisito | Comprobación | Resultado |
|---|---|---|
| RF-027-01/02 | Test Client en memoria, 11 pantallas. | Acceso e inicio con base compartida. FarmaTEF, inventario, recetas y práctica con jade. Área clínica, panel docente, ficha, DAU y laboratorio con azul. Todas respondieron 200 y renderizaron el atributo esperado en body. |
| RF-027-02 | POST incompleto de registro de medicamento. | Respuesta 200 con errores de formulario y área FarmaTEF conservada. |
| RF-027-03 | Inventario ficticio en navegador. | Lotes vencidos en rojo, stock bajo en ámbar, confirmación sin alertas en verde. |
| RNF-027-01 | Contraste de 36 pares por luminancia relativa. | Todos cumplen mínimos de 4,5:1 para texto y 3:1 para foco/control en los pares medidos. Blanco sobre base 11,14:1, jade 4,61:1 y azul clínico 5,72:1. El fondo suave de FarmaTEF se aclaró tras detectar 4,22:1 en la primera medición. El par corregido alcanza 4,52:1. |
| RNF-027-01 | `npm.cmd run build` en `theme/static_src`. | Correcto con Tailwind 4.3.3 y Node 20.15.0. El motor Node sigue fuera del rango 22/24 declarado por el tema. |
| RNF-027-01 | Brave y Chrome, HTML renderizado por Django con estáticos vigentes. | Inicio e inventario en escritorio. Inicio, FarmaTEF y área clínica en marcos de 390 px. Inicio a 768 px. DAU en escritorio. Foco de Inicio visible sobre la navegación azul profundo. |

## Comandos y límites

- `.venv/Scripts/python.exe manage.py check --settings=core.test_settings` → sin incidencias.
- `.venv/Scripts/python.exe manage.py test homeApp --settings=core.test_settings` → 2 pruebas correctas.
- `node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs` → 4 pruebas correctas.
- Test Client verificó redirección anónima al inventario (302) y denegación al estudiante (403).
- HTML y resultados de contraste en `.test-artifacts/paleta-027/`, ignorados por Git. Los enlaces de la vista previa entre las pantallas generadas se adaptaron a archivos hermanos para poder comparar las áreas.
- La inspección visual usó HTML de datos ficticios con los estáticos actuales. El recorrido de formularios en vivo, zoom 200% y revisión visual completa de todas las pantallas siguen pendientes.

La usuaria aprobó guardar y subir esta versión visual en la rama valentina.
