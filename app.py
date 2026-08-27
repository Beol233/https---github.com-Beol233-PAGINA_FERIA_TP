from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
    session
)
import os
import uuid

from flask_bcrypt import Bcrypt
from functools import wraps


from werkzeug.utils import secure_filename
from mysqlconnection import connectToMySQL

from config import DB_NAME

from usuario import Usuario
from libro import Libro
from prestamo import Prestamo
from categorias import Categoria
from roles import Rol


app = Flask(__name__)

bcrypt = Bcrypt(app)

app.secret_key = "fjwefwein"


# =========================================================
# PROTECCIÓN DE RUTAS
# =========================================================

def login_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "usuario_id" not in session:

            flash("Debes iniciar sesión.")

            return redirect(url_for("login"))

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        if "usuario_id" not in session:

            flash("Debes iniciar sesión.")

            return redirect(url_for("login"))

        if session.get("tipo_usuario") != "admin":

            flash("No tienes permisos para entrar a esta sección.")

            return redirect(url_for("libros"))

        return func(*args, **kwargs)

    return wrapper


# =========================================================
# INICIO
# =========================================================

@app.route("/")
def inicio():

    if "usuario_id" in session:

        return redirect(url_for("libros"))

    return redirect(url_for("login"))


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        correo = request.form["correo"].strip().lower()
        password = request.form["password"]

        usuario = Usuario.get_by_email(correo)

        if usuario and bcrypt.check_password_hash(
            usuario.password,
            password
        ):

            session["usuario_id"] = usuario.id
            session["usuario"] = usuario.nombre
            session["tipo_usuario"] = usuario.tipo_usuario
            session["rol_id"] = usuario.rol_id

            if usuario.tipo_usuario == "admin":
                return redirect(url_for("gestion"))


            return redirect(url_for("libros"))

        flash("Correo o contraseña incorrectos.")

    return render_template("login.html")


# =========================================================
# REGISTRO
# =========================================================

@app.route("/registro", methods=["GET", "POST"])
def registro():

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        correo = request.form["correo"].strip().lower()

        tipo_usuario = request.form.get("tipo_usuario")

        password = request.form["password"]
        confirmar = request.form["confirmar"]

        # -----------------------------------------
        # Validar campos
        # -----------------------------------------

        if not nombre or not apellido or not correo:

            flash("Rellena todos los datos.")

            return redirect(url_for("registro"))

        if not password or not confirmar:

            flash("Debes ingresar una contraseña.")

            return redirect(url_for("registro"))

        # El registro público NO puede crear admins
        if tipo_usuario not in [
            "alumno",
            "profesor"
        ]:

            flash("Seleccione un tipo de usuario válido.")

            return redirect(url_for("registro"))

        if password != confirmar:

            flash("Las contraseñas no coinciden.")

            return redirect(url_for("registro"))

        # -----------------------------------------
        # Revisar correo existente
        # -----------------------------------------

        usuario_existente = Usuario.get_by_email(correo)

        if usuario_existente:

            flash("Este correo ya está registrado.")

            return redirect(url_for("registro"))

        # -----------------------------------------
        # Obtener rol
        # -----------------------------------------

        rol = Rol.get_by_nombre(tipo_usuario)

        if not rol:

            flash("El rol seleccionado no existe.")

            return redirect(url_for("registro"))

        # -----------------------------------------
        # Hash contraseña
        # -----------------------------------------

        password_hash = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        # -----------------------------------------
        # Crear usuario
        # -----------------------------------------

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "password": password_hash,
            "matricula": None,
            "rol_id": rol.id
        }

        resultado = Usuario.crear(datos)

        if resultado is False:

            flash("No se pudo crear la cuenta.")

            return redirect(url_for("registro"))

        flash(
            "Su cuenta está creada. Ahora puedes iniciar sesión."
        )

        return redirect(url_for("login"))

    return render_template("registro.html")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =========================================================
# LIBROS / COLECCIÓN
# =========================================================

