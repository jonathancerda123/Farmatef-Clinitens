# Plan técnico — 026

[Especificación](spec.md). La fuente de identidad es `static/css/tokens.css`. Los estilos del acceso, la navegación y las acciones dependen de los componentes CSS de Tailwind. DAU, Laboratorio y preparación docente incluyen estilos propios. Se preservan `docs/diagramas/` y `work/`, preexistentes y sin seguimiento.

| Requisito | Trabajo |
|---|---|
| RF-026-01 | Actualizar los tokens, la escala `brand` y los consumidores de colores de marca directos. Reutilizar la estructura, tipografía y jerarquía de los recorridos existentes. |
| RF-026-02 | Revisar avisos de inventario, validaciones, notificaciones y controles críticos. Mantener sus estados y mensajes. |
| RNF-026-01 | Recompilar Tailwind, medir pares de contraste y revisar pantallas representativas y foco de teclado con datos ficticios bajo `core.test_settings`. |

La reversión se limita a los archivos de presentación de esta spec y a recompilar la hoja de Tailwind. No hay pasos de migración.

## Revisión del 2026-11-18

La nueva imagen sustituye la dirección de color anterior. Mantener tipografía, estructura y alineación a izquierda. Usar gris oscuro para navegación y texto, blanco para superficies, turquesa para interacción y gris claro para separaciones. Oscurecer el turquesa en botones de texto blanco y en enlaces para cumplir contraste. Repetir build, contraste y revisión visual con las pantallas ficticias.
