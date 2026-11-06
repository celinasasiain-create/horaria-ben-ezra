# -*- coding: utf-8 -*-
"""
Tablas de dignidades esenciales, débilidades, recepción, aspectos y
descripciones planetarias para el método de Pepa Sanchís, según el
material entregado por Celina.

Todas las posiciones se manejan en grados 0-360 (0 = 0° Aries).
"""

SIGNS = ["Aries", "Tauro", "Géminis", "Cáncer", "Leo", "Virgo",
         "Libra", "Escorpio", "Sagitario", "Capricornio", "Acuario", "Piscis"]

PLANETS = ["Sol", "Luna", "Mercurio", "Venus", "Marte", "Júpiter", "Saturno"]

# ---------------------------------------------------------------------------
# DOMICILIOS (regente principal y, si tiene, segundo domicilio) y EXILIOS
# ---------------------------------------------------------------------------
DOMICILE = {
    "Aries": ["Marte"], "Tauro": ["Venus"], "Géminis": ["Mercurio"],
    "Cáncer": ["Luna"], "Leo": ["Sol"], "Virgo": ["Mercurio"],
    "Libra": ["Venus"], "Escorpio": ["Marte"], "Sagitario": ["Júpiter"],
    "Capricornio": ["Saturno"], "Acuario": ["Saturno"], "Piscis": ["Júpiter"],
}

EXILE = {
    "Aries": "Venus", "Tauro": "Marte", "Géminis": "Júpiter",
    "Cáncer": "Saturno", "Leo": "Saturno", "Virgo": "Júpiter",
    "Libra": "Marte", "Escorpio": "Venus", "Sagitario": "Mercurio",
    "Capricornio": "Luna", "Acuario": "Sol", "Piscis": "Mercurio",
}

EXALTATION = {
    "Aries": "Sol", "Tauro": "Luna", "Cáncer": "Júpiter",
    "Virgo": "Mercurio", "Libra": "Saturno", "Capricornio": "Marte",
    "Piscis": "Venus",
}
# Signos sin exaltación tradicional: Géminis, Leo, Escorpio, Sagitario, Acuario

FALL = {
    "Aries": "Saturno", "Cáncer": "Marte", "Virgo": "Venus",
    "Libra": "Sol", "Capricornio": "Júpiter", "Escorpio": "Luna",
    "Piscis": "Mercurio",
}

# ---------------------------------------------------------------------------
# TRIPLICIDADES (primer regente = carta diurna, segundo = nocturna, tercero = participante)
# ---------------------------------------------------------------------------
TRIPLICITY = {
    "fuego": ("Sol", "Júpiter", "Saturno"),
    "tierra": ("Venus", "Luna", "Marte"),
    "aire": ("Saturno", "Mercurio", "Júpiter"),
    "agua": ("Venus", "Marte", "Luna"),
}
SIGN_ELEMENT = {
    "Aries": "fuego", "Leo": "fuego", "Sagitario": "fuego",
    "Tauro": "tierra", "Virgo": "tierra", "Capricornio": "tierra",
    "Géminis": "aire", "Libra": "aire", "Acuario": "aire",
    "Cáncer": "agua", "Escorpio": "agua", "Piscis": "agua",
}

SIGN_MODE = {
    "Aries": "cardinal", "Cáncer": "cardinal", "Libra": "cardinal", "Capricornio": "cardinal",
    "Tauro": "fijo", "Leo": "fijo", "Escorpio": "fijo", "Acuario": "fijo",
    "Géminis": "mutable", "Virgo": "mutable", "Sagitario": "mutable", "Piscis": "mutable",
}

# Cualidades elementales (calor/frío, humedad/sequedad) por planeta - para la validez del tema
PLANET_QUALITY = {
    "Sol": {"caliente", "seco"},
    "Luna": {"frío", "húmedo"},
    "Mercurio": {"seco"},  # Pepa (Lección 2): Mercurio es neutro y sólo MUY ligeramente seco
    "Venus": {"frío", "húmedo"},
    "Marte": {"caliente", "seco"},
    "Júpiter": {"caliente", "húmedo"},
    "Saturno": {"frío", "seco"},
}

