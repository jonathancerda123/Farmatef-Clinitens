"""Validación de uploads sin confiar en accept, MIME ni extensión por sí solos."""
from pathlib import Path
from django.core.exceptions import ValidationError
from PIL import Image, UnidentifiedImageError


def validar_archivo(archivo):
    if not archivo:
        return archivo
    extension = Path(archivo.name).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp", ".pdf", ".mp4", ".mov", ".webm"}:
        raise ValidationError("Formato de archivo no permitido.")
    if archivo.size > 50 * 1024 * 1024:
        raise ValidationError("Cada archivo puede pesar como máximo 50 MB.")
    if archivo.size == 0:
        raise ValidationError("El archivo está vacío.")
    archivo.seek(0)
    head = archivo.read(32)
    archivo.seek(0)
    try:
        if extension in {".jpg", ".jpeg", ".png", ".webp"}:
            with Image.open(archivo) as imagen:
                expected = {".jpg": "JPEG", ".jpeg": "JPEG", ".png": "PNG", ".webp": "WEBP"}
                if imagen.format != expected[extension]:
                    raise ValidationError("La imagen no corresponde a su extensión.")
                imagen.verify()
        elif extension == ".pdf" and not head.startswith(b"%PDF-"):
            raise ValidationError("El contenido no corresponde a un PDF.")
        elif extension in {".mp4", ".mov"} and head[4:8] != b"ftyp":
            raise ValidationError("El contenido no corresponde a un video MP4/MOV.")
        elif extension == ".webm" and not head.startswith(b"\x1aE\xdf\xa3"):
            raise ValidationError("El contenido no corresponde a un video WebM.")
    except (OSError, UnidentifiedImageError, Image.DecompressionBombError):
        raise ValidationError("No fue posible validar la imagen.")
    finally:
        archivo.seek(0)
    return archivo


def validar_archivo_nuevo(archivo):
    # Los archivos existentes no se reabren al editar otro campo del modelo.
    if archivo and not getattr(archivo, "_committed", False):
        validar_archivo(archivo)
