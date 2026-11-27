from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from core.permissions import cargo, recetas_visibles_para_docente
from .models import (
    Dispensacion,
    DispensacionLote,
    LoteInventario,
    MovimientoInventario,
    Receta,
    RespuestaReceta,
)


def lotes_de_practica(receta):
    return LoteInventario.objects.filter(
        medicamento__creado_por_id=receta.creado_por_id,
        medicamento__activo=True,
        vence_el__gte=timezone.localdate(),
        unidades__gt=0,
    ).select_related("medicamento")


def _registrar_consumo_stock(receta, actor, cantidades, *, respuesta=None, lotes_elegidos=None):
    actualizar_saldo = respuesta is None
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
    # Acquire inventory locks in the same order across recipes.
    for linea in sorted(lineas, key=lambda linea: (linea.medicamento_id, linea.pk)):
        restante = cantidades[linea.pk]
        if restante == 0:
            continue
        lotes = LoteInventario.objects.select_for_update(of=("self",)).filter(
            medicamento=linea.medicamento,
            medicamento__activo=True,
            vence_el__gte=hoy,
            unidades__gt=0,
        ).order_by("vence_el", "creado_en", "id")
        if lotes_elegidos is not None:
            lotes = lotes.filter(pk=lotes_elegidos[linea.pk])
        for lote in lotes:
            tomar = min(restante, lote.unidades)
            actualizado = LoteInventario.objects.filter(
                pk=lote.pk, unidades__gte=tomar
            ).update(unidades=F("unidades") - tomar)
            if not actualizado:
                raise ValidationError("El inventario cambió durante la entrega; vuelve a intentar.")
            uso = DispensacionLote.objects.create(
                dispensacion=dispensacion,
                linea=linea,
                lote=lote,
                unidades=tomar,
            )
            MovimientoInventario.objects.create(lote=lote, actor=actor, sentido="salida",
                cantidad=tomar, saldo_anterior=lote.unidades, saldo_posterior=lote.unidades-tomar,
                motivo="dispensacion", uso=uso)
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


def _receta_docente_bloqueada(receta_id, actor):
    visibles = recetas_visibles_para_docente(Receta.objects.filter(pk=receta_id), actor)
    receta = Receta.objects.select_for_update().filter(pk__in=visibles.values("pk")).first()
    if not receta:
        raise ValidationError("No se encontró la receta en tu ámbito de acceso.")
    return receta


