from __future__ import annotations

import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv

from llm.llm import procesa_lenguaje_natural

ROOT = Path(__file__).resolve().parent
REACT_BUILD_DIR = ROOT / "app" / "build"

# Serve React build if present (after `npm run build` inside app/)
app = Flask(
    __name__,
    static_folder=str(REACT_BUILD_DIR),
    static_url_path="/",
)

@app.route("/")
def home():
    # Al abrir la página: cargar React (si está compilado).
    index_path = REACT_BUILD_DIR / "index.html"
    if index_path.exists():
        return send_from_directory(REACT_BUILD_DIR, "index.html")
    return (
        "React aún no está compilado. Ejecuta `cd app && npm run build` "
        "y recarga esta página.",
        503,
    )


@app.route("/<path:path>")
def static_proxy(path: str):
    # Permite rutas del frontend (SPA) y assets.
    file_path = REACT_BUILD_DIR / path
    if file_path.exists():
        return send_from_directory(REACT_BUILD_DIR, path)
    # fallback SPA
    index_path = REACT_BUILD_DIR / "index.html"
    if index_path.exists():
        return send_from_directory(REACT_BUILD_DIR, "index.html")
    return ("React aún no está compilado.", 503)


@app.route("/api/mensaje", methods=["POST"])
def mensaje():
    data = request.get_json()
    mensaje_usuario = (data or {}).get("mensaje")

    return jsonify({"respuesta": procesa_lenguaje_natural(mensaje_usuario)})

if __name__ == "__main__":
    load_dotenv()
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)