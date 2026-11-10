# Plan — 020

Reutilizar `DocenteModuloView` y sus formularios; selección `?caso=id` validada dentro del queryset de cursos visibles. Nueva revisión por caso con el mismo mixin. Helper único para calcular los cuatro estados y condiciones existentes de publicación. Tarjetas y alta apuntan al recorrido; POST publicado retorna revisión cuando proviene de ella.

Dirección visual: tokens petróleo/verde existentes, Trebuchet/Segoe, controles existentes. Lista ordenada de pasos con nombre y estado textual; título del caso permanente, una acción primaria por pantalla y resumen final. El número ahora expresa una secuencia real; retirar el «4» aislado de la lista de casos. Formularios de un caso por pantalla, sin diálogos ni dependencias.

Pruebas: selección autorizada/ajena/inválida, manipulación de caso_id, guardado y continuidad, errores, pendientes/condiciones de publicación y solo lectura. Navegador con fixture/puente 019 para recorrido dirigido y 390px. No aplicar migraciones ni copiar datos entre carpetas.
