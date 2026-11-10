"""Avance de preparación según las condiciones existentes de publicación."""
from django.urls import reverse


def paso_url(caso, modulo):
    return reverse(f"clinitens_simulacion:docente_{modulo}") + f"?caso={caso.pk}"


def preparacion_caso(caso):
    requisitos = [
        ("enfermeria", "Paciente", bool(caso.paciente_codigo and caso.paciente_nombre), "Completa la identificación del paciente ficticio."),
        ("dau", "Urgencia", bool(caso.escenario_dau.strip()), "Describe el escenario de atención de urgencia."),
        ("laboratorio", "Laboratorio", bool(caso.ordenes_laboratorio), "Agrega al menos un examen con su muestra y tubo."),
        ("diagnostico", "Apoyo diagnóstico", bool(caso.documentos_diagnosticos), "Agrega al menos un resultado o informe ficticio."),
    ]
    pasos = [dict(modulo=modulo, nombre=nombre, completo=completo, ayuda=ayuda,
                  numero=i + 1, url=paso_url(caso, modulo))
             for i, (modulo, nombre, completo, ayuda) in enumerate(requisitos)]
    pendientes = [paso for paso in pasos if not paso["completo"]]
    revision = reverse("clinitens_simulacion:preparar_caso", args=[caso.pk])
    return dict(caso=caso, pasos=pasos, pendientes=pendientes, listo=not pendientes,
                completados=4-len(pendientes), revision_url=revision,
                continuar_url=pendientes[0]["url"] if pendientes and not caso.publicado else revision,
                siguiente_nombre=pendientes[0]["nombre"] if pendientes else "Revisar y publicar")
