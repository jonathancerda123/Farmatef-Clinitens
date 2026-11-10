# 020 — Preparación clínica guiada por caso

Fecha: 2026-11-09. Petición: el usuario se pierde desde las tarjetas de casos y exige mayor facilidad de uso. Corrección de recorrido autorizada por ese reporte; aceptación humana pendiente. Preservar todos los cambios 019 en `jonathan`.

Observado: cada tarjeta ofrece cuatro enlaces sin avance ni siguiente acción. Los enlaces llevan a todos los casos del módulo, perdiendo el contexto. Crear/guardar devuelve a listados y publicar ofrece un rechazo genérico cuando falta información.

RF-020-01: cada tarjeta presenta avance, próximo paso y una acción principal para continuar la preparación del caso elegido.
RF-020-02: recorrido Paciente → Urgencia → Laboratorio → Apoyo diagnóstico → Revisar y publicar. Formularios existentes filtrados al caso autorizado; guardado correcto continúa al siguiente paso, errores conservan contexto/valores. Accesos generales a módulos siguen disponibles.
RF-020-03: revisión presenta lo preparado, lo pendiente y enlaces para corregir; publicar solo disponible en interfaz cuando cumple las condiciones actuales. El servidor vuelve a validar las mismas condiciones existentes.
RF-020-04: URL/POST con caso ajeno o diferente al seleccionado no revela ni modifica datos. Publicados conservan solo lectura. Sin modelos/migraciones ni cambio de requisitos de publicación.
RF-020-05: identidad visual actual, H1 único, teclado y móvil; pruebas en settings aislados. Sin tocar base habitual, commit o push.

No se hace opcional laboratorio/CAD para RAE en esta corrección; ese cambio de reglas requiere un alcance separado. La guía hace explícitos los requisitos actuales.


## Revisión solicitada de módulos y textos

El usuario confirma Juan visible al estudiante y pide verificar las ramas/copia completa antes de crear módulos; prohíbe cambiar los módulos existentes de sus capturas. Se actualizan referencias remotas sin checkout: origin/jonathan y origin/valentina siguen en df23932; main en b3feef5. Panel/casos/códigos/pacientes/resultados/estudiantes/en vivo ya existen. No se crean sustitutos ni se modifica CliniTensDocenteApp, CliniTensFichaApp o sus plantillas. Se registran hashes de 59 archivos protegidos para comprobar conservación. La copia OneDrive es anterior; sus diferencias se corresponden con colaboración docente, no con módulos ausentes.

RF-020-06: ordenar solo el formulario nuevo de paciente RAE por identificación/datos de referencia/antecedentes, y la lectura estudiantil por paciente/situación/antecedentes/contexto académico. Conservar nombres POST, límites, datos guardados y control de versión.
RF-020-07: los estados de preparación deben distinguir contenido que el docente aún debe completar de una revisión clínica o actividad pendiente del estudiante. No cambiar las condiciones de publicación ni unir modelos tradicionales con simulaciones.

Verificar el comportamiento existente con datos sintéticos y registrar la diferencia entre presencia de código, prueba funcional y datos de demostración vacíos. Los cambios de interfaz usan frontend-design ya cargada y tokens existentes. Sin archivos funcionales nuevos para este ajuste, migraciones, commit/push ni lectura de datos habituales.