@app.route("/libros")
@login_required
def libros():

    lista_libros = Libro.get_all()

    return render_template(
        "libros.html",
        libros=lista_libros,
        generos_seleccionados=[],
        disponibilidad_seleccionada="todos"
    )

# =========================================================
# DETALLE DE UN LIBRO
# =========================================================

@app.route("/libros/<int:libro_id>")
@login_required
def detalle_libro(libro_id):

    libro = Libro.get_by_id(libro_id)

    if not libro:

        flash("El libro no existe.")

        return redirect(
            url_for("libros")
        )

    return render_template(
        "detalle_libro.html",
        libro=libro
    )

# =========================================================
# BUSCADOR DE LIBROS
# =========================================================

@app.route("/buscar")
@login_required
def buscar():

    texto = request.args.get(
        "q",
        ""
    ).strip()

    generos = request.args.getlist(
        "genero"
    )

    disponibilidad = request.args.get(
        "disponibilidad",
        "todos"
    )

    lista_libros = Libro.filtrar(
        texto=texto,
        generos=generos,
        disponibilidad=disponibilidad
    )

    return render_template(
        "libros.html",
        libros=lista_libros,
        busqueda=texto,
        generos_seleccionados=generos,
        disponibilidad_seleccionada=disponibilidad
    )

# =========================================================
# ESCÁNER
# =========================================================

@app.route("/escaner")
@login_required
def escaner():

    return render_template("escaner.html")


@app.route("/buscar_codigo", methods=["POST"])
@login_required
def buscar_codigo():

    datos = request.get_json()

    if not datos:

        return jsonify({
            "encontrado": False,
            "mensaje": "No se recibieron datos."
        }), 400

    codigo = str(
        datos.get("codigo", "")
    ).strip()

    if not codigo:

        return jsonify({
            "encontrado": False,
            "mensaje": "Código no recibido."
        }), 400

    libro = Libro.buscar_por_codigo(codigo)

    if not libro:

        return jsonify({
            "encontrado": False,
            "mensaje": "Libro no encontrado."
        })

    return jsonify({
        "encontrado": True,
        "id": libro.id,
        "titulo": libro.titulo,
        "autor": libro.autor,
        "editorial": libro.editorial,
        "cantidad_disponible": libro.cantidad_disponible
    })


# =========================================================
# PRÉSTAMOS
# =========================================================
# =========================================================
# PÁGINA DE PRÉSTAMOS
# =========================================================

@app.route("/prestamo")
@login_required
def prestamo():

    # Actualizar automáticamente los atrasados
    Prestamo.actualizar_atrasados()

    # Libro que viene seleccionado desde el escáner
    libro_id_seleccionado = request.args.get(
        "libro_id",
        type=int
    )

    # ADMIN: ve todos los préstamos
    if session.get("tipo_usuario") == "admin":

        lista_prestamos = Prestamo.get_all()
        lista_usuarios = Usuario.get_all()
        lista_libros = Libro.get_all()

    # ALUMNO / PROFESOR: solo ve sus préstamos
    else:

        lista_prestamos = Prestamo.get_by_usuario(
            session["usuario_id"]
        )

        lista_usuarios = []
        lista_libros = []


    activos = 0
    atrasados = 0

    for prestamo_actual in lista_prestamos:

        if prestamo_actual.estado == "activo":
            activos += 1

        elif prestamo_actual.estado == "atrasado":
            atrasados += 1


    return render_template(
        "prestamo.html",

        prestamos=lista_prestamos,
        usuarios=lista_usuarios,
        libros=lista_libros,

        activos=activos,
        atrasados=atrasados,

        libro_id_seleccionado=libro_id_seleccionado
    )


# =========================================================
# CREAR PRÉSTAMO
# =========================================================

