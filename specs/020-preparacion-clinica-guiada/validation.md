# Validación — 020

Implementación local en `jonathan`, cambios 019 conservados. Python/requirements de `.test-artifacts/clinica-019-env`, `core.test_settings`, base ficticia exclusivamente. Aceptación humana pendiente.

Ejecutado: `manage.py test homeApp UsuarioApp CliniTensDocenteApp CliniTensFichaApp FarmaTEFApp CliniTensSimulacionApp --settings=core.test_settings`: 66 correctas, incluidas cinco nuevas del recorrido guiado. Cotejo `makemigrations --check --dry-run`: sin cambios. Cuatro pruebas JS correctas. Build `node build.cjs` desde `theme/static_src`: Tailwind 4.3.3 correcto. Un intento desde raíz falló por ruta y se corrigió. Se repitieron las 19 pruebas de simulación tras ajustes de interfaz: detectaron una instrucción de guardado que aún aparecía en solo lectura; se corrigió el texto para publicados y la repetición pasó.

RF-020-01/02: Chrome sin ventana mediante el puente stdio de 019 (Django/CSRF reales sin red HTTP). Fixture exclusiva `guia-visual020`/curso propio, sin alterar los casos que prepara el usuario. Se completaron paciente, DAU, laboratorio, diagnóstico, revisión y publicación, comprobando destinos de cada redirect. Se corrigió el formato ISO del campo fecha HTML para mantenerlo al avanzar de paciente a DAU. Un primer fallo del harness esperaba `/diagnostico/` en vez de la ruta real `/centro-diagnostico/`; corregido sin modificar rutas de producto.

RF-020-03/04: pruebas de pendientes/condiciones de publicación, bloqueo publicado, POST con caso_id distinto del seleccionado, selección inválida/ajena, estudiante denegado, conservación de errores y alta al primer paso. No se cambian requisitos de publicación ni se certifica concurrencia de preparación docente.

RF-020-05: capturas revisadas de tarjetas 1440px y paciente 390px; revisión final a 1440/390. H1 único, ancho del documento igual al viewport y cero errores JavaScript durante el recorrido. Evidencia en `docs/evidencias/020-preparacion/navegador.json` y PNG vecinos. No probado zoom real 200%, otros motores ni recorrido completo de teclado. El puente no valida un servidor/red HTTP real. No se modifican PDF/Excel.

Sin migraciones nuevas, base habitual, despliegue, commit/push. Próximo paso: el usuario reabre el listado y prueba «Continuar preparación» con su caso. Su servidor se inició sin `--noreload`; si no detecta el código nuevo, reiniciar el mismo comando de prueba en 8019. No confundir este alcance con hacer módulos opcionales para publicar RAE.


## Revisión de módulos existentes y orden de textos

Se ejecutó `git fetch origin` sin checkout ni cambios de rama. Referencias resultantes: main b3feef5, jonathan y valentina df23932. Comparados código/rutas/modelos/formularios/plantillas y tests de CliniTensDocenteApp y CliniTensFichaApp. Las 59 fuentes Python/HTML protegidas coinciden entre HEAD y origin/valentina/origin/jonathan. Main carece únicamente de la ampliación de colaboradores en esos directorios (seis archivos), no de los módulos mostrados. La copia OneDrive conserva 53 archivos iguales normalizando finales de línea, cinco distintos y una migración ausente; sus diferencias corresponden al mismo incremento anterior. No se leen bases ni medios de esa copia.

| Pantalla de las capturas | Implementación existente comprobada | Comprobación funcional aislada |
|---|---|---|
| Panel docente | DashboardDocenteView y métricas sobre FichaClinica/CasoClinico/Paciente | Caso propio y ficha ENVIADA incrementan contadores |
| Casos clínicos | CasoClinicoListCreateView, edición, previsualización, borrado protegido | Alta por POST 302 y listado propio con un registro |
| Códigos | CodigoListCreateView, relación caso/curso y toggle | Alta POST, activación y listado con un código |
| Pacientes | PacienteListCreateView, edición/detalle/borrado | Alta POST ficticia, listado con paciente propio |
| Apoyo diagnóstico | ResultadoListCreateView, publicación/habilitación y archivos privados | Alta POST de informe ficticio y listado con resultado |
| Estudiantes | EstudiantesListView sobre fichas ENVIADA/CALIFICADA | Ficha sintética enviada aparece en listado |
| En vivo | EnVivoView, filtros y actualización declarada de 30 s | Curso/código sintéticos muestran alumno inscrito |

Toda la integración adicional se ejecutó con core.test_settings, migraciones en memoria y usuarios nuevos de auditoría, sin adjuntos reales. Otro docente ve listas vacías; estudiante recibe 403 al panel. La suite completa volvió a pasar: 66 pruebas. Esto no acredita todas las acciones CRUD, SMTP, carga ni todas las interacciones de esas pantallas; no se cambiaron para extender su cobertura.

Los ceros de las capturas se explican por sus querysets tradicionales: CasoClinico/Paciente/FichaClinica. Juan pertenece a CasoSimulacion y AtencionEnfermeria; esos registros no alimentan los contadores tradicionales. No se unieron tablas, migraron datos ni duplicaron capacidades para ocultar esa separación. La ficha tradicional sigue su evaluación existente; no se añadió evaluación automática ni clave docente a RAE.

RF-020-06/07 implementados solo en paciente RAE y guía nueva: identificación, datos de referencia y antecedentes en fieldsets; lectura estudiantil separa situación y antecedentes; instrucciones para escribir cuidados/observaciones. Estados “Falta preparar”/“Preparación guardada” distinguen trabajo docente de revisiones del alumno. Se conservan contratos POST, validación, versión y datos ingresados. Se mantuvieron intactos los motores DAU/laboratorio/CAD y las apps/plantillas tradicionales. Ningún archivo funcional nuevo para este ajuste; se reutilizaron archivos y paquete 020.

Build 4.3.3 correcto. Navegador Chrome con puente Django/CSRF de pruebas: formulario RAE a 1440/390 y registro estudiantil a 390, H1 único y sin overflow; tres fieldsets y cuatro estados “Falta preparar” comprobados. Capturas inspeccionadas en paciente-ordenado-1440.png y rae-ordenado-390.png; reporte orden-textos.json en la carpeta de evidencia 020. Identidades/casos propios de revisión visual, sin alterar Juan ni registros preparados por el usuario. No se simula un tratamiento ni se interpreta información clínica. Aceptación visual del usuario pendiente.
