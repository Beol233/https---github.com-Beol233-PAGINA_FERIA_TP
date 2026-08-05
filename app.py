from flask import Flask, render_template, request, jsonify
from mysqlconnection import connectToMySQL

app = Flask(__name__)


def buscar_libro(codigo):
    query = """
        SELECT titulo, autor, editorial
        FROM libros
        WHERE codigo = %(codigo)s
    """

    datos = {
        "codigo": codigo
    }

    # Reemplaza "biblioteca" por el nombre real de tu base de datos
    resultado = connectToMySQL("biblioteca").query_db(query, datos)

    if resultado:
        libro = resultado[0]
        return (
            libro["titulo"],
            libro["autor"],
            libro["editorial"]
        )

    return None


@app.route("/")
def inicio():
    return render_template("login.html")


@app.route("/libros")
def libros():
    return render_template("libros.html")


@app.route("/buscar_codigo", methods=["POST"])
def buscar_codigo():

    datos = request.get_json()

    if not datos or "codigo" not in datos:
        return jsonify({
            "encontrado": False,
            "mensaje": "Código no recibido"
        }), 400

    codigo = datos["codigo"]

    libro = buscar_libro(codigo)

    if libro:
        return jsonify({
            "encontrado": True,
            "titulo": libro[0],
            "autor": libro[1],
            "editorial": libro[2]
        })

    return jsonify({
        "encontrado": False
    })
    
@app.route("/login", methods=["POST"])
def login():
        tipo = request.form.get("tipo_usuario")
        usuario = request.form.get("usuario")

        print("TIPO:", tipo)
        print("USUARIO:", usuario)

        return "Funcionó"
@app.route("/registro")
def registro():
    return render_template("registro.html")


if __name__ == "__main__":
    app.run(debug=True)