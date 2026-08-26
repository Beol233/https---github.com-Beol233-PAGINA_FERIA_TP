from flask_bcrypt import Bcrypt

from config import DB_NAME
from mysqlconnection import connectToMySQL


bcrypt = Bcrypt()


print("================================")
print(" CREAR ADMINISTRADOR - LIBROTECA")
print("================================")


nombre = input("Nombre: ").strip()
apellido = input("Apellido: ").strip()
correo = input("Correo: ").strip().lower()
password = input("Contraseña: ").strip()


if not nombre or not apellido or not correo or not password:
    print("ERROR: Debes completar todos los datos.")
    exit()


# Buscar el rol admin
query_rol = """
    SELECT id
    FROM roles
    WHERE nombre = 'admin'
    LIMIT 1;
"""

resultado_rol = connectToMySQL(
    DB_NAME
).query_db(query_rol)


if not resultado_rol:
    print("ERROR: No existe el rol admin.")
    exit()


rol_id = resultado_rol[0]["id"]


# Crear hash de contraseña
password_hash = bcrypt.generate_password_hash(
    password
).decode("utf-8")


# Verificar si ya existe el correo
query_existente = """
    SELECT id
    FROM usuarios
    WHERE LOWER(correo) = %(correo)s
    LIMIT 1;
"""

usuario_existente = connectToMySQL(
    DB_NAME
).query_db(
    query_existente,
    {
        "correo": correo
    }
)


# Si ya existe, lo actualizamos como admin
if usuario_existente:

    usuario_id = usuario_existente[0]["id"]

    query_update = """
        UPDATE usuarios
        SET
            nombre = %(nombre)s,
            apellido = %(apellido)s,
            password = %(password)s,
            rol_id = %(rol_id)s,
            updated_at = NOW()
        WHERE id = %(id)s;
    """

    resultado = connectToMySQL(
        DB_NAME
    ).query_db(
        query_update,
        {
            "nombre": nombre,
            "apellido": apellido,
            "password": password_hash,
            "rol_id": rol_id,
            "id": usuario_id
        }
    )

    if resultado is False:
        print("ERROR: No se pudo actualizar el administrador.")
    else:
        print("")
        print("Administrador actualizado correctamente.")
        print("Correo:", correo)


# Si no existe, lo creamos
else:

    query_insert = """
        INSERT INTO usuarios (
            nombre,
            apellido,
            correo,
            password,
            matricula,
            rol_id
        )
        VALUES (
            %(nombre)s,
            %(apellido)s,
            %(correo)s,
            %(password)s,
            NULL,
            %(rol_id)s
        );
    """

    resultado = connectToMySQL(
        DB_NAME
    ).query_db(
        query_insert,
        {
            "nombre": nombre,
            "apellido": apellido,
            "correo": correo,
            "password": password_hash,
            "rol_id": rol_id
        }
    )

    if resultado is False:
        print("ERROR: No se pudo crear el administrador.")
    else:
        print("")
        print("Administrador creado correctamente.")
        print("Correo:", correo)