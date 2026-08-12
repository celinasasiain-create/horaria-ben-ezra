# -*- coding: utf-8 -*-
"""
Motor de cálculo astrológico para Astrología Horaria - método Ben Ezra
(transmitido por Pepa Sanchís).

Usa pyswisseph con el motor Moshier incorporado (sin necesidad de
archivos de efemérides externos) - precisión de arco-segundos, más
que suficiente para horaria.
"""
import os
import swisseph as swe
import datetime as dt

EPHE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ephe")
_EPHE_FILES = {
    "sepl_18.se1": "https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/sepl_18.se1",
    "semo_18.se1": "https://raw.githubusercontent.com/aloistr/swisseph/master/ephe/semo_18.se1",
}


def _asegurar_archivos_efemerides():
    """Si los archivos .se1 no están (por ejemplo porque no se pudieron subir
    a GitHub), los descarga una sola vez desde el repositorio oficial de
    Swiss Ephemeris. Así la app funciona igual aunque el repo de GitHub sólo
    tenga el código."""
    os.makedirs(EPHE_PATH, exist_ok=True)
    for filename, url in _EPHE_FILES.items():
        destino = os.path.join(EPHE_PATH, filename)
        if os.path.exists(destino) and os.path.getsize(destino) > 100_000:
            continue
        try:
            import requests
            r = requests.get(url, timeout=30)
            r.raise_for_status()
            with open(destino, "wb") as f:
                f.write(r.content)
        except Exception as e:
            print(f"[aviso] no se pudo descargar {filename}: {e}. Se usará el motor Moshier como respaldo.")


_asegurar_archivos_efemerides()
swe.set_ephe_path(EPHE_PATH)

from tables import (
    SIGNS, PLANETS, DOMICILE, EXILE, EXALTATION, FALL, TRIPLICITY,
    SIGN_ELEMENT, SIGN_MODE, TERMS, decan_ruler, POINTS, ASPECTS,
    DEFAULT_ORB, MOON_ORB, CHALDEAN_HOUR_ORDER, WEEKDAY_RULER,
)

SWE_PLANET = {
    "Sol": swe.SUN, "Luna": swe.MOON, "Mercurio": swe.MERCURY,
    "Venus": swe.VENUS, "Marte": swe.MARS, "Júpiter": swe.JUPITER,
    "Saturno": swe.SATURN,
}


def sign_of(lon):
    lon = lon % 360
    idx = int(lon // 30)
    return SIGNS[idx], lon - idx * 30  # (signo, grado dentro del signo)


def norm360(x):
    return x % 360


# ---------------------------------------------------------------------------
# DIGNIDADES / ALMUTEN
# ---------------------------------------------------------------------------
def dignities_at(lon, is_day):
    """Devuelve dict planeta -> puntos, para el grado dado."""
    sign, deg = sign_of(lon)
    scores = {p: 0 for p in PLANETS}

    for p in DOMICILE[sign]:
        scores[p] += POINTS["domicilio"]

    if sign in EXALTATION:
        scores[EXALTATION[sign]] += POINTS["exaltacion"]

    element = SIGN_ELEMENT[sign]
    trip_day, trip_night, trip_part = TRIPLICITY[element]
    trip_ruler = trip_day if is_day else trip_night
    scores[trip_ruler] += POINTS["triplicidad"]

    for planet, g0, g1 in TERMS[sign]:
        if g0 <= deg < g1:
            scores[planet] += POINTS["termino"]
            break

    dp = decan_ruler(sign, deg)
    scores[dp] += POINTS["decanato"]

    if EXILE.get(sign):
        scores[EXILE[sign]] += POINTS["exilio"]
    if sign in FALL:
        scores[FALL[sign]] += POINTS["caida"]

    return scores


def almuten_of(lon, is_day):
    """Devuelve lista de (planeta, puntos) ordenada de mayor a menor,
    sólo con puntaje positivo (para no confundir 'almuten' con un exilio)."""
    scores = dignities_at(lon, is_day)
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)
    return ranked, scores


