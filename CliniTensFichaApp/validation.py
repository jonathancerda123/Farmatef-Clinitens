"""Contrato explícito del JSON de las 13 secciones del editor."""
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError
from .ficha_config import SECCIONES, HENDERSON, MASLOW, GCS, DOWNTON, BRADEN

FIELDS = {
    "identidad": "nombre nombre_social rut edad sexo diagnostico patologia anamnesis_remota anamnesis_proxima".split(),
    "signos": "fc fr pas pad temperatura saturacion peso talla hgt eva interpretacion".split(),
    "necesidades": "henderson maslow justificacion rol_asistencial rol_administrativo rol_educativo".split(),
    "plan": [f"necesidad_{i}" for i in range(1, 4)] + [f"n{i}_c{j}" for i in range(1, 4) for j in range(1, 4)],
    "riesgos": [f"{name}_{i}" for name, n in [("glasgow", 3), ("downton", 5), ("braden", 6)] for i in range(1, n + 1)] + ["aislamiento", "epp", "habitacion"],
    "balance": "egresos_deposiciones egresos_diuresis egresos_drenajes egresos_vomitos horas ingresos_agua ingresos_alimentacion ingresos_medicamentos ingresos_otros ingresos_sueros peso temperatura".split(),
    "indicaciones": [f"{name}_{i}" for name in ["curaciones", "examenes", "monitorizacion", "oxigenoterapia"] for i in range(1, 4)],
    "evolucion": "datos_paciente novedades actividades_pendientes eventos_adversos".split(),
}
ROWS = {
    "farmacos": "medicamento dosis horario via accion reaccion cuidado".split(),
    "recontroles": "fecha hora pa fc fr temp sat hgt".split(),
    "registro": "hora procedimiento materiales alteraciones manejo firma".split(),
    "examenes": "categoria examen observaciones".split(),
    "dispositivos": "tipo caracteristicas dias cuidado1 cuidado2 cuidado3".split(),
}
ARRAYS = {("necesidades", "henderson"), ("necesidades", "maslow"),
          ("riesgos", "aislamiento"), ("riesgos", "epp")}
NUMERIC = {("signos", x) for x in FIELDS["signos"] if x != "interpretacion"} | {
    ("identidad", "edad"), *[("balance", x) for x in FIELDS["balance"]]}
CHOICES = {
    ("identidad", "sexo"): {"Mujer", "Hombre", "Intersexual"},
    ("necesidades", "henderson"): set(HENDERSON),
    ("necesidades", "maslow"): {x for group in MASLOW.values() for x in group},
    ("riesgos", "aislamiento"): {"Precauciones estándar", "Contacto", "Gotas", "Aéreo"},
    ("riesgos", "epp"): {"Mascarilla quirúrgica", "Mascarilla N95", "Pechera", "Guantes", "Antiparras / escudo facial", "Cofia", "Botas"},
    ("riesgos", "habitacion"): {"Individual", "Compartida", "Aislamiento", "UCI / UTI"},
}
for name, groups in [("glasgow", GCS), ("downton", DOWNTON), ("braden", BRADEN)]:
    for i, options in enumerate(groups.values(), 1):
        CHOICES[("riesgos", f"{name}_{i}")] = {label for label, _ in options}


def contenido(valor):
    if isinstance(valor, dict):
        return any(contenido(v) for k, v in valor.items() if k != "no_aplica")
    if isinstance(valor, list):
        return any(contenido(v) for v in valor)
    return valor is not None and valor is not False and str(valor).strip() != ""


def texto(value):
    if not isinstance(value, str) or len(value) > 5000 or "\x00" in value:
        raise ValidationError("Los campos deben ser texto de hasta 5000 caracteres.")


def validar_datos(datos):
    sections = {s[0] for s in SECCIONES}
    if not isinstance(datos, dict) or not set(datos) <= sections:
        raise ValidationError("La ficha contiene secciones desconocidas.")
    for section, fields in datos.items():
        allowed = set(FIELDS.get(section, ["filas"])) | {"no_aplica"}
        if not isinstance(fields, dict) or not set(fields) <= allowed:
            raise ValidationError("La ficha contiene campos desconocidos.")
        for field, value in fields.items():
            if field == "no_aplica":
                if type(value) is not bool or (section == "identidad" and value):
                    raise ValidationError("Identificación es obligatoria; No aplica debe ser booleano.")
            elif field == "filas":
                if not isinstance(value, list) or len(value) > 200:
                    raise ValidationError("Se admiten hasta 200 filas por tabla.")
                for row in value:
                    if not isinstance(row, dict) or not set(row) <= set(ROWS[section]):
                        raise ValidationError("La tabla contiene columnas desconocidas.")
                    for cell in row.values():
                        texto(cell)
            elif (section, field) in ARRAYS:
                if not isinstance(value, list) or len(value) > 50:
                    raise ValidationError("Selección múltiple no válida.")
                for item in value:
                    texto(item)
                    if item not in CHOICES[(section, field)]:
                        raise ValidationError("La selección no pertenece al catálogo permitido.")
            else:
                texto(value)
                if value and (section, field) in CHOICES and value not in CHOICES[(section, field)]:
                    raise ValidationError("La opción no pertenece al catálogo permitido.")
                if (section, field) in NUMERIC and value.strip():
                    try:
                        number = Decimal(value)
                    except InvalidOperation:
                        raise ValidationError("El campo numérico no es válido.")
                    if not number.is_finite():
                        raise ValidationError("El campo numérico debe ser finito.")
                    if section == "identidad" and (number != number.to_integral_value() or not 0 <= number <= 120):
                        raise ValidationError("La edad debe ser un entero entre 0 y 120.")
    return datos


def seccion_completa(key, section):
    if not isinstance(section, dict):
        return False
    if key == "identidad":
        return all(contenido(section.get(k)) for k in ["nombre", "rut", "edad", "sexo"])
    if section.get("no_aplica") is True:
        return True
    if key in ROWS:
        rows = section.get("filas", [])
        return bool(rows) and all(all(contenido(row.get(field)) for field in ROWS[key]) for row in rows)
    return all(contenido(section.get(field)) for field in FIELDS[key])


def pendientes(datos):
    missing = []
    identity = datos.get("identidad", {})
    if any(not contenido(identity.get(k)) for k in ["nombre", "rut", "edad", "sexo"]):
        missing.append("Identificación: nombre, identificación, edad y sexo")
    for key, _, title in SECCIONES:
        section = datos.get(key, {})
        if key == "identidad":
            continue
        if not seccion_completa(key, section):
            missing.append(title)
    return missing
