# Plan — 022

Reemplazar introducción redundante de index por dos entradas grandes con componentes/tokens existentes. Tipografía Trebuchet/Segoe, turquesa de acción, superficie blanca y dos columnas (una móvil). Conservar tabla de actividad y privacidad.

Marcar los tres widgets medicamento en FarmaTEFApp/forms.py; widget compartido añade metadatos de búsqueda, conservando metadatos existentes de etiquetas. JS local único mejora select mediante combobox accesible y lista máxima de 20 resultados; mantiene select oculto para POST y eventos. Inicializar nuevas filas mediante MutationObserver y sincronizar reset/change. Mantener lote dependiente y servidor intactos.

Pruebas: forms autorizados/manipulados, integración navegador sobre fixtures sintéticas para filtro/selección/lote/reset/filas dinámicas/teclado/móvil y POST; suite actual y build. Nunca consultar catálogo original para producir capturas/fixtures. Cambios 021 independientes conservados.
