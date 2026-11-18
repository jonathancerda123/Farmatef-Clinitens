# Validación — 028

Rama `valentina`. Verificación con `core.test_settings`, base ficticia en memoria y estáticos vigentes. Se usó `.venv/Scripts/python.exe` con Django 5.2.18, porque el target de 004 no está presente.

| Requisito | Comprobación | Resultado |
|---|---|---|
| RF-028-01/02 | Renderizado de la presentación y accesos. | Un H1, presentación H2, cuatro accesos completos docentes y dos estudiantiles. Cada acceso incluye icono, título, descripción breve y flecha. La guía de inicio se retiró por petición posterior. |
| RF-028-03 | Test Client con MANAGER, ADMIN, superusuario sin perfil y gestor sin existencias. | Alertas únicas en la presentación, antes de las herramientas. Ambos enlaces filtrados presentes y dos conteos cero en inventario vacío. |
| RF-028-04 | Test Client con estudiante y sin perfil. | Estudiante con presentación de una columna, dos tarjetas y sin alertas de gestión. Sus destinos responden 200 e inventario 403. El perfil sin cargo recibe el aviso de acceso. La visita anónima redirige a login (302). |

## Comandos y límites

- `.venv/Scripts/python.exe manage.py test homeApp FarmaTEFApp.tests.InventarioAlertasTests --settings=core.test_settings` → 5 pruebas correctas.
- `npm.cmd run build` desde `theme/static_src` → correcto, Tailwind 4.3.3 con Node 20.15.0, fuera del rango 22/24 declarado por el tema.
- Renderizados ficticios en `.test-artifacts/portada-028/`, ignorados por Git.
- La primera revisión visual se interrumpió porque la herramienta no pudo determinar la URL de Chrome con suficiente confianza. La comprobación visual de la nueva posición de alertas queda pendiente hasta un nuevo intento.

La revisión posterior se completó en Edge con los HTML ficticios y los estilos vigentes. Se inspeccionaron la portada en escritorio, marcos de 390 y 768 px y un marco de 1920 px mostrado al 80% para verlo completo. Se observó una columna en móvil, dos en tableta/escritorio intermedio y cuatro herramientas en escritorio amplio. Las alertas quedan junto a la presentación o debajo de ella en móvil, con altura ajustada a dos líneas de contenido. La evidencia visual de Edge resuelve la revisión pendiente de composición. El recorrido de formularios en vivo sigue fuera de esta inspección.

## Ajuste de densidad anterior

Se redujo la escala del título y la separación entre secciones. Las alertas se presentan en filas de altura ligada al contenido con conteo destacado y acceso completo. Las herramientas usan cuatro columnas desde 1600 px, dos en anchos intermedios y una en móvil. Se incorporan iconos de inventario, registro, receta y etiqueta al componente existente.

Tras el ajuste pasaron de nuevo las cinco regresiones de inicio/alertas y la compilación. El renderizado adicional comprobó MANAGER, ADMIN, superusuario sin perfil, gestor sin existencias, estudiante y usuario sin perfil. Los cuatro destinos docentes responden 200. Los dos destinos estudiantiles responden 200 e inventario responde 403 al estudiante. La composición de ejemplo incluye conteos ficticios 82 y 45 para revisar las proporciones.

## Revisión vigente — cuadrícula 2×2

La usuaria prefirió dos tarjetas arriba y dos abajo, con mayor tamaño. Se retiró la regla de cuatro columnas. Las tarjetas usan una altura mínima de 9rem, títulos de 1,2rem, descripción de 0,95rem e iconos en contenedores de 3,25rem. En móvil se mantiene una columna.

`npm.cmd run build` terminó correctamente con Tailwind 4.3.3. Las dos pruebas de `node.exe --test theme/static_src/build.test.cjs` pasaron. Se revisó en Edge el marco ficticio de 1920 px al 80%, comprobando las dos filas y dos columnas. El marco de 390 px mostró textos e iconos ampliados sin recortes, con altura ajustada al contenido. La revisión utilizó HTML ficticio y estilos vigentes. `git -c core.whitespace=cr-at-eol diff --check` sin errores.

La usuaria aprobó guardar y subir esta versión visual en la rama valentina.
