from flask import Flask, render_template, request, jsonify,redirect
from flask_bcrypt import Bcrypt 
from mysqlconnection import connectToMySQL

app = Flask(__name__)
bcrypt = Bcrypt(app)


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
    if "user_id" in session:
        return render_template("")
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

# @app.route("/login", methods=["POST"])
# def login():
    
#         tipo = request.form.get("tipo_usuario")
#         usuario = request.form.get("usuario")

#         print("TIPO:", tipo)
#         print("USUARIO:", usuario)

#         return "Funcionó"
@app.route("/login", methods ["GET", "POST"])
def login():
    if  request.method == "POST"
    usuario =  request.form["usuario"].strip()
    password = request.form["password"]
    
    mysql = mysqlconnection(BD)
    result = mysql.query_db(
        "SELECT id", usuario, password.hash FROM users WHERE usuario ="$(usuario)s",
        {"usuario":usuario}
    )
    #query_bd devuelve una lista  de diccionarios
    user = result else None
    

    # contra el hash guardado, sin necesitar "deshacer" el hash (eso no se puede).
    if  user and bcrypt.checkpw(password.encode("uft-8"), user["password_hash"].encode("utf-8")):
        session["usuario"] = user["id"]
        session["usuario"] = user["usuario"]
        return redirect(url_for("home"))
    
    

    flash("usuario o contraseña incorrectos.")

    return redirect(url_for("login"))

    return render_template("login.html")

@app.route("/registro")

def registro():
    return render_template("registro.html")

@app.route("/registro" methods=[POST])

def registro_process():
    #ruta solo para procesar los datos del formulario de registro 
    
    usuario = request.form["usuario"].strip.()
    
    password = request.form["password"]
    
    if not usuario or not password:
    
        flash("Rellena Los datos que te piden")
    
        return redirect(url_for("registro"))
    
    # Chequeamos que el usuario no exista ya.
    # OJO: cada vez que queremos hacer una consulta, generamos una
    # conexión nueva con connectToMySQL, porque la clase MySQLConnection
    # cierra la conexión automáticamente después de cada query_db().
    mysql = connectToMySQL(BD)
    existing = mysql.query_db(
        "Select id from users where usuario = %(usuario)s",
        {"usuario":usuario}
    )
    if existing
        flash("Este usuario ya esta registro intenta con otro")
        return redirect(url_for(registro))
    
    # AQUÍ está lo importante: NUNCA guardamos la contraseña tal cual.
    # bcrypt.hashpw genera el hash. gensalt() crea un "salt" random para
    # que dos contraseñas iguales no generen el mismo hash (ver README).
    # bcrypt trabaja con bytes, por eso el .encode() y el .decode() al final
    # (para guardar el resultado como texto normal en la base de datos).
    
    
    hashed = bcrypt.hashpw(password.encode("uft-8"),bcrypt.gensalt()).decode("uft-8")
    mysql = connectToMySQL(BD_NAME)
    mysql.query_db(
        "INSERT INTO users(usuario,password_hash,) VALUES (%(usuario)s), (%password_hash)s)",
        {"usuario"usuario:, "password_hash":hashed}
    )
    
    flash("Su cuanta esta creada. Ahora puedes iniciar session")
    return redirect(url_for("login"))

@app.route("/lagout")
def lagout():
    session.clear()
    return redirect(url_for("login"))





@app.route("/escaner")
def escaner():
    return render_template("escaner.html")




@app.route("/prestamos")
def prestamos():
    return render_template("prestamo.html")



if __name__ == "__main__":
    app.run(debug=True)