from config import DB_NAME
from mysqlconnection import connectToMySQL


class Reserva:

    def __init__(self, data):

        self.id = data["id"]
        self.usuario_id = data["usuario_id"]
        self.libro_id = data["libro_id"]

        self.fecha_reserva = data["fecha_reserva"]
        self.estado = data["estado"]

        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")

        # Aparecen cuando hacemos JOIN
        self.usuario = data.get("usuario")
        self.correo = data.get("correo")
        self.titulo = data.get("titulo")
        self.autor = data.get("autor")


    # =====================================================
    # CREAR RESERVA
    # =====================================================

    @classmethod
    def crear(cls, data):

        query = """
            INSERT INTO reservas (
                usuario_id,
                libro_id,
                fecha_reserva,
                estado,
                created_at,
                updated_at
            )

            VALUES (
                %(usuario_id)s,
                %(libro_id)s,
                NOW(),
                'pendiente',
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
    # COMPROBAR SI YA RESERVÓ EL LIBRO
    # =====================================================

    @classmethod
    def get_pendiente(cls, usuario_id, libro_id):

        query = """
            SELECT *
            FROM reservas

            WHERE usuario_id = %(usuario_id)s
              AND libro_id = %(libro_id)s
              AND estado = 'pendiente'

            LIMIT 1;
        """

        datos = {
            "usuario_id": usuario_id,
            "libro_id": libro_id
        }

        resultado = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )

        if resultado:
            return cls(resultado[0])

        return None


    # =====================================================
    # OBTENER TODAS
    # PARA EL PANEL DEL ADMINISTRADOR
    # =====================================================

    @classmethod
    def get_all(cls):

        query = """
            SELECT
                reservas.*,

                CONCAT(
                    usuarios.nombre,
                    ' ',
                    usuarios.apellido
                ) AS usuario,

                usuarios.correo,

                libros.titulo,
                libros.autor

            FROM reservas

            JOIN usuarios
                ON reservas.usuario_id = usuarios.id

            JOIN libros
                ON reservas.libro_id = libros.id

            ORDER BY reservas.fecha_reserva DESC;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(query)

        reservas = []

        if resultados:

            for reserva in resultados:
                reservas.append(
                    cls(reserva)
                )

        return reservas

    # =====================================================
# OBTENER RESERVA POR ID
# =====================================================

    @classmethod
    def get_by_id(cls, reserva_id):

        query = """
            SELECT
                reservas.*,

                CONCAT(
                    usuarios.nombre,
                    ' ',
                    usuarios.apellido
                ) AS usuario,

                usuarios.correo,

                libros.titulo,
                libros.autor

            FROM reservas

            JOIN usuarios
                ON reservas.usuario_id = usuarios.id

            JOIN libros
                ON reservas.libro_id = libros.id

            WHERE reservas.id = %(id)s

            LIMIT 1;
        """

        resultado = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            {
                "id": reserva_id
            }
        )

        if resultado:
            return cls(resultado[0])

        return None


# =====================================================
# OBTENER RESERVAS PENDIENTES
# =====================================================

    @classmethod
    def get_pendientes(cls):

        query = """
            SELECT
                reservas.*,

                CONCAT(
                    usuarios.nombre,
                    ' ',
                    usuarios.apellido
                ) AS usuario,

                usuarios.correo,

                libros.titulo,
                libros.autor

            FROM reservas

            JOIN usuarios
                ON reservas.usuario_id = usuarios.id

            JOIN libros
                ON reservas.libro_id = libros.id

            WHERE reservas.estado = 'pendiente'

            ORDER BY reservas.fecha_reserva ASC;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(query)

        reservas = []

        if resultados:

            for reserva in resultados:

                reservas.append(
                    cls(reserva)
                )

        return reservas


# =====================================================
# CAMBIAR ESTADO
# =====================================================

    @classmethod
    def cambiar_estado(cls, reserva_id, estado):

        query = """
            UPDATE reservas

            SET
                estado = %(estado)s,
                updated_at = NOW()

            WHERE id = %(id)s;
        """

        datos = {
            "id": reserva_id,
            "estado": estado
        }

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )