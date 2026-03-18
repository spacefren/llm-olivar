from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hola, esta es mi primera app web con Python 🚀"

if __name__ == "__main__":
    app.run(debug=True)