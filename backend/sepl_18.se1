# -*- coding: utf-8 -*-
"""Chequeos de validez del tema (Lección 2) y utilidades de traslación/colección de luz."""

from tables import SIGN_ELEMENT, TRIPLICITY, PLANET_QUALITY, DOMICILE, SIGNS
from astro import (
    almuten_of, angular_sep, ASPECTS, DEFAULT_ORB, MOON_ORB, _is_applying,
)


def _triplicity_group(planet):
    groups = []
    for elem, trio in TRIPLICITY.items():
        if planet in trio:
            groups.append(elem)
    return groups


def almuten_hour_agreement(chart):
    """Compara el/los almuten(es) de la cúspide I con el regente de la Hora,
    según las 3 condiciones de la Lección 2."""
    ranked, scores = almuten_of(chart["house_cusps"][0], chart["is_day"])
    top_score = ranked[0][1]
    almutenes_I = [p for p, s in ranked if s == top_score and s > 0]
    hour_ruler = chart["hour_ruler"]

    notes = []
    valid = False
    for alm in almutenes_I:
        if alm == hour_ruler:
            notes.append(f"{alm} es a la vez almuten de I y regente de la Hora (misma pieza: carta muy fiable).")
            valid = True
            continue
        trip_alm = set(_triplicity_group(alm))
        trip_hour = set(_triplicity_group(hour_ruler)) if hour_ruler else set()
        if trip_alm & trip_hour:
            notes.append(f"{alm} (almuten I) y {hour_ruler} (regente Hora) comparten triplicidad ({', '.join(trip_alm & trip_hour)}).")
            valid = True
        qual_alm = PLANET_QUALITY.get(alm, set())
        qual_hour = PLANET_QUALITY.get(hour_ruler, set()) if hour_ruler else set()
        shared_qual = qual_alm & qual_hour
        if shared_qual:
            notes.append(f"{alm} y {hour_ruler} comparten cualidad elemental ({', '.join(shared_qual)}).")
            valid = True
    if not notes:
        notes.append(f"Los almutenes de I ({', '.join(almutenes_I)}) y el regente de la Hora ({hour_ruler}) no comparten planeta, triplicidad ni cualidad elemental.")
    return {"almutenes_I": almutenes_I, "regente_hora": hour_ruler, "coincide": valid, "notas": notes}


def house_intercepted(chart, house_n):
    """Indica si hay un signo completo interceptado dentro de la casa house_n
    (dos cúspides consecutivas 'saltan' un signo), y devuelve su regente."""
    cusps = chart["house_cusps"]
    i = house_n - 1
    c0 = cusps[i]
    c1 = cusps[(i + 1) % 12]
    from astro import sign_of
    sign0 = sign_of(c0)[0]
    sign1 = sign_of(c1)[0]
    idx0 = SIGNS.index(sign0)
    idx1 = SIGNS.index(sign1)
    span = (idx1 - idx0) % 12
    if span >= 2:
        # hay al menos un signo completo salteado
        intercepted_signs = [SIGNS[(idx0 + k) % 12] for k in range(1, span)]
        rulers = {s: DOMICILE[s][0] for s in intercepted_signs}
        return True, intercepted_signs, rulers
    return False, [], {}


def asc_degree_notes(chart):
    deg = chart["asc_deg"]
    notes = []
    if deg < 3:
        notes.append(f"Ascendente muy a principio de signo ({deg:.1f}°): aún no ha llegado el momento para lo que se pregunta; interpretar con cautela.")
    elif deg > 27:
        notes.append(f"Ascendente muy a final de signo ({deg:.1f}°): situación muy avanzada, que el consultante ya da por terminada en su fuero interno.")
    return notes


def saturn_in_vii(chart):
    return chart["planets"]["Saturno"]["house"] == 7


def translation_of_light(chart, sig_a, sig_b):
    """Busca un tercer planeta que se separe (últimamente) de sig_a y aplique
    (próximamente) a sig_b (o viceversa): traslación de luz."""
    planets = chart["planets"]
    candidates = []
    for name, data in planets.items():
        if name in (sig_a, sig_b):
            continue
        sep_a = angular_sep(data["lon"], planets[sig_a]["lon"])
        sep_b = angular_sep(data["lon"], planets[sig_b]["lon"])
        for asp_name, asp_deg in ASPECTS.items():
            orb = MOON_ORB if name == "Luna" or sig_a == "Luna" or sig_b == "Luna" else DEFAULT_ORB
            separating_from_a = abs(sep_a - asp_deg) <= orb and not _is_applying(
                data["lon"], data["speed"], planets[sig_a]["lon"], planets[sig_a]["speed"], asp_deg)
            applying_to_b = abs(sep_b - asp_deg) <= orb and _is_applying(
                data["lon"], data["speed"], planets[sig_b]["lon"], planets[sig_b]["speed"], asp_deg)
            if separating_from_a and applying_to_b:
                candidates.append({"planeta": name, "separa_de": sig_a, "aplica_a": sig_b, "aspecto": asp_name})
    return candidates


def collection_of_light(chart, sig_a, sig_b):
    """Busca un tercer planeta al que tanto sig_a como sig_b apliquen
    (colección de luz), preferentemente con dignidad sobre él."""
    planets = chart["planets"]
    candidates = []
    for name, data in planets.items():
        if name in (sig_a, sig_b):
            continue
        for asp_name, asp_deg in ASPECTS.items():
            orb = DEFAULT_ORB
            sep_a = angular_sep(planets[sig_a]["lon"], data["lon"])
            sep_b = angular_sep(planets[sig_b]["lon"], data["lon"])
            a_applies = abs(sep_a - asp_deg) <= orb and _is_applying(
                planets[sig_a]["lon"], planets[sig_a]["speed"], data["lon"], data["speed"], asp_deg)
            b_applies = abs(sep_b - asp_deg) <= orb and _is_applying(
                planets[sig_b]["lon"], planets[sig_b]["speed"], data["lon"], data["speed"], asp_deg)
            if a_applies and b_applies:
                candidates.append({"planeta_colector": name, "de": [sig_a, sig_b], "aspectos": asp_name})
    return candidates
