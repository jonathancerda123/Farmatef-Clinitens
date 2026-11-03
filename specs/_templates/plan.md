# Plan técnico — <NNN / cambio de CliniTENS>

Spec: [spec.md](spec.md). Propuesta documental; código no autorizado.

## Base inspeccionada

<Archivos reales y cambios locales a preservar. Config normal core/settings.py; core/test_settings.py independiente para fixtures. Apps/permisos en docs/ARQUITECTURA_BASE y presentación en docs/PERSONALIZACION_VISUAL.>

## Integración propuesta

<Ampliar módulo existente o justificar uno nuevo. Reutilizar User/Profile/Position, allauth, mixins y layouts; no reconstruirlos por copiar una plantilla.>

| RF | Archivo existente / propuesto | Cambio | Verificación prevista |
|---|---|---|---|
| <ID> | <ruta y estado> | <acción> | <prueba pertinente> |

## Datos, contratos y permisos

<Modelos/formularios/POST, validación servidor, esquema JSON si aplica, estados, propiedad, transacciones/concurrencia, precisión y manejo de errores. Superusuario por operación.>

## Interfaz y estilos

<Templates reales en templates/pages; estructura común components/Layout/app_shell.html y guía PERSONALIZACION_VISUAL. Tailwind 4 en theme/static_src; @source explícitos incluyen HTML/Python/JS del proyecto; @config carga config JS de compatibilidad. Justificar CSS/build/navegación; no crear archivos en DOCUMENTAR.>

## Migraciones, compatibilidad y reversión

<Ninguna o cambio propuesto, respaldo ficticio, conservación y recuperación. Migraciones actuales disponibles en Git desde 002; no aplicar a base recibida sin autorización y respaldo.>

## Pruebas y riesgos

<Casos normales/denegados/límite por RF. Suite existente: 47 Django/3 JS con core.test_settings; añadir regresión pertinente si corresponde. Navegador/PDF/Excel según alcance; tamaños/teclado/errores para UI. No usar datos reales.>

## Documentos y decisiones pendientes

<Spec/tareas/validation/docs afectados, OBS relacionados, decisiones críticas. Detenerse antes de código si no está autorizado.>