def essential_dignity_label(lon, planet, is_day):
    """Describe brevemente el estado esencial de `planet` en su propia posición `lon`."""
    sign, deg = sign_of(lon)
    labels = []
    if planet in DOMICILE[sign]:
        labels.append("domiciliado")
    if EXALTATION.get(sign) == planet:
        labels.append("exaltado")
    element = SIGN_ELEMENT[sign]
    trip_day, trip_night, trip_part = TRIPLICITY[element]
    if planet == (trip_day if is_day else trip_night):
        labels.append("triplicidad")
    for pl, g0, g1 in TERMS[sign]:
        if pl == planet and g0 <= deg < g1:
            labels.append("término propio")
    if decan_ruler(sign, deg) == planet:
        labels.append("decanato propio")
    if EXILE.get(sign) == planet:
        labels.append("EXILIADO")
    if FALL.get(sign) == planet:
        labels.append("EN CAÍDA")
    if not labels:
        labels.append("peregrino")
    return labels


# ---------------------------------------------------------------------------
# CARTA COMPLETA
# ---------------------------------------------------------------------------
def compute_chart(year, month, day, hour, minute, utc_offset, lat, lon_geo, tz_name=""):
    """
    hour/minute en hora LOCAL. utc_offset en horas (ej. Uruguay = -3).
    lat/lon_geo en grados decimales (lon_geo positivo = Este).
    """
    # Hora UT
    local_dt = dt.datetime(year, month, day, hour, minute)
    ut_dt = local_dt - dt.timedelta(hours=utc_offset)
    jd = swe.julday(ut_dt.year, ut_dt.month, ut_dt.day,
                     ut_dt.hour + ut_dt.minute / 60.0)

    # SEFLG_SWIEPH (efemérides Swiss reales, archivos .se1) con fallback
    # automático a Moshier si la fecha cae fuera del rango cargado (1800-2399).
    flag = swe.FLG_SWIEPH | swe.FLG_SPEED

    planets = {}
    ephe_used = {}
    for name, pid in SWE_PLANET.items():
        try:
            (lo, la, r, spd_lo, spd_la, spd_r), ret_flag = swe.calc_ut(jd, pid, flag)
        except swe.Error:
            (lo, la, r, spd_lo, spd_la, spd_r), ret_flag = swe.calc_ut(
                jd, pid, swe.FLG_MOSEPH | swe.FLG_SPEED)
        sign, deg = sign_of(lo)
        planets[name] = {
            "lon": lo, "sign": sign, "deg_in_sign": round(deg, 2),
            "speed": spd_lo, "retrograde": spd_lo < 0,
        }
        ephe_used[name] = "Swiss Ephemeris (SWIEPH)" if (ret_flag & swe.FLG_SWIEPH) else "Moshier (fuera de rango 1800-2399)"

    cusps, ascmc = swe.houses(jd, lat, lon_geo, b"P")  # Placidus
    asc = ascmc[0]
    mc = ascmc[1]
    house_cusps = list(cusps[0:12])  # cusps[0] = casa I ... índice 0-based

    # Determinar casa de cada planeta (casas Placidus por cúspides ya calculadas)
    def house_of(lon_p):
        for i in range(12):
            c0 = house_cusps[i]
            c1 = house_cusps[(i + 1) % 12]
            span = norm360(c1 - c0)
            rel = norm360(lon_p - c0)
            if rel < span:
                return i + 1
        return 12

    for name in planets:
        planets[name]["house"] = house_of(planets[name]["lon"])

    # Carta diurna/nocturna: Sol sobre el horizonte = casas VII a XII (sobre el eje ASC-DESC)
    sun_house = planets["Sol"]["house"]
    is_day = sun_house in (7, 8, 9, 10, 11, 12)

    # Signo interceptado (si una casa abarca un signo entero) - simplificado:
    # se detecta cuando dos cúspides consecutivas están en el mismo signo (signo "salteado")
    cusp_signs = [sign_of(c)[0] for c in house_cusps]
    intercepted = []
    covered = set(cusp_signs)
    for s in SIGNS:
        if s not in covered:
            intercepted.append(s)

    # Regente de la Hora (horas planetarias caldeas, con salida/puesta de sol reales)
    hour_ruler, hour_info = planetary_hour_ruler(jd, ut_dt, lat, lon_geo)

    return {
        "jd_ut": jd,
        "local_datetime": local_dt.isoformat(),
        "utc_offset": utc_offset,
        "lat": lat, "lon": lon_geo,
        "asc": asc, "mc": mc,
        "asc_sign": sign_of(asc)[0], "asc_deg": round(sign_of(asc)[1], 2),
        "mc_sign": sign_of(mc)[0], "mc_deg": round(sign_of(mc)[1], 2),
        "house_cusps": house_cusps,
        "planets": planets,
        "is_day": is_day,
        "intercepted_signs": intercepted,
        "hour_ruler": hour_ruler,
        "hour_info": hour_info,
        "ephemeris_source": ephe_used,
    }


def planetary_hour_ruler(jd_ut, ut_dt, lat, lon_geo):
    """Calcula el regente de la hora planetaria caldea vigente."""
    try:
        # Salida y puesta de sol del día (aprox, en UT) usando swe.rise_trans
        geopos = (lon_geo, lat, 0)
        jd_start = swe.julday(ut_dt.year, ut_dt.month, ut_dt.day, 0.0)
        rflag = swe.CALC_RISE | swe.BIT_DISC_CENTER
        _, tret_rise = swe.rise_trans(jd_start, swe.SUN, rflag, geopos)
        sflag = swe.CALC_SET | swe.BIT_DISC_CENTER
        _, tret_set = swe.rise_trans(jd_start, swe.SUN, sflag, geopos)
        sunrise = tret_rise[0]
        sunset = tret_set[0]

        weekday = ut_dt.weekday()  # 0=lunes
        if jd_ut >= sunrise and jd_ut < sunset:
            # Hora diurna: 12 horas entre orto y ocaso
            day_ruler = WEEKDAY_RULER[weekday]
            start_idx = CHALDEAN_HOUR_ORDER.index(day_ruler)
            span = (sunset - sunrise) / 12.0
            hour_n = int((jd_ut - sunrise) / span)
            planet = CHALDEAN_HOUR_ORDER[(start_idx + hour_n) % 7]
            return planet, {"periodo": "diurna", "hora_n": hour_n + 1}
        else:
            # Hora nocturna: buscar el ocaso anterior y el orto siguiente
            if jd_ut < sunrise:
                jd_prev = swe.julday(ut_dt.year, ut_dt.month, ut_dt.day - 1, 0.0)
                _, tret_set_prev = swe.rise_trans(jd_prev, swe.SUN, sflag, geopos)
                sunset_prev = tret_set_prev[0]
                night_start = sunset_prev
                night_end = sunrise
                weekday_of_night = (weekday - 1) % 7
            else:
                jd_next = swe.julday(ut_dt.year, ut_dt.month, ut_dt.day + 1, 0.0)
                _, tret_rise_next = swe.rise_trans(jd_next, swe.SUN, rflag, geopos)
                sunrise_next = tret_rise_next[0]
                night_start = sunset
                night_end = sunrise_next
                weekday_of_night = weekday
            day_ruler = WEEKDAY_RULER[weekday_of_night]
            start_idx = CHALDEAN_HOUR_ORDER.index(day_ruler)
            span = (night_end - night_start) / 12.0
            hour_n = int((jd_ut - night_start) / span)
            planet = CHALDEAN_HOUR_ORDER[(start_idx + 12 + hour_n) % 7]
            return planet, {"periodo": "nocturna", "hora_n": hour_n + 1}
    except Exception as e:
        return None, {"error": str(e)}


# ---------------------------------------------------------------------------
# ASPECTOS Y RECEPCIÓN
# ---------------------------------------------------------------------------
def angular_sep(a, b):
    d = abs(norm360(a - b))
    return min(d, 360 - d)


def find_aspects(chart):
    planets = chart["planets"]
    names = list(planets.keys())
    result = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            p1, p2 = names[i], names[j]
            lon1, lon2 = planets[p1]["lon"], planets[p2]["lon"]
            sep = angular_sep(lon1, lon2)
            for asp_name, asp_deg in ASPECTS.items():
                orb = MOON_ORB if ("Luna" in (p1, p2)) else DEFAULT_ORB
                diff = abs(sep - asp_deg)
                if diff <= orb:
                    # Aplicativo o separativo: comparar velocidades relativas
                    faster, slower = (p1, p2) if planets[p1]["speed"] > planets[p2]["speed"] else (p2, p1)
                    # distancia angular orientada del más rápido al más lento en la dirección del movimiento
                    applying = _is_applying(planets[p1]["lon"], planets[p1]["speed"],
                                             planets[p2]["lon"], planets[p2]["speed"], asp_deg)
                    reception = reception_between(chart, p1, p2)
                    result.append({
                        "p1": p1, "p2": p2, "aspecto": asp_name,
                        "orbe": round(diff, 2), "aplicativo": applying,
                        "recepcion": reception,
                    })
                    break
    return result


def _is_applying(lon1, spd1, lon2, spd2, asp_deg):
    """Aproximación: mira si la separación angular hacia el aspecto exacto
    disminuye avanzando ambos planetas a su velocidad actual."""
    sep_now = angular_sep(lon1, lon2)
    dt_test = 0.5  # medio día
    lon1_f = lon1 + spd1 * dt_test
    lon2_f = lon2 + spd2 * dt_test
    sep_future = angular_sep(lon1_f, lon2_f)
    return abs(sep_future - asp_deg) < abs(sep_now - asp_deg)


def reception_between(chart, p1, p2):
    """Calcula si p1 recibe a p2 y/o viceversa, y si es mutua, según el
    grado exacto de cada uno (domicilio/exaltación/triplicidad/término/decanato)."""
    is_day = chart["is_day"]
    lon1, lon2 = chart["planets"][p1]["lon"], chart["planets"][p2]["lon"]
    scores_at_1 = dignities_at(lon1, is_day)  # quién recibe a un planeta situado en lon1
    scores_at_2 = dignities_at(lon2, is_day)
    p2_received_by_1 = scores_at_1.get(p2, 0) > 0  # p2 tiene dignidad sobre el grado donde está p1? no.
    # Recepción correcta: "p1 es recibido por p2" si p2 tiene dignidad sobre el grado en que ESTÁ p1.
    p1_received_by_p2 = dignities_at(lon1, is_day).get(p2, 0) > 0
    p2_received_by_p1 = dignities_at(lon2, is_day).get(p1, 0) > 0
    if p1_received_by_p2 and p2_received_by_p1:
        return "mutua"
    if p1_received_by_p2:
        return f"{p1} recibido por {p2}"
    if p2_received_by_p1:
        return f"{p2} recibido por {p1}"
    return None


def _moon_aspect_candidates(chart):
    """Calcula (y devuelve completas, ordenadas) las listas de aspectos
    pasados y aplicativos de la Luna con los demás planetas."""
    moon_lon = chart["planets"]["Luna"]["lon"]
    moon_spd = chart["planets"]["Luna"]["speed"]
    candidates_next = []
    candidates_last = []

    PASO = 0.02   # ~29 minutos
    RANGO = 30.0  # días hacia cada lado

    for name, data in chart["planets"].items():
        if name == "Luna":
            continue
        other_lon = data["lon"]
        other_spd = data["speed"]

        for asp_name, asp_deg in ASPECTS.items():
            orb = MOON_ORB
            sep_ahora = angular_sep(moon_lon, other_lon)
            if abs(sep_ahora - asp_deg) > orb:
                continue  # ni siquiera está en orbe ahora; no es el aspecto relevante

            def f(t):
                return angular_sep(moon_lon + moon_spd * t, other_lon + other_spd * t) - asp_deg

            dias_next = None
            t_prev, f_prev = 0.0, f(0.0)
            t = PASO
            while t <= RANGO:
                f_now = f(t)
                if f_prev == 0 or (f_prev > 0) != (f_now > 0):
                    if f_now != f_prev:
                        dias_next = t_prev + (0 - f_prev) * (t - t_prev) / (f_now - f_prev)
                    else:
                        dias_next = t
                    break
                t_prev, f_prev = t, f_now
                t += PASO

            dias_last = None
            t_prev, f_prev = 0.0, f(0.0)
            t = -PASO
            while t >= -RANGO:
                f_now = f(t)
                if f_prev == 0 or (f_prev > 0) != (f_now > 0):
                    if f_now != f_prev:
                        dias_last = t_prev + (0 - f_prev) * (t - t_prev) / (f_now - f_prev)
                    else:
                        dias_last = t
                    break
                t_prev, f_prev = t, f_now
                t -= PASO

            if dias_next is not None and 0 < dias_next < RANGO:
                candidates_next.append({"planeta": name, "aspecto": asp_name,
                                         "orbe": round(abs(sep_ahora - asp_deg), 2),
                                         "dias": round(dias_next, 2),
                                         "lon_otro_ahora": other_lon, "spd_otro": other_spd})
            if dias_last is not None and -RANGO < dias_last < 0:
                candidates_last.append({"planeta": name, "aspecto": asp_name,
                                         "orbe": round(abs(sep_ahora - asp_deg), 2),
                                         "dias": round(dias_last, 2)})

    candidates_next.sort(key=lambda e: e["dias"])
    candidates_last.sort(key=lambda e: -e["dias"])
    return candidates_last, candidates_next


def moon_last_next_aspect(chart):
    """Último aspecto (separativo) y próximo aspecto (aplicativo) de la Luna
    con cualquiera de los otros 6 planetas clásicos. Usa un barrido numérico
    (en vez de una fórmula analítica con supuestos de signo) para no
    confundirse cuando la Luna está "detrás" del otro planeta acercándose
    a una conjunción."""
    candidates_last, candidates_next = _moon_aspect_candidates(chart)
    last = {k: v for k, v in candidates_last[0].items()} if candidates_last else None
    nxt = {k: v for k, v in candidates_next[0].items() if k not in ("lon_otro_ahora", "spd_otro")} if candidates_next else None
    return (last, nxt)


def _dias_a_cambio_signo(deg_in_sign, speed):
    """Días hasta que un planeta cambie de signo, dado su grado dentro del
    signo actual (0-30) y su velocidad diaria (puede ser negativa si es
    retrógrado)."""
    if speed > 0:
        return (30 - deg_in_sign) / speed
    elif speed < 0:
        return deg_in_sign / abs(speed)
    return None


def moon_void_of_course(chart):
    """Luna vacía de curso: no completa ningún aspecto mayor antes de cambiar
    de signo ELLA MISMA, y además el aspecto tiene que completarse antes de
    que el OTRO planeta involucrado cambie de signo (si el otro planeta se
    va de signo antes, ese aspecto no cuenta como "salvador")."""
    candidates_last, candidates_next = _moon_aspect_candidates(chart)
    moon_deg = chart["planets"]["Luna"]["deg_in_sign"]
    moon_spd = chart["planets"]["Luna"]["speed"]
    dias_cambio_luna = _dias_a_cambio_signo(moon_deg, moon_spd)

    if dias_cambio_luna is None:
        # Luna estacionaria (rarísimo): no hay ventana clara, se informa vacía
        return True, None

    for cand in candidates_next:
        if cand["dias"] >= dias_cambio_luna:
            continue  # la Luna cambia de signo antes de completar este aspecto
        otro_deg = chart["planets"][cand["planeta"]]["deg_in_sign"]
        otro_spd = cand["spd_otro"]
        dias_cambio_otro = _dias_a_cambio_signo(otro_deg, otro_spd)
        if dias_cambio_otro is not None and cand["dias"] >= dias_cambio_otro:
            continue  # el otro planeta cambia de signo antes de que se complete el aspecto
        return False, dias_cambio_luna  # hay un aspecto válido: no está vacía de curso

    return True, dias_cambio_luna


def via_combusta(chart):
    """Luna entre 15° Libra y 15° Escorpio (vía combusta clásica)."""
    lon = chart["planets"]["Luna"]["lon"]
    start = 6 * 30 + 15  # 15° Libra
    end = 7 * 30 + 15    # 15° Escorpio
    return start <= lon <= end
