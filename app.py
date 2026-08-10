from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL

app = Flask(__name__)
bcrypt = Bcrypt(app)

# NOTA PEDAGÓGICA: la sesión y flash() de Flask NECESITAN una secret_key
# configurada, o Flask lanzará un error en tiempo de ejecución apenas se
# use session[...] o flash(...). Estaba comentada, lo que impedía que el
# login funcionara. Se descomenta y se deja un valor de desarrollo.
# IMPORTANTE: en un proyecto real esto NO debería quedar hardcodeado así;
# debería venir de una variable de entorno. Queda pendiente para más adelante.
app.secret_key = "fjwefwein"

# Nombre de la base de datos. Antes se usaba "BD" / "BD_NAME" en distintas
# partes del archivo sin que existiera en ningún lado. Se deja UNA sola
# constante y se usa siempre la misma, igual que ya hacía buscar_libro().
BD_NAME = "biblioteca"


def buscar_libro(codigo):
    query = """
        SELECT titulo, autor, editorial
        FROM libros
        WHERE codigo = %(codigo)s
    """

    datos = {
        "codigo": codigo
    }

    resultado = connectToMySQL(BD_NAME).query_db(query, datos)

    if resultado:
        libro = resultado[0]
        return (
            libro["titulo"],
            libro["autor"],
            libro["editorial"]
        )

    return None


# ruta inicial
@app.route("/")
def inicio():
    # Duda si tendria que ir a login o a registro
    return render_template("login.html")


# ruta hacia los libros
@app.route("/libros")
def libros():
    return render_template("libros.html")


# ruta para el lector del codigo del libro
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


# ruta de logearse
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # OJO: se cambió "usuario" por "correo". registro.html nunca pide un
        # nombre de usuario, solo nombre/apellido/correo/contraseña, así que
        # no existe ningún valor "usuario" guardado contra el cual comparar.
        # El correo es el único dato que sirve hoy como identificador único
        # (ver PARTE 2 si más adelante quieren agregar un username real).
        correo = request.form["correo"].strip()
        password = request.form["password"]

        mysql = connectToMySQL(BD_NAME)
        result = mysql.query_db(
            "SELECT id, nombre, correo, tipo_usuario, password_hash FROM users WHERE correo = %(correo)s",
            {"correo": correo}
        )
        # query_db devuelve una lista de diccionarios
        user = result[0] if result else None

        # Comparamos la contraseña ingresada contra el hash guardado, sin
        # necesitar "deshacer" el hash (eso no se puede).
        # OJO: con Flask-Bcrypt el método correcto es check_password_hash,
        # no checkpw (eso es de la librería bcrypt "pelada", no de Flask-Bcrypt).
        if user and bcrypt.check_password_hash(user["password_hash"], password):
            session["usuario_id"] = user["id"]
            session["usuario"] = user["nombre"]
            session["tipo_usuario"] = user["tipo_usuario"]
            return redirect(url_for("libros"))

        flash("usuario o contraseña incorrectos.")
        return redirect(url_for("login"))

    return render_template("login.html")


# Registro que solo da la entrada a el html
@app.route("/registro")
def registro():
    return render_template("registro.html")


# esta ruta solo procesa los datos que manda el formulario de registro
@app.route("/registro", methods=["POST"])
def registro_process():
    # ruta solo para procesar los datos del formulario de registro
    #
    # NOTA PEDAGÓGICA IMPORTANTE:
    # registro.html (revisar el template) pide estos campos: nombre,
    # apellido, password, confirmar, correo (name="correo", NO "gmail") y
    # tipo_usuario. No pide un campo "usuario" (nombre de usuario), pero
    # login.html sí espera un campo "usuario" para poder iniciar sesión.
    # Esto es una INCONSISTENCIA entre pantallas que el código original no
    # resolvía (usaba variables que nunca llegaban a definirse, como
    # "nombre", "apellido", "gmail", "password", "confirmar", sin sacarlas
    # de request.form). No se inventa aquí una solución (por ejemplo,
    # generar el "usuario" a partir del correo) porque es una decisión de
    # diseño que les corresponde tomar a ustedes. Ver PARTE 2, sección 8,
    # para más detalle.
    nombre = request.form["nombre"].strip()
    apellido = request.form["apellido"].strip()
    correo = request.form["correo"].strip()
    tipo_usuario = request.form.get("tipo_usuario")
    password = request.form["password"]
    confirmar = request.form["confirmar"]

    if not nombre or not apellido or not correo or not password or not confirmar:
        flash("Rellena Los datos que te piden")
        return redirect(url_for("registro"))

    if tipo_usuario not in ["alumno", "profesor", "admin"]:
        flash("Seleccione un tipo de usuario")
        return redirect(url_for("registro"))

    if password != confirmar:
        flash("Las contraseñas no coinciden")
        return redirect(url_for("registro"))

    # Chequeamos que el usuario no exista ya.
    # OJO: cada vez que queremos hacer una consulta, generamos una
    # conexión nueva con connectToMySQL, porque la clase MySQLConnection
    # cierra la conexión automáticamente después de cada query_db().
    #
    # NOTA: esta consulta asume que existe una tabla "users" con una
    # columna "correo". Esa tabla todavía NO existe en el proyecto
    # (db.sql está vacío) — ver PARTE 2, sección "Base de datos propuesta".
    # Al ejecutar esto hoy va a fallar con un error de MySQL porque la
    # tabla no existe; eso es esperado hasta que se cree el esquema.
    mysql = connectToMySQL(BD_NAME)
    existing = mysql.query_db(
        "SELECT id FROM users WHERE correo = %(correo)s",
        {"correo": correo}
    )
    if existing:
        flash("Este correo ya esta registrado.")
        return redirect(url_for("registro"))

    # AQUÍ está lo importante: NUNCA guardamos la contraseña tal cual.
    # Con Flask-Bcrypt, generate_password_hash() ya se encarga de crear
    # el hash y el salt por nosotros (no hace falta bcrypt.gensalt()
    # aparte, eso es de la librería bcrypt "pelada").
    hashed = bcrypt.generate_password_hash(password).decode("utf-8")

    mysql = connectToMySQL(BD_NAME)
    mysql.query_db(
        """
        INSERT INTO users (nombre, apellido, correo, tipo_usuario, password_hash)
        VALUES (%(nombre)s, %(apellido)s, %(correo)s, %(tipo_usuario)s, %(password_hash)s)
        """,
        {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "tipo_usuario": tipo_usuario,
            "password_hash": hashed
        }
    )

    flash("Su cuenta esta creada. Ahora puedes iniciar sesion")
    return redirect(url_for("login"))


# logout: elimina la sesión del usuario actual
@app.route("/logout")
def logout():
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
