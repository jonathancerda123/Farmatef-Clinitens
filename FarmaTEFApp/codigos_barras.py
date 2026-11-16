import base64
from io import BytesIO
from math import ceil
import re

from PIL import Image, ImageDraw
from reportlab.graphics.barcode.code128 import Code128


def codigo_para_etiqueta(medicamento):
    codigo = medicamento.codigo_barras.strip()
    if re.fullmatch(r"[ -~]{1,40}", codigo) and not re.fullmatch(r"FT-\d+", codigo, re.IGNORECASE):
        return codigo
    return f"FT-{medicamento.pk}"


def patron_code128(codigo):
    simbolo = Code128(codigo)
    simbolo.validate()
    simbolo.encode()
    return simbolo.decompose()


def ancho_code128(patron):
    modulos = sum(ord(tramo.lower()) - ord("a") + 1 for tramo in patron)
    # Módulo de 0,26 mm y zonas de silencio de diez módulos por lado.
    return ceil((modulos + 20) * 0.26)


def imagen_code128(patron):
    puntos = 8
    silencio = 10 * puntos
    tramos = [(ord(tramo.lower()) - ord("a") + 1) * puntos for tramo in patron]
    imagen = Image.new("1", (sum(tramos) + 2 * silencio, 160), 1)
    dibujo = ImageDraw.Draw(imagen)
    x = silencio
    for tramo, ancho in zip(patron, tramos):
        if tramo.isupper():
            dibujo.rectangle((x, 0, x + ancho - 1, imagen.height - 1), fill=0)
        x += ancho
    with BytesIO() as salida:
        imagen.save(salida, format="PNG")
        return base64.b64encode(salida.getvalue()).decode("ascii")
