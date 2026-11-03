from decimal import Decimal, ROUND_HALF_UP
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from .rubrica import RUBRICA, niveles_por_puntaje
from CliniTensFichaApp.models import FichaClinica


def guardar_evaluacion(ficha, usuario, puntajes, feedback, accion, version):
    limites = {codigo: {v for _, v in niveles_por_puntaje(maximo)}
               for codigo, _, maximo in RUBRICA}
    if not isinstance(puntajes, dict) or not set(puntajes) <= set(limites):
        raise ValidationError("La evaluación contiene criterios desconocidos.")
    if any(type(valor) is not int or valor not in limites[codigo]
           for codigo, valor in puntajes.items()):
        raise ValidationError("Todos los puntajes deben ser enteros de un nivel válido.")
    if len(feedback) > 5000 or accion not in {"guardar", "publicar"}:
        raise ValidationError("Acción o retroalimentación no válida.")
    if accion == "publicar" and set(puntajes) != set(limites):
        raise ValidationError("Debes evaluar todos los criterios antes de publicar.")
    changes = {"borrador_evaluacion": {"puntajes": puntajes, "retroalimentacion": feedback},
               "version": F("version") + 1, "actualizado_en": timezone.now()}
    if accion == "publicar":
        total = sum(puntajes.values())
        porcentaje = Decimal(total) * Decimal(100) / sum(x[2] for x in RUBRICA)
        nota = (Decimal(1) + porcentaje * Decimal(3) / Decimal(60) if porcentaje <= 60
                else Decimal(4) + (porcentaje - Decimal(60)) * Decimal(3) / Decimal(40))
        changes.update(evaluacion_rubrica={"puntajes": puntajes}, puntaje=total,
                       porcentaje=porcentaje.quantize(Decimal("0.01")),
                       calificacion=nota.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP),
                       retroalimentacion=feedback, estado=FichaClinica.Estado.CALIFICADA,
                       evaluada_por=usuario, evaluada_en=timezone.now(), borrador_evaluacion={})
    with transaction.atomic():
        return FichaClinica.objects.filter(pk=ficha.pk, version=version,
            estado__in=[FichaClinica.Estado.ENVIADA, FichaClinica.Estado.CALIFICADA]).update(**changes)
