# -*- coding: utf-8 -*-
"""Arma el informe técnico completo de una carta horaria."""

from tables import PLANETS, HOUR_RULER_MEANING, DESCRIPTIONS
from astro import (
    compute_chart, almuten_of, essential_dignity_label, find_aspects,
    moon_last_next_aspect, moon_void_of_course, via_combusta,
)
from validity import (
    almuten_hour_agreement, house_intercepted, asc_degree_notes,
    saturn_in_vii, translation_of_light, collection_of_light,
)
from signif import significadores

HOUSE_LABELS = {
    1: "I - El consultante mismo",
    2: "II - Dinero, bienes muebles, recursos",
    3: "III - Hermanos, vecinos, comunicaciones, viajes cortos",
    4: "IV - Hogar, familia de origen, el padre, bienes raíces, el final del asunto",
    5: "V - Hijos, creatividad, romances, especulación, embarazo",
    6: "VI - Salud, trabajo (empleados), animales pequeños, tíos/tías",
    7: "VII - Pareja, socios, el otro, contrincantes, vendedor/comprador",
    8: "VIII - Dinero de otros, herencias, muerte, cirugías, lo oculto",
    9: "IX - Viajes largos, estudios superiores, religión, la ley, el astrólogo",
    10: "X - Profesión, estatus, la madre, autoridad",
    11: "XI - Amigos, deseos, proyectos, aliados",
    12: "XII - Lo oculto, enemigos ocultos, pruebas, encierro, animales grandes",
}


def build_report(payload):
    chart = compute_chart(
        year=payload["year"], month=payload["month"], day=payload["day"],
        hour=payload["hour"], minute=payload["minute"],
        utc_offset=payload["utc_offset"], lat=payload["lat"], lon_geo=payload["lon"],
    )

    is_day = chart["is_day"]

    # --- Planetas: signo, casa, velocidad, dignidad esencial propia ---
    planets_report = {}
    for p in PLANETS:
        d = chart["planets"][p]
        planets_report[p] = {
            "signo": d["sign"], "grado": round(d["deg_in_sign"], 2),
            "casa": d["house"], "retrógrado": d["retrograde"],
            "dignidad_esencial": essential_dignity_label(d["lon"], p, is_day),
            "descripcion": DESCRIPTIONS.get(p, {}),
        }

    # --- Almutenes de cada cúspide ---
    cusps_report = {}
    for i in range(12):
        cusp_lon = chart["house_cusps"][i]
        ranked, scores = almuten_of(cusp_lon, is_day)
        top = ranked[0][1]
        almutenes = [{"planeta": p, "puntos": s} for p, s in ranked if s == top and s > 0]
        segundo = [{"planeta": p, "puntos": s} for p, s in ranked if s < top and s > 0][:3]
        interc, interc_signs, interc_rulers = house_intercepted(chart, i + 1)
        cusps_report[i + 1] = {
            "etiqueta": HOUSE_LABELS[i + 1],
            "signo_cuspide": planets_and_sign_of_cusp(chart, i),
            "almuten_principal": almutenes,
            "otras_dignidades": segundo,
            "planetas_en_casa": [p for p in PLANETS if chart["planets"][p]["house"] == i + 1],
            "signo_interceptado": {"hay": interc, "signos": interc_signs, "regentes": interc_rulers},
        }

    # --- Aspectos y recepciones ---
    aspects = find_aspects(chart)

    # --- Luna: último y próximo aspecto, vacía de curso, vía combusta ---
    last_asp, next_asp = moon_last_next_aspect(chart)
    voc, days_to_change = moon_void_of_course(chart)

    # --- Significadores (consultante y, si se indicó, casa de la pregunta) ---
    sig = significadores(chart, casa_pregunta=payload.get("casa_pregunta"))

    # --- Validez del tema ---
    validity = {
        "almuten_hora": almuten_hour_agreement(chart),
        "ascendente": asc_degree_notes(chart),
        "luna_vacia_de_curso": voc,
        "dias_a_cambio_signo_luna": round(days_to_change, 2) if days_to_change is not None else None,
        "via_combusta": via_combusta(chart),
        "saturno_en_vii": saturn_in_vii(chart),
    }

    return {
        "chart_meta": {
            "fecha_local": chart["local_datetime"], "utc_offset": chart["utc_offset"],
            "lat": chart["lat"], "lon": chart["lon"],
            "asc": f'{chart["asc_sign"]} {chart["asc_deg"]:.2f}°',
            "mc": f'{chart["mc_sign"]} {chart["mc_deg"]:.2f}°',
            "carta_diurna": is_day,
            "regente_hora": chart["hour_ruler"],
            "regente_hora_significado": HOUR_RULER_MEANING.get(chart["hour_ruler"], ""),
            "fuente_efemerides": chart["ephemeris_source"],
        },
        "planetas": planets_report,
        "casas": cusps_report,
        "significadores": sig,
        "aspectos": aspects,
        "luna": {
            "ultimo_aspecto": last_asp, "proximo_aspecto": next_asp,
            "vacia_de_curso": voc, "via_combusta": via_combusta(chart),
        },
        "validez_tema": validity,
        "_chart_raw": chart,  # se usa internamente para traslación/colección bajo demanda
    }


def planets_and_sign_of_cusp(chart, house_idx0):
    from astro import sign_of
    sign, deg = sign_of(chart["house_cusps"][house_idx0])
    return f"{sign} {deg:.2f}°"


def perfection_helpers(report, sig_a, sig_b):
    """Bajo demanda: traslación y colección de luz entre dos significadores dados."""
    chart = report["_chart_raw"]
    return {
        "traslacion": translation_of_light(chart, sig_a, sig_b),
        "coleccion": collection_of_light(chart, sig_a, sig_b),
    }
