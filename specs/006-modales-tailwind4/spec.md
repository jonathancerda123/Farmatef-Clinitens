# 006 — Compatibilidad de modales con Tailwind 4

Fecha: 2026-10-21. Estado actual: implementación local autorizada, comprobaciones ejecutadas con límites visuales pendientes. Área: transversal, con consumidores en UsuarioApp y CliniTensDocenteApp. Fuente: reporte del usuario de problemas en modales después del paso de Tailwind 3 a 4. El usuario revisó el paquete documental y autorizó posteriormente implementar. La aceptación funcional final permanece pendiente.

## Problema, actores y resultado

Se solicita recuperar la presentación y operación de los modales existentes en varios módulos. El usuario no precisó una pantalla ni describió si falla apertura, centrado, cierre o superposición. No hay reproducción en navegador en esta entrega; no se atribuye todo fallo de modal a Tailwind.

Actores: administrador/superusuario activo en cuentas; docente MANAGER, ADMIN y superusuario activo en pacientes. El resultado esperado es poder abrir, leer y cerrar los diálogos autorizados, con tamaño adaptable, foco utilizable y acciones existentes conservadas.

Se relaciona con RF-004-02 (compatibilidad Tailwind) y RF-003-03/05/06 (diálogos, adaptación y teclado). Es corrección de comportamiento esperado, no cambio de las reglas de negocio. Se abre 006 por el alcance transversal solicitado y los patrones distintos observados; se conservan la evidencia histórica de 003/004 y el trabajo independiente de 005.

## Base observada y diagnóstico provisional

| Elemento real | Observado el 2026-10-21 | Interpretación y límite |
|---|---|---|
| `theme/static_src/package.json`, `src/styles.css` y `node_modules/tailwindcss/preflight.css` | Manifiesto fija Tailwind/CLI 4.3.3; fuente importa Preflight, que aplica margen cero universal | No se reinstaló ni compiló; la versión declarada no acredita funcionamiento visual |
| `templates/pages/usuarios/usuarios_lista.html`, `static/css/styles.css` | Confirmación usa `dialog.account-dialog`, `showModal()` y `close()`; CSS define ancho, padding, borde y backdrop, sin margen automático explícito | Candidato principal: pérdida del centrado tras el reset de v4; síntoma aún no reproducido |
| `templates/pages/clinitens/docente/pacientes.html` | Vista previa usa contenedor fijo, flex, `x-show`, `x-cloak`, Escape y cierre exterior; consulta JSON con comprobación HTTP | No usa `dialog`; no se le aplica automáticamente la explicación de márgenes. Revisar como consumidor activo y regresión, sin presumir defecto |
| `templates/components/modal/modal.html`, `static/js/modal.js` | Componente mezcla `dialog`, clase `hidden` y `x-show`; helper cambia `style.display` tras sanitizar HTML; `aria-labelledby` no corresponde a un ID presente y el título es H1 | Riesgos estáticos adicionales. La búsqueda en plantillas y JS propios no localizó includes, llamadas activas ni carga del helper; no se justifica refactorizarlos por existencia solamente |
| FarmaTEF, ficha y portadas | No se localizaron otros consumidores de estos patrones en la búsqueda acotada | Regresión de estilos compartidos; no añadir modales a módulos que no los tienen |

