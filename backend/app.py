# -*- coding: utf-8 -*-
import os
import json
import uuid
import time
import threading

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic

from report import build_report
from ai_prompt import SYSTEM_PROMPT, build_user_message
from geocode import buscar_lugares, utc_offset_para

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
MAX_FOLLOWUPS = 6

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None


@app.errorhandler(Exception)
def manejar_cualquier_error(e):
    """Red de seguridad: si algo se rompe en cualquier endpoint, devolver
    siempre JSON con el motivo real (y dejarlo en los logs de Render), en vez
    de que el servidor caiga y el navegador reciba una página HTML de error."""
    import traceback
    traceback.print_exc()
    return jsonify({"error": f"Error interno del servidor: {type(e).__name__}: {e}"}), 500

# --- Sesiones en memoria (informe + historial de preguntas de esta consulta) ---
SESSIONS = {}
SESSIONS_LOCK = threading.Lock()
SESSION_TTL_SECONDS = 60 * 60 * 12  # 12 horas


def _cleanup_sessions():
    now = time.time()
    dead = [sid for sid, s in SESSIONS.items() if now - s["created_at"] > SESSION_TTL_SECONDS]
    for sid in dead:
        SESSIONS.pop(sid, None)


@app.route("/api/health")
def health():
    return jsonify({"ok": True, "ia_configurada": bool(client)})


@app.route("/api/geocodificar")
def geocodificar():
    """Busca lugares por nombre (autocompletar). Ej: /api/geocodificar?q=Roma"""
    texto = request.args.get("q", "")
    resultados = buscar_lugares(texto)
    if isinstance(resultados, dict) and "error" in resultados:
        return jsonify({"error": resultados["error"]}), 502
    return jsonify({"resultados": resultados})


@app.route("/api/utc_offset", methods=["POST"])
def utc_offset():
    """Dado un timezone IANA y una fecha/hora local, devuelve el offset UTC
    real de esa fecha (respeta horario de verano)."""
    data = request.get_json(force=True)
    try:
        offset = utc_offset_para(
            data["timezone"], data["year"], data["month"], data["day"],
            data["hour"], data["minute"],
        )
        return jsonify({"utc_offset": offset})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/carta", methods=["POST"])
def crear_carta():
    """Calcula la carta y arma el informe técnico. Crea una sesión para
    poder hacer hasta 6 preguntas de seguimiento sobre este mismo tema."""
    data = request.get_json(force=True)
    required = ["year", "month", "day", "hour", "minute", "utc_offset", "lat", "lon"]
    for r in required:
        if r not in data:
            return jsonify({"error": f"Falta el campo {r}"}), 400

    try:
        report = build_report(data)
    except Exception as e:
        return jsonify({"error": f"No se pudo calcular la carta: {e}"}), 500

    report_public = {k: v for k, v in report.items() if k != "_chart_raw"}

    with SESSIONS_LOCK:
        _cleanup_sessions()
        session_id = str(uuid.uuid4())
        SESSIONS[session_id] = {
            "report": report,  # incluye _chart_raw, se usa server-side solamente
            "history": [],
            "created_at": time.time(),
        }

    return jsonify({"session_id": session_id, "informe": report_public})


@app.route("/api/preguntar", methods=["POST"])
def preguntar():
    """Responde una pregunta (inicial o de seguimiento) sobre la carta de la sesión.
    modo: 'ia' o 'sin_ia'. Sin IA sólo devuelve el informe técnico ya calculado
    (no vuelve a llamar a la IA); con IA usa la API de Anthropic."""
    data = request.get_json(force=True)
    session_id = data.get("session_id")
    question = (data.get("pregunta") or "").strip()
    modo = data.get("modo", "ia")

    if not session_id or session_id not in SESSIONS:
        return jsonify({"error": "Sesión no encontrada o expirada. Volvé a calcular la carta."}), 404
    if not question:
        return jsonify({"error": "Falta la pregunta."}), 400

    session = SESSIONS[session_id]
    history = session["history"]

    if modo == "sin_ia":
        report_public = {k: v for k, v in session["report"].items() if k != "_chart_raw"}
        return jsonify({
            "modo": "sin_ia",
            "informe": report_public,
            "preguntas_restantes": MAX_FOLLOWUPS - len(history),
        })

    # modo IA
    if not client:
        return jsonify({"error": "El servidor no tiene configurada ANTHROPIC_API_KEY."}), 500
    if len(history) >= MAX_FOLLOWUPS + 1:
        return jsonify({"error": f"Ya se alcanzó el máximo de {MAX_FOLLOWUPS} preguntas de seguimiento para este tema. Calculá una carta nueva para otra pregunta."}), 400

    report_public = {k: v for k, v in session["report"].items() if k != "_chart_raw"}
    report_json = json.dumps(report_public, ensure_ascii=False, default=str)

    user_message = build_user_message(question, report_json, history)

    try:
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=16000,
                thinking={"type": "disabled"},
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
        except anthropic.BadRequestError:
            # Por si el modelo/SDK no acepta el parámetro "thinking": reintentar sin él.
            resp = client.messages.create(
                model=MODEL,
                max_tokens=16000,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
        answer_text = "".join(
            block.text for block in resp.content if getattr(block, "type", None) == "text"
        )
        if resp.stop_reason == "max_tokens" and answer_text.strip():
            answer_text += ("\n\n[Nota: esta respuesta se cortó por límite de longitud. "
                             "Si quedó incompleta, pedime que la continúe o resumí la pregunta.]")
        if resp.stop_reason not in ("end_turn", "max_tokens"):
            usage_info = getattr(resp, "usage", None)
            answer_text += (f"\n\n---\n[Diagnóstico temporal: stop_reason={resp.stop_reason}, "
                             f"usage={usage_info}]")
        if not answer_text.strip():
            tipos = [getattr(b, "type", "?") for b in resp.content]
            return jsonify({
                "error": f"La IA no devolvió texto de respuesta (stop_reason: {resp.stop_reason}, "
                         f"tipos de contenido recibidos: {tipos}). Probá de nuevo o achicá la pregunta."
            }), 502
    except Exception as e:
        return jsonify({"error": f"Error consultando la IA: {e}"}), 502

    history.append({"pregunta": question, "respuesta": answer_text})

    return jsonify({
        "modo": "ia",
        "respuesta": answer_text,
        "preguntas_restantes": MAX_FOLLOWUPS + 1 - len(history),
    })


# --- Servir el frontend estático (para desplegar todo junto en Render) ---
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
