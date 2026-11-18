# Plan — 028

La portada clínica usa `home-intro`, `clinical-guide`, `guide-step` y tarjetas `clinical-module`. FarmaTEF ya recibe los tokens jade de 027 y dispone de cuatro herramientas docentes y dos accesos estudiantiles. Los cambios locales de 027, los diagramas y `work/` se preservan.

Reutilizar esas clases en `templates/pages/farmatef/farmatef.html`. La acción docente abre Recetas y la estudiantil abre Mis recetas de práctica. Por petición posterior, retirar la guía de FarmaTEF y mover el bloque único de alertas al lado de la presentación. El estudiante usa una presentación de una columna.

Retirar las reglas de la antigua barra de alertas junto a herramientas, ya sin consumidor. Las herramientas ocupan el ancho disponible debajo de la presentación. El cambio afecta plantilla y CSS, sin persistencia ni migraciones.

Verificar plantillas con perfiles ficticios, enlaces y estados de acceso. Ejecutar las regresiones pertinentes de alertas y revisar escritorio y móvil en navegador. Para recuperar, revertir los cambios de 028 y recompilar, conservando 027.

## Ajuste de densidad solicitado

Acotar el título a 40–44 px en escritorio y abreviar la descripción sin añadir texto decorativo. Convertir cada alerta en una fila con conteo, título y flecha. Usar accesos completos a herramientas con iconos del sistema y descripciones breves, sin un pie de tarjeta separado. Reutilizar los tokens y la clase base `module-entry`, con reglas acotadas a FarmaTEF para controlar proporciones, espaciado y columnas.

La revisión más reciente fija dos columnas en escritorio. Retirar el salto a cuatro columnas y aumentar iconos, títulos, descripciones y separación interna de las herramientas. Dar una altura mínima moderada a los accesos para recuperar presencia visual con el contenido alineado al centro vertical. Comprobar la cuadrícula 2×2 en ancho amplio y una columna en móvil.
