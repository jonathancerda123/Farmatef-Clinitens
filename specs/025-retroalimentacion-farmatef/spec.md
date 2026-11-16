# 025 — Alertas, registro y etiquetas de FarmaTEF

Fecha 2026-11-15. La solicitud autoriza cambios de plataforma y pruebas locales en la rama `jonathan`. Las capturas aportan contexto. El informe, la matriz RACI, los diagramas, el alojamiento definitivo y la entrevista docente quedan fuera de esta implementación.

| Requisito | Criterio de aceptación |
|---|---|
| RF-025-01 | La portada docente reemplaza el flujo por dos alertas clicables. Cada una abre el inventario filtrado por stock bajo o vencimiento próximo, incluso cuando el conteo es cero. |
| RF-025-02 | Inventario permite combinar búsqueda por nombre y clasificación. El alta de medicamentos y lotes tiene pantalla propia, mantiene los errores en el formulario y vuelve al inventario al guardar. |
| RF-025-03 | La etiqueta incluye un Code 128 imprimible y su texto. La práctica encuentra los lotes autorizados mediante ese código. Escanear por sí solo no dispensa. |
| RF-025-04 | Desde el área Farmacia, el estudiante inscrito puede listar y visualizar las etiquetas de sus dispensaciones simuladas. |
| RF-025-05 | Los avisos se apilan arriba a la derecha en escritorio, con ámbar para stock bajo y rosa para vencimiento próximo. En pantallas angostas aparecen encima de las herramientas. Las cuatro tarjetas mantienen sus destinos y alinean sus acciones. |
| RF-025-06 | El registro ocupa la columna principal de Recetas y el buscador se mantiene compacto a la derecha en escritorio. La búsqueda por fragmento del número devuelve coincidencias autorizadas. Seleccionar una abre su detalle debajo de la lista y conserva los resultados. |
| RF-025-07 | La vista previa de la etiqueta se actualiza al seleccionar medicamento y lote o al cambiar medidas o copias. Se valida en servidor y solo se habilita la impresión para la selección vigente y un formato que acomode la etiqueta. |
| RNF-025-01 | MANAGER ve su inventario. ADMIN y superusuario activo tienen acceso global. La ruta de registro se protege en servidor. Las etiquetas estudiantiles se comprueban por matrícula y propiedad. |
| RNF-025-02 | El conteo coincide con el filtro. Stock bajo compara disponibilidad vigente con el mínimo. Vencimiento próximo cuenta medicamentos activos con algún lote vigente, con unidades, dentro del plazo del medicamento. La fecha actual y el límite del aviso se incluyen. |
| RNF-025-03 | El entorno de PostgreSQL en Docker utiliza datos ficticios. Una prueba comprueba el saldo tras dos dispensaciones simultáneas y un ensayo aparte mide 500 transacciones SQL y su latencia. |
| RNF-025-04 | Un notebook ejecutable en VS Code compara dos detectores con el mismo conjunto de prueba de Roboflow y exporta las métricas de cada ejecución. Los aumentos pertenecen al entrenamiento. |

La tabla muestra el stock total registrado y las unidades disponibles. Se imprime el código de catálogo de hasta 40 caracteres ASCII imprimibles si está fuera del espacio reservado `FT-`. En los demás casos se genera un código educativo a partir del identificador del producto. La vista previa estudiantil abre con 55 mm de alto para dar espacio a dosis e indicaciones. El etiquetador docente mantiene el formato inicial de 55 × 44 mm. Los modelos de detección son una hipótesis de experimentación y corren fuera de Django.