La [guía oficial de migración, «Dialog margins removed»](https://tailwindcss.com/docs/upgrade-guide#dialog-margins-removed), consultada el 2026-10-21, confirma que v4 elimina el margen predeterminado de `dialog`. Esto respalda la hipótesis de centrado, no demuestra el síntoma de esta instalación. El [estándar HTML de dialog](https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element) diferencia la apertura modal nativa de la mera presentación CSS.

Git: `git status --short` devolvió «not a git repository»; `.git` no existe en esta carpeta. No se puede determinar rama, commit ni cambios locales contra una revisión. Los archivos presentes son la referencia de esta inspección y deben preservarse.

## Alcance y exclusiones

Incluye reproducir el fallo con datos ficticios, corregir únicamente las incompatibilidades comprobadas de presentación/interacción en los consumidores activos y verificar regresiones en los otros módulos. Se propone empezar por el centrado del diálogo de cuentas. Revisar pacientes no implica reescribir su patrón.

El componente/helper compartido queda inventariado; su modificación está condicionada a localizar un consumidor real afectado y documentarlo. No crear consumidores, demostraciones o endpoints para activar código actualmente sin uso localizado.

Sin rediseño integral, bibliotecas nuevas, cambio de versión de Tailwind, modelos, migraciones, rutas nuevas, reglas de permisos o contratos de formulario. No incluye reparar el runtime, desarrollar el roadmap FarmaTEF, desplegar, commit/push ni operar sobre datos recibidos. Durante DOCUMENTAR no se crea código, prototipo ni prueba ejecutable.

## Permisos por acción/dato: conservar 002

| Acción existente | Anónimo | RESTRICTED | MANAGER | ADMIN activo | Superusuario activo | Restricción |
|---|---|---|---|---|---|---|
| Listar cuentas / confirmar desactivación | Login | Denegado | Denegado | Permitido | Permitido, incluso sin perfil | No desactivar superusuario; propia cuenta rechazada sin modificación; POST/CSRF existentes |
| Listar / consultar detalle de paciente | Login | Denegado | Solo propios | Global | Global, incluso sin perfil | Filtro de propiedad en servidor; ID ajeno no expone datos |

Usuarios inactivos o sin perfil/cargo no obtienen autorización por abrir un modal; excepción existente del superusuario activo conservada. Ficha estudiantil sigue siendo propia y matrícula sigue obligatoria cuando el código tiene curso. No se amplían accesos por navegación, contenido precargado o URLs directas.

## Flujo, requisitos y aceptación propuesta

1. Usuario autorizado abre una página existente y activa su diálogo.
2. La ventana se muestra sobre la página, sin recorte de título/acciones; contenido largo se desplaza dentro de un área acotada.
3. Cancelar/cerrar/Escape no envían formularios ni cambian datos; foco vuelve al activador. El clic exterior conserva el comportamiento de cada consumidor: pacientes cierra; no se introduce cierre exterior nuevo en cuentas.
4. Desactivar cuenta mantiene su POST/CSRF y restricciones. Detalle de paciente mantiene lectura JSON y autorización.

| RF | Dado / cuando | Entonces verificable | Negativo / límite |
|---|---|---|---|
| RF-006-01 | Se abre el diálogo de cuentas en 1440, 768 y 390 px | Centrado explícito compatible con v4, margen visible, título y botones accesibles; contenido largo permite desplazamiento | Cerrado no aparece al cargar ni intercepta la página; zoom 200% sin perder acciones |
| RF-006-02 | Se abre/cierra un modal activo con teclado o sus controles | Estado visible y estado modal coherentes, nombre accesible, foco inicial dentro, Tab/Shift+Tab contenidos, Escape cierra y foco retorna | Fondo no operable mientras esté modal; cierre repetido y reapertura no dejan capa bloqueante; movimiento reducido respetado |
| RF-006-03 | Se abre la vista previa de pacientes y la consulta tarda, falla o se repite | Se conserva carga visible, error entendible y cierre recuperable; no se muestran datos de otro paciente por una respuesta tardía | Ensayar error HTTP, red y apertura A seguida de B; corrección solo si se reproduce defecto en este flujo |
| RF-006-04 | Se usan o cancelan acciones existentes y se solicitan URLs directas | Mismos métodos, CSRF, filtros, roles y propiedad; cerrar/cancelar no modifica datos | Cuentas: rol denegado, propia cuenta y superusuario protegidos; pacientes: ajeno/anónimo/inactivo/sin cargo denegados según contrato existente |
| RF-006-05 | Se compilan estilos y se recorren los módulos existentes | CSS de modales presente, build conserva salida previa ante fallo; navegación, formularios y avisos mantienen su presentación | No editar CSS generado a mano, no ampliar escaneo a datos/entornos; evidencia nueva separada de las 47 Django/4 JS históricas |

RF-006-02 concreta la interacción modal y teclado de 003. RF-006-03 delimita regresiones del flujo asíncrono existente; no autoriza nuevas funciones clínicas. La aceptación de esta tabla está pendiente de revisión.

## Decisiones y pendientes

- D-023/D-024 en [decisiones](../../docs/DECISIONES.md): fase documental y solución mínima basada en consumidores reales. Ninguna decisión reemplaza permisos o políticas previas.
- P-006-01: identificar en reproducción la pantalla/síntoma originalmente reportado y registrar antes/después. Pendiente técnico; no bloquea esta documentación. No fijar causa raíz antes de esa evidencia.
- P-006-02: el entorno Django válido está pendiente según `docs/ENTORNO_Y_VERIFICACION.md`; no se intentó arrancarlo aquí. Bloquea validación integrada si continúa indisponible.
- P-006-03: revisión de spec/plan/tareas e instrucción posterior del usuario. Bloquea implementación; no se infiere aprobación del texto inicial «puedes IMPLEMENTAR» frente a la orden final de detenerse.

Revisión 2026-10-21: documentación inicial. Arquitectura propuesta, código y pruebas sin ejecutar, aceptación humana pendiente.

### Autorización posterior — 2026-10-21

El usuario revisó el paquete y respondió «ya revisé, puedes implementar». Quedan autorizadas T-006-02 a T-006-07 y sus comprobaciones aisladas. P-006-03 resuelto; las menciones anteriores a la espera de instrucción describen la entrega documental previa. No autoriza despliegue, commit/push ni operación sobre datos recibidos. La aceptación funcional final continúa pendiente.

### Resultado implementado — 2026-10-21

P-006-01: reproducido el diálogo de cuentas en (0,0), margen cero; corregido con margen automático y límites de tamaño/scroll acotados a los dos diálogos activos. En pacientes se reprodujo foco detrás del overlay; ahora usa `dialog` nativo con nombre, cierre siempre disponible y fondo inerte. Cuatro regresiones del controlador demostraron respuestas/fallos antiguos que alteraban consultas posteriores, datos repoblados después de cerrar y cierre ante error sin recuperación en el propio diálogo; corregidos mediante versión de solicitud y error visible. Se añadió una quinta regresión de clic exterior.

P-006-02: resuelto para comprobar 006 usando el Python 3.12 instalado y paquetes del target mediante el arnés aislado; el launcher anterior sigue roto y no se reparó. El runtime informa 3.12.0: no se presenta como entorno parcheado de producción. No se actualizan dependencias ni se trasladan estos resultados a 005.

El helper/componente sin consumidores sigue intacto. Pruebas: 35 Django, 9 JS y build correctos; navegador a 1440/768/390, foco, Escape, cierre exterior y contenido largo. Zoom real 200% y emulación de movimiento reducido quedan pendientes; evidencia y alcance exacto en [validation.md](validation.md). No se declara aceptación completa de los RF con comprobaciones pendientes.
