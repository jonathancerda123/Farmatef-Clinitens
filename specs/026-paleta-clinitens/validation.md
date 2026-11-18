# Validación — 026

## Revisión vigente — 2026-11-18

La usuaria rechazó la paleta anterior y entregó una referencia gris/turquesa/blanco. Se muestrearon sus cinco franjas con Pillow. La implementación actual usa esos tonos y variantes oscuras para texto y botones.

| Comprobación | Resultado |
|---|---|
| `npm.cmd run build` en `theme/static_src` | Correcto con Tailwind 4.3.3 y Node 20.15.0. Se conserva la limitación de versión de Node documentada abajo. |
| Contraste calculado por luminancia relativa, 16 pares de tokens | Todos cumplen los mínimos de 4,5:1 para texto y 3:1 para foco/controles en los pares medidos. Blanco sobre botón principal 5,07:1, blanco sobre navegación 12,63:1, texto secundario sobre fondo 5,64:1. |
| Enlaces, hover y foco | Turquesa oscuro sobre blanco 6,47:1. Blanco sobre `brand-500` 4,56:1. Foco sobre fondo claro 3,19:1 y sobre navegación 4,90:1. |
| Barra de progreso | Se cambia el porcentaje a texto oscuro sobre turquesa claro. |
| Chrome, HTML ficticio de la revisión anterior con CSS vigente | Inventario en escritorio. Acceso, inicio y FarmaTEF en marcos de 390 px. Se observan navegación gris, botones turquesa oscuros con texto blanco, texto oscuro en superficies claras y estado vencido rojo. |
| `manage.py check --settings=core.test_settings` con `.venv/Scripts/python.exe` | Sin incidencias. |
| Suite Django de las seis apps con `core.test_settings` | 86 pruebas, 85 pasaron y una omitida por requerir PostgreSQL. |
| `node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs` | 4 pasaron. |
| `git -c core.whitespace=cr-at-eol diff --check` | Sin errores. |

La inspección visual utilizó archivos HTML con datos ficticios renderizados el 16 de noviembre y los estilos actuales. Queda pendiente el recorrido de formularios en vivo y la aceptación de la usuaria. Las medidas y capturas siguientes corresponden a la primera propuesta.

## Evidencia anterior — 2026-11-16

2026-11-16. Rama local `valentina`. Django 5.2.18 y allauth 65.19.7 con Python 3.11.1 de `.venv`, dado que el intérprete target de 004 no está presente. Django usó `core.test_settings` y datos ficticios.

| Requisito | Comprobación | Resultado |
|---|---|---|
| RF-026-01 | `npm.cmd run build` en `theme/static_src`. | Correcto con Tailwind 4.3.3. La instalación emitió advertencia de motor por Node 20.15.0, frente al rango 22/24. |
| RF-026-02 | Portada docente e inventario ficticio en Chrome. | Stock bajo en ámbar, vencimiento próximo en rosa y lotes vencidos en rojo. Las notificaciones usan el color semántico para icono y borde. |
| RNF-026-01 | Luminancia relativa de 17 pares de color. | Texto blanco sobre violeta 9,62:1, enlace azul sobre blanco 7,26:1 y error sobre fondo claro 5,97:1. Foco azul sobre blanco 4,03:1 y cian sobre ciruela 8,07:1. |
| RNF-026-01 | Chrome de escritorio y marcos de 390 px. | Portada de FarmaTEF e inventario en escritorio. Acceso, inicio y FarmaTEF en ancho móvil. El foco cian sobre Inicio se observó al navegar con Tab. |

## Pruebas y límites

- `.venv/Scripts/python.exe manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp CliniTensSimulacionApp --settings=core.test_settings` → 86 pruebas, 85 pasaron y una se omitió porque requiere PostgreSQL.
- `node.exe --test static/js/mensajes.test.cjs theme/static_src/build.test.cjs` → 4 pasaron.
- Django Test Client comprobó acceso docente al inventario (200), acceso estudiantil denegado (403) y carga estudiantil de DAU y Laboratorio (200).
- El navegador local no conectó al servidor de prueba. Se inspeccionaron archivos HTML renderizados por Django con datos ficticios y los estáticos del proyecto. Quedó pendiente recorrer los formularios en vivo y revisar visualmente DAU y Laboratorio.

La usuaria decidió conservar provisionalmente la paleta gris y turquesa. La revisión de formularios en vivo sigue pendiente.
