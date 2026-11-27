"""Operaciones de inventario: saldo e historial se confirman juntos."""
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import transaction
from django.utils import timezone

from core.permissions import es_administrador, es_docente_de_area
from UsuarioApp.models import AreaDocente
from .models import LoteInventario, MovimientoInventario


def autorizar(actor, medicamento):
    if not es_docente_de_area(actor, AreaDocente.FARMACIA) or (
        medicamento.creado_por_id != actor.pk and not es_administrador(actor)
    ):
        raise PermissionDenied


@transaction.atomic
def registrar_alta(lote, actor):
    autorizar(actor, lote.medicamento)
    lote.registrado_por = actor
    lote.full_clean()
    lote.save()
    if lote.unidades:
        MovimientoInventario.objects.create(
            lote=lote, actor=actor, motivo="ingreso", sentido="entrada",
            cantidad=lote.unidades, saldo_anterior=0, saldo_posterior=lote.unidades,
        )
    return lote


@transaction.atomic
def mover_stock(actor, lote_id, sentido, cantidad, motivo, observacion, operacion):
    lote = LoteInventario.objects.select_for_update().select_related("medicamento").get(pk=lote_id)
    autorizar(actor, lote.medicamento)
    anterior = MovimientoInventario.objects.filter(operacion=operacion).first()
    if anterior:
        if (anterior.actor_id, anterior.lote_id, anterior.sentido, anterior.cantidad, anterior.motivo, anterior.observacion) != (
            actor.pk, lote.pk, sentido, cantidad, motivo, observacion
        ):
            raise ValidationError("Este formulario ya se utilizó para otra operación. Recarga la página.")
        return anterior
    if type(cantidad) is not int or not 1 <= cantidad <= 2147483647:
        raise ValidationError("Indica una cantidad entera positiva válida.")
    if sentido not in ("entrada", "salida") or motivo not in dict(MovimientoInventario.MOTIVOS):
        raise ValidationError("Movimiento no válido.")
    if motivo in ("venta", "vencimiento", "dispensacion") and sentido != "salida":
        raise ValidationError("Este motivo corresponde a una salida.")
    if motivo == "ingreso" and sentido != "entrada":
        raise ValidationError("El ingreso corresponde a una entrada.")
    if motivo == "vencimiento" and lote.vence_el >= timezone.localdate():
        raise ValidationError("El lote aún no está vencido.")
    if not isinstance(observacion, str) or len(observacion) > 300 or (motivo == "otro" and not observacion.strip()):
        raise ValidationError("Indica una observación de hasta 300 caracteres; es obligatoria para Otro.")
    nuevo = lote.unidades + (cantidad if sentido == "entrada" else -cantidad)
    if not 0 <= nuevo <= 2147483647:
        raise ValidationError("La cantidad supera el saldo o el límite del lote.")
    if not LoteInventario.objects.filter(pk=lote.pk, unidades=lote.unidades).update(unidades=nuevo):
        raise ValidationError("El inventario cambió. Recarga antes de reintentar.")
    return MovimientoInventario.objects.create(
        lote=lote, actor=actor, sentido=sentido, cantidad=cantidad, motivo=motivo,
        saldo_anterior=lote.unidades, saldo_posterior=nuevo,
        observacion=observacion, operacion=operacion,
    )
