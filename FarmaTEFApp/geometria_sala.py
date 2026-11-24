"""Reglas de la sala compartidas por modelos/servicios, sin acceso a datos."""
from django.core.exceptions import ValidationError

TIPOS_MUEBLE = (
    ("sliding", "Estante deslizante"), ("drawers", "Cajonera"),
    ("table", "Mesa simple"), ("board", "Pizarra"),
    ("counter", "Mesón de trabajo"), ("studentTable", "Mesa con seis sillas"),
    ("entrance", "Zona de entrada"),
)


def huella(mueble):
    ancho = mueble.ancho_cm
    fondo = mueble.fondo_cm + (90 if mueble.tipo == "studentTable" else 0)
    return (fondo, ancho) if mueble.orientacion in (90, 270) else (ancho, fondo)


def compartimentos(mueble):
    if mueble.tipo == "sliding":
        return [f"{col}-{fila}" for col in ("A", "B", "F1", "F2", "F3")
                for fila in range(1, mueble.filas + 1)]
    if mueble.tipo == "drawers":
        return [f"C{i}" for i in range(1, mueble.filas * mueble.columnas + 1)]
    return []


def nombre_compartimento(clave):
    if clave.startswith("C"):
        return f"Cajón {clave[1:]}"
    columna, fila = clave.split("-")
    prefijo = f"Fondo · columna {columna[1:]}" if columna.startswith("F") else f"Móvil {columna}"
    return f"{prefijo} · fila {fila}"


def validar_mueble(mueble, sala):
    if mueble.tipo not in dict(TIPOS_MUEBLE):
        raise ValidationError("Selecciona un tipo de mueble válido.")
    min_ancho = 150 if mueble.tipo == "studentTable" else 180 if mueble.tipo == "counter" else 60
    min_fondo, max_fondo = (5, 15) if mueble.tipo == "board" else (35, 120)
    campos = (mueble.ancho_cm, mueble.alto_cm, mueble.fondo_cm, mueble.x_cm,
              mueble.y_cm, mueble.orientacion, mueble.filas, mueble.columnas)
    if any(type(n) is not int for n in campos):
        raise ValidationError("Las medidas y posiciones deben ser números enteros en centímetros.")
    if not (min_ancho <= mueble.ancho_cm <= 720 and 50 <= mueble.alto_cm <= 220
            and min_fondo <= mueble.fondo_cm <= max_fondo
            and mueble.orientacion in (0, 90, 180, 270)
            and 1 <= mueble.filas <= 12 and 1 <= mueble.columnas <= 8):
        raise ValidationError("Revisa las medidas, filas, columnas y orientación del mueble.")
    if mueble.tipo == "sliding" and mueble.columnas != 3:
        raise ValidationError("El estante deslizante conserva tres columnas de fondo y dos móviles.")
    if (mueble.tipo == "sliding" and mueble.alto_cm < 20 + 6 * mueble.filas) or (mueble.tipo == "drawers" and (mueble.alto_cm < 16 + 6 * mueble.filas or mueble.ancho_cm < 12 * mueble.columnas)):
        raise ValidationError("Las medidas no dejan espacio suficiente para esos compartimentos.")
    if not compartimentos(mueble) and (mueble.filas != 1 or mueble.columnas != 1):
        raise ValidationError("Este tipo de mueble no tiene compartimentos de almacenamiento.")
    ancho, fondo = huella(mueble)
    if min(mueble.x_cm, mueble.y_cm) < 0 or mueble.x_cm + ancho > sala.ancho_cm or mueble.y_cm + fondo > sala.largo_cm:
        raise ValidationError(f"{mueble.nombre}: el elemento y sus sillas, si corresponde, deben quedar dentro de la sala.")