@app.route("/prestamos/crear", methods=["POST"])
@admin_required
def crear_prestamo():

    usuario_id = request.form.get("usuario_id")
    libro_id = request.form.get("libro_id")
    fecha_dev_esperada = request.form.get(
        "fecha_dev_esperada"
    )

    # Validar campos
    if not usuario_id or not libro_id or not fecha_dev_esperada:

        flash(
            "Debes completar todos los campos."
        )

        return redirect(
            url_for("prestamo")
        )


    resultado = Prestamo.crear({
        "usuario_id": usuario_id,
        "libro_id": libro_id,
        "fecha_dev_esperada": fecha_dev_esperada
    })


    if resultado:

        flash(
            "Préstamo realizado correctamente."
        )

    else:

        flash(
            "No se pudo realizar el préstamo."
        )


    return redirect(
        url_for("prestamo")
    )


# =========================================================
# DEVOLVER LIBRO
# =========================================================

@app.route(
    "/prestamos/<int:prestamo_id>/devolver",
    methods=["POST"]
)
@admin_required
def devolver_libro(prestamo_id):

    resultado = Prestamo.devolver(
        prestamo_id
    )

    if resultado["ok"]:

        flash(
            "Libro devuelto correctamente."
        )

    else:

        flash(
            resultado["mensaje"]
        )

    return redirect(
        url_for("prestamo")
    )

# =========================================================
# PERFIL
# =========================================================

@app.route("/perfil")
@login_required
def perfil():

    usuario = Usuario.get_by_id(
        session["usuario_id"]
    )

    prestamos_usuario = Prestamo.get_by_usuario(
        session["usuario_id"]
    )

    return render_template(
        "perfil.html",
        usuario=usuario,
        prestamos=prestamos_usuario
    )


# =========================================================
# AJUSTES
# =========================================================

@app.route("/ajustes")
@login_required
def ajustes():

    return render_template(
        "ajustes.html"
    )


# =========================================================
# PANEL DE GESTIÓN
# =========================================================

@app.route("/gestion")
@admin_required
def gestion():

    return render_template(
        "gestion.html"
    )


# =========================================================
# GESTIÓN DE LIBROS
# =========================================================

@app.route("/gestion/libros")
@admin_required
def gestion_libros():

    lista_libros = Libro.get_all()

    return render_template(
        "gestion_libros.html",
        libros=lista_libros
    )


# =========================================================
# AGREGAR LIBRO
# =========================================================

@app.route(
    "/gestion/libros/agregar",
    methods=["GET", "POST"]
)
@admin_required
def agregar_libro():

    categorias = Categoria.get_all()

    if request.method == "POST":

        titulo = request.form["titulo"].strip()

        autor = request.form["autor"].strip()

        if not titulo or not autor:

            flash("El título y el autor son obligatorios.")

            return redirect(
                url_for("agregar_libro")
            )

        cantidad = int(
            request.form.get(
                "cantidad_total",
                1
            )
        )

        datos = {

            "isbn":
                request.form.get("isbn") or None,

            "titulo":
                titulo,

            "autor":
                autor,

            "editorial":
                request.form.get("editorial") or None,

            "anio":
                request.form.get("anio") or None,

            "cantidad_total":
                cantidad,

            "portada_url":
                request.form.get("portada_url") or None,

            "categoria_id":
                request.form["categoria_id"]
        }

        resultado = Libro.crear(datos)

        if resultado is False:

            flash("No se pudo agregar el libro.")

        else:

            flash("Libro agregado correctamente.")

            return redirect(
                url_for("gestion_libros")
            )

    return render_template(
        "formulario_libro.html",
        categorias=categorias
    )


# =========================================================
# EDITAR LIBRO
# =========================================================

@app.route(
    "/gestion/libros/<int:libro_id>/editar",
    methods=["GET", "POST"]
)
@admin_required
def editar_libro(libro_id):

    libro = Libro.get_by_id(libro_id)

    if not libro:

        flash("El libro no existe.")

        return redirect(
            url_for("gestion_libros")
        )

    categorias = Categoria.get_all()

    if request.method == "POST":

        datos = {

            "id":
                libro_id,

            "isbn":
                request.form.get("isbn") or None,

            "titulo":
                request.form["titulo"].strip(),

            "autor":
                request.form["autor"].strip(),

            "editorial":
                request.form.get("editorial") or None,

            "anio":
                request.form.get("anio") or None,

            "cantidad_total":
                int(request.form["cantidad_total"]),

            "portada_url":
                request.form.get("portada_url") or None,

            "categoria_id":
                request.form["categoria_id"]
        }

        resultado = Libro.actualizar(datos)

        if resultado is False:

            flash("No se pudo actualizar el libro.")

        else:

            flash("Libro actualizado correctamente.")

            return redirect(
                url_for("gestion_libros")
            )

    return render_template(
        "formulario_libro.html",
        libro=libro,
        categorias=categorias
    )


