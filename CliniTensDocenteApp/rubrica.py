RUBRICA = [
    (
        "3.1.1.I.1",
        "Revisión del caso clínico, diagnóstico e indicaciones médicas y selección de datos relevantes",
        5,
    ),
    ("3.1.1.I.2", "Descripción del diagnóstico médico", 5),
    ("3.1.1.I.3", "Acción farmacológica y reacción adversa más importante", 5),
    ("3.1.1.I.4", "Cuidados relevantes asociados a medicamentos", 5),
    ("3.1.2.I.5", "Interpretación de signos vitales y estado nutricional", 5),
    ("3.1.2.I.6", "Prioriza y justifica tres necesidades alteradas", 10),
    ("3.1.2.I.7", "Plan de cuidados específico por necesidad priorizada", 15),
    ("3.1.3.I.8", 'Completa "Registro de Atención de Enfermería"', 10),
    ("3.1.3.I.9", 'Completa "Plan de Atención de Enfermería Básico"', 10),
    ("3.1.3.I.10", 'Completa "Riesgos Asociados a la Hospitalización"', 5),
    ("3.1.3.I.11", "Balance Hídrico (ingresos y egresos)", 5),
    ("3.1.4.I.12", 'Registra actividades del "Plan de Cuidados"', 5),
    ("3.1.4.I.13", "Tres cuidados para cada dispositivo invasivo", 5),
    ("3.1.4.I.14", 'Registra "Otras Indicaciones"', 5),
    ("3.1.4.I.15", "Evolución del usuario y entrega de turno", 5),
]


def niveles_por_puntaje(maximo):
    if maximo == 15:
        return [
            ("Experto", 15),
            ("Competente", 12),
            ("Elemental", 9),
            ("Inicial", 3),
            ("Ausente", 0),
        ]

    if maximo == 10:
        return [
            ("Experto", 10),
            ("Competente", 8),
            ("Elemental", 6),
            ("Inicial", 2),
            ("Ausente", 0),
        ]

    return [
        ("Experto", 5),
        ("Competente", 4),
        ("Elemental", 3),
        ("Inicial", 1),
        ("Ausente", 0),
    ]
