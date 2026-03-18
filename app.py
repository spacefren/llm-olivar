from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/mensaje", methods=["POST"])
def mensaje():
    data = request.get_json()
    mensaje_usuario = data.get("mensaje")

    return jsonify({"respuesta": procesa_lenguaje_natural(mensaje_usuario)})

if __name__ == "__main__":
    load_dotenv()
    app.run(debug=True)