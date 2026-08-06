# -*- coding: utf-8 -*-
"""
Tablas de dignidades esenciales, débilidades, recepción, aspectos y
descripciones planetarias para el método Ben Ezra (transmitido por
Pepa Sanchís), según el material entregado por Celina.

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
    "Mercurio": {"variable"},  # frío/seco según tradición, se trata aparte
    "Venus": {"frío", "húmedo"},
    "Marte": {"caliente", "seco"},
    "Júpiter": {"caliente", "húmedo"},
    "Saturno": {"frío", "seco"},
}

# ---------------------------------------------------------------------------
# TÉRMINOS EGIPCIOS (límites clásicos, grados dentro del signo 0-30)
# Cada signo: lista de (planeta, grado_inicio, grado_fin)
# ---------------------------------------------------------------------------
TERMS = {
    "Aries":       [("Júpiter", 0, 6), ("Venus", 6, 12), ("Mercurio", 12, 20), ("Marte", 20, 25), ("Saturno", 25, 30)],
    "Tauro":       [("Venus", 0, 8), ("Mercurio", 8, 15), ("Júpiter", 15, 22), ("Saturno", 22, 26), ("Marte", 26, 30)],
    "Géminis":     [("Mercurio", 0, 7), ("Júpiter", 7, 14), ("Venus", 14, 21), ("Marte", 21, 25), ("Saturno", 25, 30)],
    "Cáncer":      [("Marte", 0, 6), ("Venus", 6, 13), ("Mercurio", 13, 20), ("Júpiter", 20, 27), ("Saturno", 27, 30)],
    "Leo":         [("Júpiter", 0, 6), ("Venus", 6, 11), ("Saturno", 11, 18), ("Mercurio", 18, 24), ("Marte", 24, 30)],
    "Virgo":       [("Mercurio", 0, 7), ("Venus", 7, 13), ("Júpiter", 13, 18), ("Marte", 18, 24), ("Saturno", 24, 30)],
    "Libra":       [("Saturno", 0, 6), ("Mercurio", 6, 11), ("Júpiter", 11, 19), ("Venus", 19, 24), ("Marte", 24, 30)],
    "Escorpio":    [("Marte", 0, 6), ("Venus", 6, 14), ("Mercurio", 14, 21), ("Júpiter", 21, 27), ("Saturno", 27, 30)],
    "Sagitario":   [("Júpiter", 0, 8), ("Venus", 8, 14), ("Mercurio", 14, 19), ("Saturno", 19, 25), ("Marte", 25, 30)],
    "Capricornio": [("Mercurio", 0, 7), ("Júpiter", 7, 14), ("Venus", 14, 22), ("Saturno", 22, 26), ("Marte", 26, 30)],
    "Acuario":     [("Mercurio", 0, 7), ("Venus", 7, 13), ("Júpiter", 13, 20), ("Marte", 20, 25), ("Saturno", 25, 30)],
    "Piscis":      [("Venus", 0, 12), ("Júpiter", 12, 16), ("Mercurio", 16, 19), ("Marte", 19, 28), ("Saturno", 28, 30)],
}

# ---------------------------------------------------------------------------
# DECANATOS (Caldeos): 3 decanatos de 10° por signo, orden de Marte->Sol->Venus...
# regente del primer decanato = regente del propio signo; luego sigue orden caldeo.
# ---------------------------------------------------------------------------
CHALDEAN_ORDER = ["Saturno", "Júpiter", "Marte", "Sol", "Venus", "Mercurio", "Luna"]


def decan_ruler(sign, degree_in_sign):
    """Regente de decanato: el primer decanato lo rige el regente del signo,
    y a partir de ahí se sigue el orden caldeo."""
    start_planet = DOMICILE[sign][0]
    start_idx = CHALDEAN_ORDER.index(start_planet)
    decan_n = int(degree_in_sign // 10)  # 0,1,2
    return CHALDEAN_ORDER[(start_idx + decan_n) % 7]


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
# Orbes tradicionales aproximados por planeta (suma de orbes de los dos cuerpos / 2, simplificado a un orbe fijo razonable)
DEFAULT_ORB = 8.0
MOON_ORB = 10.0

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
