import re

from django.core.exceptions import ValidationError


def normalizar_rut(valor: str) -> str:
    """Convierte 12345678k o 12.345.678-K en formato 12.345.678-K."""
    limpio = re.sub(r"[^0-9kK]", "", (valor or "")).upper()
    if len(limpio) < 2:
        return ""
    cuerpo, dv = limpio[:-1], limpio[-1]
    return f"{int(cuerpo):,}".replace(",", ".") + f"-{dv}"


def validar_rut(valor: str) -> None:
    limpio = re.sub(r"[^0-9kK]", "", valor or "").upper()
    if len(limpio) < 2 or not limpio[:-1].isdigit():
        raise ValidationError("Ingrese un RUT válido. Ejemplo: 12.345.678-9.")

    cuerpo, dv = limpio[:-1], limpio[-1]
    suma, multiplicador = 0, 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1
    resto = 11 - (suma % 11)
    esperado = "0" if resto == 11 else "K" if resto == 10 else str(resto)
    if dv != esperado:
        raise ValidationError("El dígito verificador del RUT no es válido.")