# =========================================================
# ELIMINAR LIBRO
# =========================================================

@app.route(
    "/gestion/libros/<int:libro_id>/eliminar",
    methods=["POST"]
)
@admin_required
def eliminar_libro(libro_id):

    resultado = Libro.eliminar(
        libro_id
    )

    if resultado is False:

        flash(
            "No se pudo eliminar el libro."
        )

    elif resultado == 0:

        flash(
            "El libro no existe."
        )

    else:

        flash(
            "Libro eliminado correctamente."
        )

    return redirect(
        url_for("gestion_libros")
    )


# =========================================================
# GESTIÓN DE USUARIOS
# =========================================================

@app.route("/gestion/usuarios")
@admin_required
def gestion_usuarios():

    lista_usuarios = Usuario.get_all()

    return render_template(
        "gestion_usuarios.html",
        usuarios=lista_usuarios
    )


# =========================================================
# AGREGAR USUARIO DESDE GESTIÓN
# =========================================================

@app.route(
    "/gestion/usuarios/agregar",
    methods=["GET", "POST"]
)
@admin_required
def agregar_usuario():

    roles = Rol.get_all()

    if request.method == "POST":

        nombre = request.form["nombre"].strip()
        apellido = request.form["apellido"].strip()
        correo = request.form["correo"].strip().lower()
        password = request.form["password"]

        if Usuario.get_by_email(correo):

            flash("El correo ya está registrado.")

            return redirect(
                url_for("agregar_usuario")
            )

        hashed = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        datos = {

            "nombre":
                nombre,

            "apellido":
                apellido,

            "correo":
                correo,

            "password":
                hashed,

            "matricula":
                request.form.get("matricula") or None,

            "rol_id":
                request.form["rol_id"]
        }

        resultado = Usuario.crear(datos)

        if resultado is False:

            flash("No se pudo crear el usuario.")

        else:

            flash("Usuario creado correctamente.")

            return redirect(
                url_for("gestion_usuarios")
            )

    return render_template(
        "formulario_usuario.html",
        roles=roles
    )


# =========================================================
# EDITAR USUARIO
# =========================================================

@app.route(
    "/gestion/usuarios/<int:usuario_id>/editar",
    methods=["GET", "POST"]
)
@admin_required
def editar_usuario(usuario_id):

    usuario = Usuario.get_by_id(
        usuario_id
    )

    if not usuario:

        flash("El usuario no existe.")

        return redirect(
            url_for("gestion_usuarios")
        )

    roles = Rol.get_all()

    if request.method == "POST":

        datos = {

            "id":
                usuario_id,

            "nombre":
                request.form["nombre"].strip(),

            "apellido":
                request.form["apellido"].strip(),

            "correo":
                request.form["correo"].strip().lower(),

            "matricula":
                request.form.get("matricula") or None,

            "rol_id":
                request.form["rol_id"]
        }

        resultado = Usuario.actualizar(datos)

        if resultado is False:

            flash("No se pudo editar el usuario.")

        else:

            flash("Usuario actualizado.")

            return redirect(
                url_for("gestion_usuarios")
            )

    return render_template(
        "formulario_usuario.html",
        usuario=usuario,
        roles=roles
    )


# =========================================================
# ELIMINAR USUARIO
# =========================================================

