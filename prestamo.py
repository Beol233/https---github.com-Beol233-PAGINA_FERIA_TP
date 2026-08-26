from config import DB_NAME
from mysqlconnection import connectToMySQL


class Prestamo:

    def __init__(self, data):

        self.id = data["id"]
        self.usuario_id = data["usuario_id"]
        self.libro_id = data["libro_id"]

        self.fecha_prestamo = data["fecha_prestamo"]
        self.fecha_dev_esperada = data["fecha_dev_esperada"]
        self.fecha_devolucion = data["fecha_devolucion"]

        self.estado = data["estado"]

        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

        # Estos datos aparecen cuando hacemos JOIN
        self.usuario = data.get("usuario")
        self.correo = data.get("correo")
        self.titulo = data.get("titulo")
        self.autor = data.get("autor")


    # =====================================================
    # OBTENER TODOS LOS PRÉSTAMOS
    # =====================================================
    @classmethod
    def get_all(cls):

        query = """
            SELECT
                prestamos.*,

                CONCAT(
                    usuarios.nombre,
                    ' ',
                    usuarios.apellido
                ) AS usuario,

                usuarios.correo,

                libros.titulo,
                libros.autor

            FROM prestamos

            JOIN usuarios
                ON prestamos.usuario_id = usuarios.id

            JOIN libros
                ON prestamos.libro_id = libros.id

            ORDER BY prestamos.fecha_prestamo DESC;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(query)

        prestamos = []

        if resultados:

            for prestamo in resultados:

                prestamos.append(
                    cls(prestamo)
                )

        return prestamos


    # =====================================================
    # OBTENER PRÉSTAMOS DE UN USUARIO
    # =====================================================
    @classmethod
    def get_by_usuario(cls, usuario_id):

        query = """
            SELECT
                prestamos.*,

                libros.titulo,
                libros.autor

            FROM prestamos

            JOIN libros
                ON prestamos.libro_id = libros.id

            WHERE prestamos.usuario_id = %(usuario_id)s

            ORDER BY prestamos.fecha_prestamo DESC;
        """

        datos = {
            "usuario_id": usuario_id
        }

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )

        prestamos = []

        if resultados:

            for prestamo in resultados:

                prestamos.append(
                    cls(prestamo)
                )

        return prestamos


    # =====================================================
    # CREAR PRÉSTAMO
    # =====================================================
    @classmethod
    def crear(cls, data):

        usuario_id = data["usuario_id"]
        libro_id = data["libro_id"]
        fecha_dev_esperada = data["fecha_dev_esperada"]

        # -----------------------------------------
        # Comprobar que el libro existe
        # -----------------------------------------

        query_libro = """
            SELECT
                id,
                titulo,
                cantidad_disponible

            FROM libros

            WHERE id = %(libro_id)s;
        """

        libro = connectToMySQL(
            DB_NAME
        ).query_db(
            query_libro,
            {
                "libro_id": libro_id
            }
        )

        if not libro:

            return {
                "ok": False,
                "mensaje": "El libro no existe."
            }

        # -----------------------------------------
        # Comprobar disponibilidad
        # -----------------------------------------

        if libro[0]["cantidad_disponible"] <= 0:

            return {
                "ok": False,
                "mensaje": "No quedan ejemplares disponibles."
            }

        # -----------------------------------------
        # Evitar prestar dos veces el mismo libro
        # al mismo usuario
        # -----------------------------------------

        query_existente = """
            SELECT id

            FROM prestamos

            WHERE usuario_id = %(usuario_id)s
              AND libro_id = %(libro_id)s
              AND estado IN ('activo', 'atrasado')

            LIMIT 1;
        """

        existente = connectToMySQL(
            DB_NAME
        ).query_db(
            query_existente,
            {
                "usuario_id": usuario_id,
                "libro_id": libro_id
            }
        )

        if existente:

            return {
                "ok": False,
                "mensaje": "Este usuario ya tiene este libro prestado."
            }

        # -----------------------------------------
        # Crear préstamo
        # -----------------------------------------

        query_prestamo = """
            INSERT INTO prestamos (
                usuario_id,
                libro_id,
                fecha_prestamo,
                fecha_dev_esperada,
                fecha_devolucion,
                estado,
                created_at,
                updated_at
            )

            VALUES (
                %(usuario_id)s,
                %(libro_id)s,
                NOW(),
                %(fecha_dev_esperada)s,
                NULL,
                'activo',
                NOW(),
                NOW()
            );
        """

        prestamo_id = connectToMySQL(
            DB_NAME
        ).query_db(
            query_prestamo,
            {
                "usuario_id": usuario_id,
                "libro_id": libro_id,
                "fecha_dev_esperada": fecha_dev_esperada
            }
        )

        if prestamo_id is False:

            return {
                "ok": False,
                "mensaje": "No se pudo realizar el préstamo."
            }

        # -----------------------------------------
        # Restar una copia disponible
        # -----------------------------------------

        query_stock = """
            UPDATE libros

            SET cantidad_disponible =
                cantidad_disponible - 1

            WHERE id = %(libro_id)s
              AND cantidad_disponible > 0;
        """

        resultado_stock = connectToMySQL(
            DB_NAME
        ).query_db(
            query_stock,
            {
                "libro_id": libro_id
            }
        )

        if resultado_stock is False or resultado_stock == 0:

            # Si por algún motivo no se pudo restar el stock,
            # eliminamos el préstamo recién creado.

            query_cancelar = """
                DELETE FROM prestamos
                WHERE id = %(prestamo_id)s;
            """

            connectToMySQL(
                DB_NAME
            ).query_db(
                query_cancelar,
                {
                    "prestamo_id": prestamo_id
                }
            )

            return {
                "ok": False,
                "mensaje": "No se pudo actualizar el stock del libro."
            }

        return {
            "ok": True,
            "id": prestamo_id
        }


    # =====================================================
    # DEVOLVER LIBRO
    # =====================================================
    @classmethod
    def devolver(cls, prestamo_id):

        # -----------------------------------------
        # Buscar préstamo
        # -----------------------------------------

        query = """
            SELECT
                id,
                libro_id,
                estado

            FROM prestamos

            WHERE id = %(id)s;
        """

        resultado = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            {
                "id": prestamo_id
            }
        )

        if not resultado:

            return {
                "ok": False,
                "mensaje": "El préstamo no existe."
            }

        prestamo = resultado[0]

        # -----------------------------------------
        # Comprobar si ya fue devuelto
        # -----------------------------------------

        if prestamo["estado"] == "devuelto":

            return {
                "ok": False,
                "mensaje": "Este libro ya fue devuelto."
            }

        # -----------------------------------------
        # Marcar préstamo como devuelto
        # -----------------------------------------

        query_devolver = """
            UPDATE prestamos

            SET
                estado = 'devuelto',
                fecha_devolucion = NOW(),
                updated_at = NOW()

            WHERE id = %(id)s;
        """

        resultado_devolucion = connectToMySQL(
            DB_NAME
        ).query_db(
            query_devolver,
            {
                "id": prestamo_id
            }
        )

        if resultado_devolucion is False:

            return {
                "ok": False,
                "mensaje": "No se pudo registrar la devolución."
            }

        # -----------------------------------------
        # Sumar nuevamente el stock
        # -----------------------------------------

        query_stock = """
            UPDATE libros

            SET cantidad_disponible =
                cantidad_disponible + 1

            WHERE id = %(libro_id)s;
        """

        resultado_stock = connectToMySQL(
            DB_NAME
        ).query_db(
            query_stock,
            {
                "libro_id": prestamo["libro_id"]
            }
        )

        if resultado_stock is False:

            return {
                "ok": False,
                "mensaje": "Se registró la devolución, pero hubo un problema actualizando el stock."
            }

        return {
            "ok": True
        }


    # =====================================================
    # ACTUALIZAR PRÉSTAMOS ATRASADOS
    # =====================================================
    @classmethod
    def actualizar_atrasados(cls):

        query = """
            UPDATE prestamos

            SET
                estado = 'atrasado',
                updated_at = NOW()

            WHERE estado = 'activo'
              AND fecha_dev_esperada < NOW();
        """

        return connectToMySQL(
            DB_NAME
        ).query_db(query)