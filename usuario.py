from config import DB_NAME
from mysqlconnection import connectToMySQL


class Usuario:

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.apellido = data["apellido"]
        self.correo = data["correo"]

        # Algunas consultas podrían no traer password
        self.password = data.get("password")

        self.matricula = data.get("matricula")

        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

        self.rol_id = data["rol_id"]

        # Solo aparece cuando hacemos JOIN con roles
        self.tipo_usuario = data.get("tipo_usuario")


    # =====================================================
    # OBTENER TODOS LOS USUARIOS
    # =====================================================
    @classmethod
    def get_all(cls):

        query = """
            SELECT
                usuarios.*,
                roles.nombre AS tipo_usuario

            FROM usuarios

            JOIN roles
                ON usuarios.rol_id = roles.id

            ORDER BY usuarios.nombre;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(query)

        usuarios = []

        if resultados:

            for usuario in resultados:

                usuarios.append(
                    cls(usuario)
                )

        return usuarios


    # =====================================================
    # OBTENER USUARIO POR ID
    # =====================================================
    @classmethod
    def get_by_id(cls, usuario_id):

        query = """
            SELECT
                usuarios.*,
                roles.nombre AS tipo_usuario

            FROM usuarios

            JOIN roles
                ON usuarios.rol_id = roles.id

            WHERE usuarios.id = %(id)s;
        """

        datos = {
            "id": usuario_id
        }

        resultado = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )

        if resultado:

            return cls(
                resultado[0]
            )

        return None


    # =====================================================
    # BUSCAR USUARIO POR CORREO
    # LOGIN / REGISTRO
    # =====================================================
    @classmethod
    def get_by_email(cls, correo):

        query = """
            SELECT
                usuarios.*,
                roles.nombre AS tipo_usuario

            FROM usuarios

            JOIN roles
                ON usuarios.rol_id = roles.id

            WHERE LOWER(usuarios.correo) = %(correo)s

            LIMIT 1;
        """

        datos = {
            "correo": correo.lower()
        }

        resultado = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )

        if resultado:

            return cls(
                resultado[0]
            )

        return None


    # =====================================================
    # CREAR USUARIO
    # =====================================================
    @classmethod
    def crear(cls, data):

        query = """
            INSERT INTO usuarios (
                nombre,
                apellido,
                correo,
                password,
                matricula,
                rol_id,
                created_at,
                updated_at
            )

            VALUES (
                %(nombre)s,
                %(apellido)s,
                %(correo)s,
                %(password)s,
                %(matricula)s,
                %(rol_id)s,
                NOW(),
                NOW()
            );
        """

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )


    # =====================================================
    # ACTUALIZAR USUARIO
    # =====================================================
    @classmethod
    def actualizar(cls, data):

        query = """
            UPDATE usuarios

            SET
                nombre = %(nombre)s,
                apellido = %(apellido)s,
                correo = %(correo)s,
                matricula = %(matricula)s,
                rol_id = %(rol_id)s,
                updated_at = NOW()

            WHERE id = %(id)s;
        """

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )


    # =====================================================
    # ELIMINAR USUARIO
    # =====================================================
    @classmethod
    def eliminar(cls, usuario_id):

        query = """
            DELETE FROM usuarios
            WHERE id = %(id)s;
        """

        datos = {
            "id": usuario_id
        }

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )