# -*- coding: utf-8 -*-
"""Geocodificación de lugares (API pública de Open-Meteo, sin necesidad de
API key) y cálculo del offset UTC real -con horario de verano- para una
fecha/hora concreta, a partir del nombre de zona horaria IANA (ej. 'Europe/Madrid')."""

import requests
import datetime as dt
from zoneinfo import ZoneInfo

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"


def buscar_lugares(texto, idioma="es"):
    """Devuelve una lista de coincidencias: nombre, país, provincia/estado,
    lat, lon, zona horaria IANA."""
    if not texto or len(texto.strip()) < 2:
        return []
    try:
        r = requests.get(GEOCODE_URL, params={
            "name": texto.strip(), "count": 8, "language": idioma, "format": "json",
        }, timeout=6)
        r.raise_for_status()
        data = r.json()
    except Exception as e:
        return {"error": str(e)}

    resultados = []
    for item in data.get("results", []) or []:
        resultados.append({
            "nombre": item.get("name"),
            "admin1": item.get("admin1", ""),
            "pais": item.get("country", ""),
            "lat": item.get("latitude"),
            "lon": item.get("longitude"),
            "timezone": item.get("timezone"),
            "etiqueta": ", ".join(filter(None, [item.get("name"), item.get("admin1"), item.get("country")])),
        })
    return resultados


def utc_offset_para(timezone_name, year, month, day, hour, minute):
    """Offset UTC (en horas, positivo al Este) real para esa fecha/hora local,
    respetando el horario de verano vigente en esa zona en esa fecha."""
    local_naive = dt.datetime(year, month, day, hour, minute)
    local_aware = local_naive.replace(tzinfo=ZoneInfo(timezone_name))
    offset = local_aware.utcoffset()
    return offset.total_seconds() / 3600.0