# ---------------------------------------------------------------------------
# TÉRMINOS (tablas de Jean-Marie Michiels, material de Pepa Sanchís: términos de
# Ptolomeo). Cada signo: lista de (planeta, grado_inicio, grado_fin), grados 0-30.
# Verificado grado a grado contra las tablas de Michiels.
# ---------------------------------------------------------------------------
TERMS = {
    "Aries":      [("Júpiter", 0, 6), ("Venus", 6, 12), ("Mercurio", 12, 20), ("Marte", 20, 25), ("Saturno", 25, 30)],
    "Tauro":      [("Venus", 0, 8), ("Mercurio", 8, 14), ("Júpiter", 14, 22), ("Saturno", 22, 27), ("Marte", 27, 30)],
    "Géminis":    [("Mercurio", 0, 6), ("Júpiter", 6, 12), ("Venus", 12, 17), ("Marte", 17, 24), ("Saturno", 24, 30)],
    "Cáncer":     [("Marte", 0, 7), ("Venus", 7, 13), ("Mercurio", 13, 19), ("Júpiter", 19, 26), ("Saturno", 26, 30)],
    "Leo":        [("Júpiter", 0, 6), ("Venus", 6, 11), ("Saturno", 11, 18), ("Mercurio", 18, 24), ("Marte", 24, 30)],
    "Virgo":      [("Mercurio", 0, 7), ("Venus", 7, 17), ("Júpiter", 17, 21), ("Marte", 21, 28), ("Saturno", 28, 30)],
    "Libra":      [("Saturno", 0, 6), ("Mercurio", 6, 14), ("Júpiter", 14, 21), ("Venus", 21, 28), ("Marte", 28, 30)],
    "Escorpio":   [("Marte", 0, 7), ("Venus", 7, 11), ("Mercurio", 11, 19), ("Júpiter", 19, 24), ("Saturno", 24, 30)],
    "Sagitario":  [("Júpiter", 0, 12), ("Venus", 12, 17), ("Mercurio", 17, 21), ("Saturno", 21, 26), ("Marte", 26, 30)],
    "Capricornio":[("Mercurio", 0, 7), ("Júpiter", 7, 14), ("Venus", 14, 22), ("Saturno", 22, 26), ("Marte", 26, 30)],
    "Acuario":    [("Mercurio", 0, 7), ("Venus", 7, 13), ("Júpiter", 13, 20), ("Marte", 20, 25), ("Saturno", 25, 30)],
    "Piscis":     [("Venus", 0, 12), ("Júpiter", 12, 16), ("Mercurio", 16, 19), ("Marte", 19, 28), ("Saturno", 28, 30)],
}

# ---------------------------------------------------------------------------
# DECANATOS (tablas de Michiels y ejemplo de la lección "Recepción" de Pepa:
# 12°40′ de Capricornio -> decanato de Marte). Orden caldeo desde 0° de Aries:
# el primer decanato de Aries es de Marte, luego Sol, Venus, Mercurio, Luna,
# Saturno, Júpiter, y así sucesivamente a lo largo de los 36 decanatos.
# ---------------------------------------------------------------------------
CHALDEAN_ORDER = ["Saturno", "Júpiter", "Marte", "Sol", "Venus", "Mercurio", "Luna"]
DECAN_SEQUENCE = ["Marte", "Sol", "Venus", "Mercurio", "Luna", "Saturno", "Júpiter"]


def decan_ruler(sign, degree_in_sign):
    """Regente del decanato (10° cada uno) según la secuencia caldea desde 0° Aries."""
    decan_n = SIGNS.index(sign) * 3 + int(degree_in_sign // 10)  # 0..35
    return DECAN_SEQUENCE[decan_n % 7]


# ---------------------------------------------------------------------------
# PUNTAJES (Lección "Dignidades y debilidades")
# ---------------------------------------------------------------------------
POINTS = {
    "domicilio": 5, "exaltacion": 4, "triplicidad": 3, "termino": 2, "decanato": 1,
    "exilio": -5, "caida": -4,
}

# ---------------------------------------------------------------------------
# ASPECTOS clásicos usados en horaria (Lección 10)
# ---------------------------------------------------------------------------
ASPECTS = {
    "Conjunción": 0, "Sextil": 60, "Cuadratura": 90, "Trígono": 120, "Oposición": 180,
}
# ORBES (Lección 10, según Al Biruni): los aspectos no tienen orbe, lo tienen los planetas.
# El orbe de un aspecto es la SUMA de los semidiámetros de los dos planetas, igual para
# todos los aspectos. Semidiámetros: Saturno 4°30′, Júpiter 4°30′, Marte 4°, Sol 7°30′,
# Venus 3°30′, Mercurio 3°30′, Luna 6°. (Ej.: Sol-Marte 11°30′; Mercurio-Marte 7°30′;
# Luna-Venus 9°30′.) Pepa recomienda que sea algo menor al límite, pues en el límite
# tal vez no actúe.
SEMIDIAMETERS = {
    "Saturno": 4.5, "Júpiter": 4.5, "Marte": 4.0, "Sol": 7.5,
    "Venus": 3.5, "Mercurio": 3.5, "Luna": 6.0,
}


def aspect_orb(p1, p2=None):
    """Orbe para un aspecto entre p1 y p2. Si p2 es None (aspecto de un planeta a una
    cúspide, que es un punto sin orbe propio) se usa el semidiámetro del planeta."""
    if p2 is None:
        return SEMIDIAMETERS[p1]
    return SEMIDIAMETERS[p1] + SEMIDIAMETERS[p2]


# ---------------------------------------------------------------------------
# Descripciones (Lección 6): psicología / físico / objetos-sitios / colores
# ---------------------------------------------------------------------------
DESCRIPTIONS = {
    "Saturno": {"psicologia": "Depresión, soledad, frialdad, seriedad", "fisico": "Enjuto, enfermizo, envejecido para su edad",
                "objetos": "Viejos, ajados, dañados", "colores": "Oscuros, amarillentos"},
    "Júpiter": {"psicologia": "Generosidad, honestidad, optimismo", "fisico": "Algo grueso, hermoso, de buena presencia",
                "objetos": "Grandes, caros, cómodos", "colores": "Azules"},
    "Marte": {"psicologia": "Irritación, enojo, ímpetu", "fisico": "Anguloso, recio, pelirrojo",
              "objetos": "Angulosos, cortantes, ruidosos", "colores": "Rojizos"},
    "Sol": {"psicologia": "Autonomía, liderazgo, autoestima", "fisico": "Majestuoso, fuerte, bronceado",
            "objetos": "Brillantes, muy valiosos", "colores": "Dorados, amarillos"},
    "Venus": {"psicologia": "Afectividad, humanismo, buen humor", "fisico": "Hermoso, pequeño, curvado",
              "objetos": "Hermosos, frágiles, curvados", "colores": "Alegres"},
    "Mercurio": {"psicologia": "Inteligencia, estrategia, cuestionamiento", "fisico": "Esbelto, alto, juvenil",
                 "objetos": "Múltiples, intercambiables, frecuentados", "colores": "Grises"},
    "Luna": {"psicologia": "Vaguedad, influenciabilidad, emoción", "fisico": "Pálido, pasivo, amorfo",
             "objetos": "Acuosos, amorfos, humildes", "colores": "Muy pálidos"},
}

# ---------------------------------------------------------------------------
# Regente de la Hora - significado breve (Lección 3), para dar contexto a la IA
# ---------------------------------------------------------------------------
HOUR_RULER_MEANING = {
    "Saturno": "frialdad o pesimismo; si está mal aspectado, no se espera nada de ese asunto",
    "Júpiter": "talante generoso y optimista frente al tema",
    "Marte": "hubo un enfado en algún momento que no ha desaparecido",
    "Sol": "seguridad, veracidad, sensación de dominar la situación",
    "Venus": "sentimientos afectuosos o amorosos de fondo; ganas de disfrutar",
    "Mercurio": "ganas de intercambiar, hablar, analizar; si está mal, autoengaño",
    "Luna": "asuntos emocionales, deseos vagos o no muy definidos",
}

# Secuencia caldea para horas planetarias (empezando por el regente del día)
CHALDEAN_HOUR_ORDER = ["Saturno", "Júpiter", "Marte", "Sol", "Venus", "Mercurio", "Luna"]
# Regente de cada día de la semana (0=lunes ... 6=domingo, según datetime.weekday())
WEEKDAY_RULER = {0: "Luna", 1: "Marte", 2: "Mercurio", 3: "Júpiter", 4: "Venus", 5: "Saturno", 6: "Sol"}
