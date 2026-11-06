# -*- coding: utf-8 -*-
"""Significadores: aplica la jerarquía de la Lección 4 (regente presente/aspectando
la cúspide > planeta partil sobre la cúspide > almuten) para dar UN significador
recomendado por casa, mostrando siempre el razonamiento y los candidatos alternativos."""

from tables import DOMICILE, PLANETS, ASPECTS, aspect_orb
from astro import almuten_of, angular_sep, sign_of


def _ruler_of(sign):
    return DOMICILE[sign][0]


def _aspects_cusp(chart, planet, cusp_lon):
    lon = chart["planets"][planet]["lon"]
    sep = angular_sep(lon, cusp_lon)
    for asp_name, asp_deg in ASPECTS.items():
        if abs(sep - asp_deg) <= aspect_orb(planet):
            return asp_name
    return None


def significador_de_casa(chart, house_n):
    cusp_lon = chart["house_cusps"][house_n - 1]
    sign, deg = sign_of(cusp_lon)
    ruler = _ruler_of(sign)
    ranked, scores = almuten_of(cusp_lon, chart["is_day"])
    top_score = ranked[0][1]
    almutenes = [p for p, s in ranked if s == top_score and s > 0]

    planeta_en_casa = [p for p in PLANETS if chart["planets"][p]["house"] == house_n]
    ruler_en_casa_domiciliado = (
        ruler in planeta_en_casa and DOMICILE[chart["planets"][ruler]["sign"]][0] == ruler
    )
    ruler_aspecta_cuspide = _aspects_cusp(chart, ruler, cusp_lon)

    partil = None
    for p in planeta_en_casa:
        orb = angular_sep(chart["planets"][p]["lon"], cusp_lon)
        if orb <= 1.5:
            partil = p
            break

    razon = ""
    if ruler_en_casa_domiciliado:
        elegido = ruler
        razon = f"{ruler} rige la cúspide y está presente y domiciliado en la casa (doble influencia: regencia + presencia)."
    elif ruler_aspecta_cuspide:
        elegido = ruler
        razon = f"{ruler} rige la cúspide y la aspecta por {ruler_aspecta_cuspide} (doble influencia: regencia + aspecto)."
    elif partil:
        elegido = partil
        razon = f"{partil} está presente en la casa y prácticamente partil sobre la cúspide."
    else:
        elegido = almutenes[0]
        if len(almutenes) > 1:
            razon = f"Hay varios almutenes con igual puntaje ({', '.join(almutenes)}); se prioriza {elegido} salvo mejor criterio (posición sobre el horizonte, aspecto de la Luna, regencia de la Hora)."
        else:
            razon = f"{elegido} es el almuten de la cúspide (mayor puntaje de dignidad: {top_score})."

    return {
        "casa": house_n,
        "signo_cuspide": f"{sign} {deg:.2f}°",
        "regente_cuspide": ruler,
        "almutenes_cuspide": almutenes,
        "planetas_en_casa": planeta_en_casa,
        "significador_recomendado": elegido,
        "razonamiento": razon,
        "nota": "Recomendación automática orientativa según la jerarquía de la Lección 4; revisar siempre los candidatos si el caso es límite.",
    }


def significadores(chart, casa_pregunta=None):
    result = {
        "consultante": significador_de_casa(chart, 1),
        "luna_co_significadora": "La Luna siempre co-significa al consultante: no lo describe, indica qué le va a pasar (ver último/próximo aspecto).",
    }
    if casa_pregunta:
        result["pregunta"] = significador_de_casa(chart, casa_pregunta)
    return result
