from flask import Flask, render_template, redirect, request
import requests

app = Flask(__name__)

# ✅ FastAPI corre en 8000 si lo levantas con uvicorn
URL = "http://127.0.0.1:8000/v1/usuarios"

@app.route("/")
def inicio():
    respuesta = requests.get(URL)
    datos = respuesta.json()
    usuarios = datos["data"]

    return render_template("index.html", usuarios=usuarios)

@app.route("/eliminar/<id>")
def eliminar(id):
    requests.delete(URL + "/" + str(id))
    return redirect("/")

@app.route("/agregar")
def agregar():
    return render_template("editar.html")

@app.route("/guardar", methods=["POST"])
def guardar():
    nombre = request.form["nombre"]
    edad = request.form["edad"]

    respuesta = requests.get(URL)
    datos = respuesta.json()
    usuarios = datos["data"]

    if usuarios:
        ultimo_id = int(usuarios[-1]["id"])
        nuevo_id = ultimo_id + 1
    else:
        nuevo_id = 1

    nuevo_usuario = {
        "id": int(nuevo_id),
        "nombre": nombre,
        "edad": int(edad)
    }

    requests.post(URL, json=nuevo_usuario)
    return redirect("/")

if __name__ == "__main__":
    app.run(port=510, debug=True)