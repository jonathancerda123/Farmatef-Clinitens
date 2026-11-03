"""Definición declarativa de las 13 secciones de la ficha."""

HENDERSON = [
    "Respirar normalmente",
    "Comer y beber adecuadamente",
    "Eliminar por todas las vías corporales",
    "Moverse y mantener posturas adecuadas",
    "Dormir y descansar",
    "Escoger ropa adecuada / vestirse",
    "Mantener la temperatura corporal",
    "Mantener la higiene corporal",
    "Evitar peligros del entorno",
    "Comunicarse con los demás",
    "Vivir según valores y creencias",
    "Ocuparse / sentirse realizado",
    "Participar en actividades recreativas",
    "Aprender, descubrir o satisfacer la curiosidad",
]

MASLOW = {
    "Fisiológicas": [
        "Respiración",
        "Alimentación / hidratación",
        "Eliminación",
        "Descanso / sueño",
        "Termorregulación",
        "Higiene",
        "Movilidad",
        "Sexualidad",
    ],
    "Seguridad": [
        "Seguridad física (caídas, lesiones)",
        "Seguridad emocional",
        "Protección frente al entorno",
        "Manejo del dolor",
    ],
    "Afiliación / Sociales": [
        "Pertenencia familiar",
        "Relaciones sociales",
        "Apoyo y red social",
        "Comunicación",
    ],
    "Reconocimiento / Estima": [
        "Autoestima",
        "Reconocimiento",
        "Autonomía / independencia",
    ],
    "Autorrealización": [
        "Realización personal",
        "Espiritualidad / valores",
        "Aprendizaje / desarrollo",
    ],
}

GCS = {
    "Apertura ocular": [
        ("Espontánea", 4),
        ("Al estímulo verbal", 3),
        ("Al dolor", 2),
        ("Sin respuesta", 1),
    ],
    "Respuesta verbal": [
        ("Orientada", 5),
        ("Confusa", 4),
        ("Palabras inapropiadas", 3),
        ("Sonidos incomprensibles", 2),
        ("Sin respuesta", 1),
    ],
    "Respuesta motora": [
        ("Obedece órdenes", 6),
        ("Localiza el dolor", 5),
        ("Retira al dolor", 4),
        ("Flexión anormal", 3),
        ("Extensión anormal", 2),
        ("Sin respuesta", 1),
    ],
}

DOWNTON = {
    "Caídas previas": [("No", 0), ("Sí", 1)],
    "Medicamentos": [("Ninguno", 0), ("Uno", 1), ("Dos o más", 2)],
    "Déficits sensoriales": [("Ninguno", 0), ("Uno", 1), ("Dos o más", 2)],
    "Estado mental": [("Orientado", 0), ("Confuso / desorientado", 1)],
    "Deambulación": [
        ("Normal", 0),
        ("Segura con ayuda", 1),
        ("Insegura con o sin ayuda", 1),
        ("Imposible", 1),
    ],
}

BRADEN = {
    "Percepción sensorial": [
        ("Completamente limitada", 1),
        ("Muy limitada", 2),
        ("Levemente limitada", 3),
        ("Sin alteración", 4),
    ],
    "Humedad": [
        ("Constantemente húmeda", 1),
        ("A menudo húmeda", 2),
        ("Ocasionalmente húmeda", 3),
        ("Raramente húmeda", 4),
    ],
    "Actividad": [
        ("Encamado/a", 1),
        ("En silla", 2),
        ("Deambula ocasionalmente", 3),
        ("Deambula frecuentemente", 4),
    ],
    "Movilidad": [
        ("Completamente inmóvil", 1),
        ("Muy limitada", 2),
        ("Levemente limitada", 3),
        ("Sin limitaciones", 4),
    ],
    "Nutrición": [
        ("Muy pobre", 1),
        ("Probablemente inadecuada", 2),
        ("Adecuada", 3),
        ("Excelente", 4),
    ],
    "Fricción y cizallamiento": [
        ("Problema", 1),
        ("Problema potencial", 2),
        ("Sin problema aparente", 3),
    ],
}

SECCIONES = [
    ("identidad", "1. Identificación del Paciente", "Identificación del Paciente"),
    ("farmacos", "2. Tratamiento Farmacológico", "Tratamiento Farmacológico"),
    ("signos", "3. Signos Vitales", "Signos Vitales"),
    (
        "recontroles",
        "4. Recontroles de Signos Vitales",
        "Recontroles de Signos Vitales",
    ),
    ("necesidades", "5. Necesidades (V. Henderson/Maslow)", "Necesidades alteradas"),
    ("plan", "6. Plan de Cuidados de Enfermería", "Plan de Cuidados de Enfermería"),
    ("registro", "7. Plan de Cuidados (Registro)", "Plan de Cuidados (Registro)"),
    ("riesgos", "8. Riesgos y Escalas Clínicas", "Riesgos y Escalas Clínicas"),
    ("balance", "9. Balance Hídrico", "Balance Hídrico"),
    ("examenes", "10. Exámenes Solicitados", "Exámenes Solicitados"),
    ("dispositivos", "11. Dispositivos Invasivos", "Dispositivos Invasivos"),
    ("indicaciones", "12. Otras Indicaciones", "Otras Indicaciones"),
    ("evolucion", "13. Evolución y Entrega de Turno", "Evolución y Entrega de Turno"),
]
