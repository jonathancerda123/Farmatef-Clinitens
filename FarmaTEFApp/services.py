from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from core.permissions import cargo, recetas_visibles_para_docente
from .models import (
    Dispensacion,
    DispensacionLote,
    LoteInventario,
    Receta,
    RespuestaReceta,
)


def _registrar_consumo_stock(receta, actor, cantidades, *, respuesta=None, actualizar_saldo=True):
    lineas = list(receta.lineas.select_related("medicamento").order_by("id"))
    if not lineas:
        raise ValidationError("La receta no tiene medicamentos asociados.")
    permitidos = {linea.pk: linea.unidades_pendientes if actualizar_saldo else linea.unidades for linea in lineas}
    if set(cantidades) != set(permitidos):
        raise ValidationError("La solicitud de entrega no coincide con las líneas de la receta.")
    for linea_id, unidades in cantidades.items():
        if not isinstance(unidades, int) or unidades < 0 or unidades > permitidos[linea_id]:
            raise ValidationError("Las unidades solicitadas deben estar entre cero y el saldo pendiente.")
    if not any(cantidades.values()):
        raise ValidationError("Indica al menos una unidad para entregar.")

    dispensacion = Dispensacion.objects.create(
        receta=receta,
        respuesta=respuesta,
        entregado_por=actor,
        es_simulada=True,
    )
    hoy = timezone.localdate()
    for linea in lineas:
        restante = cantidades[linea.pk]
        if restante == 0:
            continue
        lotes = LoteInventario.objects.select_for_update().filter(
            medicamento=linea.medicamento,
            medicamento__activo=True,
            vence_el__gte=hoy,
            unidades__gt=0,
        ).order_by("vence_el", "creado_en", "id")
        for lote in lotes:
            tomar = min(restante, lote.unidades)
            actualizado = LoteInventario.objects.filter(
                pk=lote.pk, unidades__gte=tomar
            ).update(unidades=F("unidades") - tomar)
            if not actualizado:
                raise ValidationError("El inventario cambió durante la entrega; vuelve a intentar.")
            DispensacionLote.objects.create(
                dispensacion=dispensacion,
                linea=linea,
                lote=lote,
                unidades=tomar,
            )
            restante -= tomar
            if not restante:
                break
        if restante:
            raise ValidationError(
                f"Stock insuficiente de {linea.medicamento.nombre}; no se guardó ninguna parte de esta entrega."
            )
        if actualizar_saldo:
            linea.unidades_entregadas += cantidades[linea.pk]
            linea.save(update_fields=["unidades_entregadas"])
    return lineas


@transaction.atomic
def entregar_receta(receta_id, actor, cantidades):
    receta = recetas_visibles_para_docente(
        Receta.objects.select_for_update(), actor
    ).filter(pk=receta_id).first()
    if not receta:
        raise ValidationError("No se encontró la receta en tu ámbito de acceso.")
    if receta.curso_id:
        raise ValidationError("Esta receta pertenece a una práctica de curso; no admite despacho docente manual.")
    if receta.estado == Receta.Estado.ENTREGADA:
        raise ValidationError("Esta receta ya está completamente entregada.")
    if receta.sospecha_falsificacion:
        raise ValidationError("La receta está marcada con sospecha de falsificación y no se puede dispensar en esta simulación.")
    if receta.vence_el < timezone.localdate():
        raise ValidationError("La receta está vencida y no puede entregarse.")

    lineas = _registrar_consumo_stock(receta, actor, cantidades)
    todas_completas = all(
        linea.unidades_entregadas == linea.unidades for linea in lineas
    )
    receta.estado = Receta.Estado.ENTREGADA if todas_completas else Receta.Estado.PARCIAL
    receta.entregado_por = actor
    receta.entregado_en = timezone.now()
    receta.save(update_fields=["estado", "entregado_por", "entregado_en"])
    return receta


@transaction.atomic
def responder_receta(receta_id, estudiante, decision, motivo_rechazo=""):
    if not estudiante.is_active or cargo(estudiante) != "RESTRICTED":
        raise ValidationError("La práctica está disponible para estudiantes activos inscritos en el curso.")
    if decision not in RespuestaReceta.Decision.values:
        raise ValidationError("Selecciona dispensar o rechazar la receta.")
    if decision == RespuestaReceta.Decision.RECHAZAR and motivo_rechazo not in RespuestaReceta.Motivo.values:
        raise ValidationError("Selecciona un motivo de rechazo válido.")

    receta = (
        Receta.objects.select_for_update()
        .filter(pk=receta_id, curso__estudiantes__pk=estudiante.pk)
        .select_related("curso")
        .first()
    )
    if not receta:
        raise ValidationError("No se encontró una receta de práctica en tus cursos.")
    if RespuestaReceta.objects.filter(receta=receta, estudiante=estudiante).exists():
        raise ValidationError("Ya respondiste este caso.")

    if receta.vence_el < timezone.localdate():
        expected_reason = RespuestaReceta.Motivo.VENCIDA
    elif receta.sospecha_falsificacion:
        expected_reason = RespuestaReceta.Motivo.FALSIFICACION
    else:
        expected_reason = receta.motivo_rechazo_esperado

    expected_decision = (
        RespuestaReceta.Decision.RECHAZAR
        if expected_reason
        else RespuestaReceta.Decision.DISPENSAR
    )
    correcta = decision == expected_decision and (
        decision != RespuestaReceta.Decision.RECHAZAR
        or motivo_rechazo == expected_reason
    )
    explanation = receta.retroalimentacion_docente.strip()
    if not explanation:
        if expected_decision == RespuestaReceta.Decision.DISPENSAR:
            explanation = "El caso estaba habilitado para dispensación simulada."
        else:
            explanation = f"La respuesta esperada era rechazar por: {dict(RespuestaReceta.Motivo.choices).get(expected_reason, expected_reason)}."
    respuesta = RespuestaReceta.objects.create(
        receta=receta,
        estudiante=estudiante,
        decision=decision,
        motivo_rechazo=motivo_rechazo if decision == RespuestaReceta.Decision.RECHAZAR else "",
        correcta=correcta,
        explicacion=explanation,
    )

    if correcta and decision == RespuestaReceta.Decision.DISPENSAR:
        cantidades = {
            linea.pk: linea.unidades
            for linea in receta.lineas.all()
        }
        if any(linea.unidades_entregadas for linea in receta.lineas.all()):
            raise ValidationError("El caso ya registra una entrega docente y no se puede dispensar en la práctica.")
        _registrar_consumo_stock(
            receta,
            estudiante,
            cantidades,
            respuesta=respuesta,
            actualizar_saldo=False,
        )
    return respuesta


@transaction.atomic
def eliminar_receta(receta_id, actor):
    receta = recetas_visibles_para_docente(
        Receta.objects.select_for_update(), actor
    ).filter(pk=receta_id).first()
    if not receta:
        raise ValidationError("No se encontró una receta en tu ámbito de acceso.")
    tiene_entrega_registrada = (
        receta.estado != Receta.Estado.PENDIENTE
        or receta.entregado_en is not None
        or receta.entregado_por_id is not None
        or receta.lineas.filter(unidades_entregadas__gt=0).exists()
    )
    if (
        receta.respuestas_estudiantiles.exists()
        or receta.dispensaciones.exists()
        or tiene_entrega_registrada
    ):
        raise ValidationError(
            "No se puede eliminar esta receta porque ya tiene respuestas o datos de entrega; su historial se conserva."
        )

    numero = receta.numero
    receta.lineas.all().delete()
    receta.delete()
    return numero
