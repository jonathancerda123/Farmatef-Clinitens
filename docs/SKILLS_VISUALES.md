# Skills visuales proporcionadas por el docente

Instalación local: 2026-11-24, por solicitud de la usuaria. Fuente: carpeta `anatomy` entregada por el docente. Se copiaron los tres paquetes completos, sin modificar sus instrucciones, ejemplos, recursos ni licencia existente, en `.codex/skills/`. No se añadieron dependencias de la aplicación ni se ejecutaron los scripts de los paquetes.

| Skill | Ubicación | Uso pertinente |
|---|---|---|
| anatomy | `.codex/skills/anatomy/SKILL.md` | Ilustraciones interactivas en SVG/isométrico; incluye kit, referencias y ejemplos de objetos físicos |
| threejs-animation | `.codex/skills/threejs-animation/SKILL.md` | Animación y transiciones si se decide usar Three.js |
| threejs-performance | `.codex/skills/threejs-performance/SKILL.md` | Medición de rendimiento y recursos si se decide usar Three.js |

## Aplicación al nuevo planteamiento de farmacia

El pedido sustituye el objetivo de representar con detalle cada cuadrado: se busca identificar en qué cajón está un medicamento, con varios muebles configurables y medidas ajustables. La instalación no implementó ese cambio; la posterior solicitud explícita autoriza su integración en [036](../specs/036-sala-farmacia/spec.md).

La solicitud de simplicidad prevalece sobre sugerencias de Anatomy como cantidades mínimas de piezas, mecanismos muy detallados, recorridos automáticos o marcos decorativos. Las skills no obligan a incorporar WebGL, Three.js, React ni un framework nuevo. Se evaluará primero SVG y JavaScript locales compatibles con Django y el diseño existente.

Antes de implementar el rediseño: documentar responsables de configuración, unidades y límites de medidas, número de muebles/cajones, asignación de medicamentos a ubicaciones y su conservación cuando cambie el catálogo. Mantener el inventario registrado como fuente de productos/stock y los permisos de curso/propiedad; conservar la interfaz, los tokens y la accesibilidad del sistema.

La vitrina de 033 permaneció intacta durante la instalación. 036 sustituye sus vistas/gráficos y conserva solo la URL antigua como redirección de compatibilidad. Reutiliza `iso-kit.mjs` de Anatomy como `static/vendor/anatomy/iso-kit.js`, sin alterar su contenido, y su licencia MIT. La extensión cambia para asegurar el tipo JavaScript en Windows. La migración aditiva 0011 se ensayó en memoria y fixtures nuevas y posteriormente se aplicó a la base local con respaldo verificado y autorización explícita. Cambios locales de 034 y otros preservados, sin paquetes nuevos, commit, push ni despliegue.

## Verificación de instalación

Comparación del inventario de archivos y de SHA-256 entre origen y destino: Anatomy 173 archivos; threejs-animation 1; threejs-performance 2. Contenido idéntico en todos los casos. Es una comprobación de copia, no una auditoría ni validación de ejecución de sus ejemplos.

Las skills quedan disponibles para su descubrimiento en el siguiente turno. Se leen sus referencias específicas cuando se aplican; instalarlas no equivale a ejecutar sus flujos.