@app.route(
    "/gestion/usuarios/<int:usuario_id>/eliminar",
    methods=["POST"]
)
@admin_required
def eliminar_usuario(usuario_id):

    # No permitir que el admin elimine su propia cuenta
    if usuario_id == session["usuario_id"]:

        flash(
            "No puedes eliminar tu propia cuenta."
        )

        return redirect(
            url_for("gestion_usuarios")
        )

    resultado = Usuario.eliminar(
        usuario_id
    )

    if resultado is False:

        flash(
            "No se pudo eliminar el usuario."
        )

    elif resultado == 0:

        flash(
            "El usuario no existe."
        )

    else:

        flash(
            "Usuario eliminado correctamente."
        )

    return redirect(
        url_for("gestion_usuarios")
    )

# =========================================================
# EDITAR MI PERFIL
# =========================================================

@app.route(
    "/perfil/editar",
    methods=["POST"]
)
@login_required
def editar_perfil():

    usuario_id = session["usuario_id"]

    nombre = request.form["nombre"].strip()
    apellido = request.form["apellido"].strip()
    correo = request.form["correo"].strip().lower()

    if not nombre or not apellido or not correo:

        flash("Nombre, apellido y correo son obligatorios.")

        return redirect(
            url_for("perfil")
        )


    # -----------------------------------------------------
    # Comprobar que otro usuario no tenga ese correo
    # -----------------------------------------------------

    mysql = connectToMySQL(DB_NAME)

    correo_existente = mysql.query_db(
        """
        SELECT id
        FROM usuarios
        WHERE LOWER(correo) = %(correo)s
        AND id != %(usuario_id)s
        """,
        {
            "correo": correo,
            "usuario_id": usuario_id
        }
    )


    if correo_existente:

        flash("Ese correo ya pertenece a otro usuario.")

        return redirect(
            url_for("perfil")
        )


    # -----------------------------------------------------
    # FOTO
    # -----------------------------------------------------

    foto = request.files.get(
        "foto_perfil"
    )

    ruta_foto = None


    if foto and foto.filename:

        extensiones_permitidas = {
            "jpg",
            "jpeg",
            "png",
            "webp"
        }


        nombre_seguro = secure_filename(
            foto.filename
        )


        if "." not in nombre_seguro:

            flash("La imagen no tiene una extensión válida.")

            return redirect(
                url_for("perfil")
            )


        extension = (
            nombre_seguro
            .rsplit(".", 1)[1]
            .lower()
        )


        if extension not in extensiones_permitidas:

            flash(
                "La foto debe ser JPG, PNG o WEBP."
            )

            return redirect(
                url_for("perfil")
            )


        nuevo_nombre = (
            f"usuario_{usuario_id}_"
            f"{uuid.uuid4().hex}.{extension}"
        )


        carpeta = os.path.join(
            app.static_folder,
            "uploads",
            "perfiles"
        )


        os.makedirs(
            carpeta,
            exist_ok=True
        )


        ruta_completa = os.path.join(
            carpeta,
            nuevo_nombre
        )


        foto.save(
            ruta_completa
        )


        ruta_foto = (
            f"uploads/perfiles/{nuevo_nombre}"
        )


    # -----------------------------------------------------
    # ACTUALIZAR USUARIO
    # -----------------------------------------------------

    mysql = connectToMySQL(DB_NAME)


    if ruta_foto:

        query = """
            UPDATE usuarios
            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                correo = %(correo)s,
                foto_perfil = %(foto_perfil)s,
                updated_at = NOW()
            WHERE id = %(usuario_id)s
        """

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "foto_perfil": ruta_foto,
            "usuario_id": usuario_id
        }


    else:

        query = """
            UPDATE usuarios
            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                correo = %(correo)s,
                updated_at = NOW()
            WHERE id = %(usuario_id)s
        """

        datos = {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "usuario_id": usuario_id
        }


    resultado = mysql.query_db(
        query,
        datos
    )


    if resultado is False:

        flash(
            "No se pudieron guardar los cambios."
        )

        return redirect(
            url_for("perfil")
        )


    # Actualizar nombre guardado en sesión

    session["usuario"] = nombre


    flash(
        "Perfil actualizado correctamente."
    )


    return redirect(
        url_for("perfil")
    )

# =========================================================
# EJECUTAR FLASK
# =========================================================

if __name__ == "__main__":

    app.run(debug=True)