@transaction.atomic
def entregar_receta(receta_id, actor, cantidades):
    receta = _receta_docente_bloqueada(receta_id, actor)
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
def responder_receta(
    receta_id, estudiante, decision, motivo_rechazo="", *,
    lotes_elegidos=None, intento=1, explicacion_otro_motivo="",
):
    if not estudiante.is_active or cargo(estudiante) != "RESTRICTED":
        raise ValidationError("La práctica está disponible para estudiantes activos inscritos en el curso.")
    if decision not in RespuestaReceta.Decision.values:
        raise ValidationError("Selecciona dispensar o rechazar la receta.")
    if decision == RespuestaReceta.Decision.RECHAZAR and motivo_rechazo not in RespuestaReceta.Motivo.values:
        raise ValidationError("Selecciona un motivo de rechazo válido.")
    explicacion_otro_motivo = RespuestaReceta.limpiar_explicacion_otro(
        decision, motivo_rechazo, explicacion_otro_motivo,
    )

    receta = (
        Receta.objects.select_for_update(of=("self",))
        .filter(pk=receta_id, curso__estudiantes__pk=estudiante.pk)
        .select_related("curso")
        .first()
    )
    if not receta:
        raise ValidationError("No se encontró una receta de práctica en tus cursos.")
    anterior = RespuestaReceta.objects.filter(receta=receta, estudiante=estudiante).order_by("-intento").first()
    if anterior and not anterior.reintento_disponible:
        raise ValidationError("Ya respondiste este caso.")
    if intento != (2 if anterior else 1):
        raise ValidationError("El intento cambió. Revisa el estado de la receta antes de responder.")

    lineas = list(receta.lineas.order_by("pk"))
    if not lineas:
        raise ValidationError("La receta no tiene medicamentos asociados.")
    inventario = lotes_de_practica(receta)
    lotes_elegidos = lotes_elegidos or {}
    error_seleccion = ""
    if decision == RespuestaReceta.Decision.DISPENSAR:
        if set(lotes_elegidos) != {linea.pk for linea in lineas}:
            raise ValidationError("Selecciona un producto y un lote para cada línea de la receta.")
        lotes = inventario.filter(pk__in=lotes_elegidos.values()).order_by(
            "medicamento_id", "vence_el", "creado_en", "pk"
        ).select_for_update(of=("self",))
        seleccion = {lote.pk: lote for lote in lotes}
        if set(seleccion) != set(lotes_elegidos.values()):
            raise ValidationError("Un lote seleccionado ya no está disponible en esta práctica.")
        for numero, linea in enumerate(lineas, 1):
            lote = seleccion[lotes_elegidos[linea.pk]]
            if lote.medicamento_id != linea.medicamento_id:
                error_seleccion = f"En la línea {numero}, el producto o la presentación elegida difiere de la receta."
                break
            if lote.unidades < linea.unidades:
                error_seleccion = f"En la línea {numero}, el lote elegido no cubre las unidades indicadas."
                break

    if receta.vence_el < timezone.localdate():
        expected_reason = RespuestaReceta.Motivo.VENCIDA
    elif receta.sospecha_falsificacion:
        expected_reason = RespuestaReceta.Motivo.FALSIFICACION
    else:
        expected_reason = receta.motivo_rechazo_esperado
        if not expected_reason and any(
            not inventario.filter(medicamento_id=linea.medicamento_id, unidades__gte=linea.unidades).exists()
            for linea in lineas
        ):
            expected_reason = RespuestaReceta.Motivo.SIN_STOCK

    expected_decision = (
        RespuestaReceta.Decision.RECHAZAR
        if expected_reason
        else RespuestaReceta.Decision.DISPENSAR
    )
    correcta = decision == expected_decision and (
        decision != RespuestaReceta.Decision.RECHAZAR
        or motivo_rechazo == expected_reason
    ) and not error_seleccion
    reintento_disponible = intento == 1 and not correcta
    explicacion = ""
    respuesta_esperada = ""
    if not reintento_disponible:
        if expected_reason == RespuestaReceta.Motivo.SIN_STOCK:
            explicacion = "Al menos un producto de la receta no tiene un lote vigente con las unidades necesarias."
        elif error_seleccion and not expected_reason:
            explicacion = error_seleccion
        else:
            explicacion = receta.retroalimentacion_docente.strip() or (
                "La decisión o el motivo elegido no coincide con la validación de esta receta."
                if not correcta else "La decisión coincide con las condiciones de la práctica."
            )
        if not correcta:
            if expected_reason:
                motivo = dict(RespuestaReceta.Motivo.choices).get(expected_reason, expected_reason)
                respuesta_esperada = f"Rechazar receta por: {motivo}."
            else:
                respuesta_esperada = "Dispensar los medicamentos indicados con lotes vigentes que cubran las cantidades."
    respuesta = RespuestaReceta.objects.create(
        receta=receta,
        estudiante=estudiante,
        decision=decision,
        motivo_rechazo=motivo_rechazo if decision == RespuestaReceta.Decision.RECHAZAR else "",
        explicacion_otro_motivo=explicacion_otro_motivo,
        correcta=correcta,
        intento=intento,
        reintento_disponible=reintento_disponible,
        explicacion=explicacion,
        respuesta_esperada=respuesta_esperada,
    )

    if correcta and decision == RespuestaReceta.Decision.DISPENSAR:
        cantidades = {
            linea.pk: linea.unidades
            for linea in lineas
        }
        if any(linea.unidades_entregadas for linea in lineas):
            raise ValidationError("El caso ya registra una entrega docente y no se puede dispensar en la práctica.")
        _registrar_consumo_stock(
            receta,
            estudiante,
            cantidades,
            respuesta=respuesta,
            lotes_elegidos=lotes_elegidos,
        )
    return respuesta


@transaction.atomic
def eliminar_receta(receta_id, actor):
    receta = _receta_docente_bloqueada(receta_id, actor)
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
