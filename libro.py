from config import DB_NAME
from mysqlconnection import connectToMySQL


class Libro:

    def __init__(self, data):
        self.id = data["id"]
        self.isbn = data.get("isbn")
        self.titulo = data.get("titulo")
        self.autor = data.get("autor")
        self.editorial = data.get("editorial")
        self.anio = data.get("anio")
        self.cantidad_total = data.get("cantidad_total")
        self.cantidad_disponible = data.get("cantidad_disponible")
        self.portada_url = data.get("portada_url")
        self.categoria_id = data.get("categoria_id")
        self.created_at = data.get("created_at")
        self.updated_at = data.get("updated_at")


    # ==========================================
    # OBTENER TODOS LOS LIBROS
    # ==========================================
    @classmethod
    def get_all(cls):

        query = """
            SELECT *
            FROM libros
            ORDER BY titulo;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(query)

        libros = []

        if resultados:
            for libro in resultados:
                libros.append(cls(libro))

        return libros


    # ==========================================
    # OBTENER LIBRO POR ID
    # ==========================================
    @classmethod
    def get_by_id(cls, libro_id):

        query = """
            SELECT *
            FROM libros
            WHERE id = %(id)s;
        """

        data = {
            "id": libro_id
        }

        resultado = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )

        if resultado:
            return cls(resultado[0])

        return None


    # ==========================================
    # BUSCAR LIBROS
    # ==========================================
    @classmethod
    def buscar(cls, texto):

        query = """
            SELECT *
            FROM libros
            WHERE titulo LIKE %(texto)s
               OR autor LIKE %(texto)s
               OR editorial LIKE %(texto)s
               OR isbn LIKE %(texto)s
            ORDER BY titulo;
        """

        data = {
            "texto": f"%{texto}%"
        }

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )

        libros = []

        if resultados:
            for libro in resultados:
                libros.append(cls(libro))

        return libros


    # ==========================================
    # BUSCAR POR CÓDIGO DE BARRAS / ISBN
    # ==========================================
    @classmethod
    def buscar_por_codigo(cls, codigo):

        query = """
            SELECT DISTINCT libros.*
            FROM libros

            LEFT JOIN codigo_de_barras
                ON codigo_de_barras.libro_id = libros.id

            WHERE libros.isbn = %(codigo)s
               OR codigo_de_barras.codigo = %(codigo)s

            LIMIT 1;
        """

        data = {
            "codigo": codigo
        }

        resultado = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )

        if resultado:
            return cls(resultado[0])

        return None


    # ==========================================
    # FILTRAR LIBROS
    # ==========================================
    @classmethod
    def filtrar(
        cls,
        texto="",
        generos=None,
        disponibilidad="todos"
    ):

        if generos is None:
            generos = []

        query = """
            SELECT libros.*
            FROM libros

            JOIN categorias
                ON libros.categoria_id = categorias.id

            WHERE 1 = 1
        """

        datos = {}

        # --------------------------
        # Buscar por texto
        # --------------------------
        if texto:

            query += """
                AND (
                    libros.titulo LIKE %(texto)s
                    OR libros.autor LIKE %(texto)s
                    OR libros.editorial LIKE %(texto)s
                    OR libros.isbn LIKE %(texto)s
                )
            """

            datos["texto"] = f"%{texto}%"

        # --------------------------
        # Filtrar por género
        # --------------------------
        if generos:

            placeholders = []

            for i, genero in enumerate(generos):

                clave = f"genero_{i}"

                placeholders.append(
                    f"%({clave})s"
                )

                datos[clave] = genero

            query += " AND categorias.nombre IN ("
            query += ", ".join(placeholders)
            query += ")"

        # --------------------------
        # Filtrar disponibilidad
        # --------------------------
        if disponibilidad == "disponible":

            query += """
                AND libros.cantidad_disponible > 0
            """

        elif disponibilidad == "prestado":

            query += """
                AND libros.cantidad_disponible = 0
            """

        query += """
            ORDER BY libros.titulo;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )

        libros = []

        if resultados:
            for libro in resultados:
                libros.append(cls(libro))

        return libros


    # ==========================================
    # CREAR LIBRO
    # ==========================================
    @classmethod
    def crear(cls, data):

        query = """
            INSERT INTO libros (
                isbn,
                titulo,
                autor,
                editorial,
                anio,
                cantidad_total,
                cantidad_disponible,
                portada_url,
                categoria_id
            )

            VALUES (
                %(isbn)s,
                %(titulo)s,
                %(autor)s,
                %(editorial)s,
                %(anio)s,
                %(cantidad_total)s,
                %(cantidad_total)s,
                %(portada_url)s,
                %(categoria_id)s
            );
        """

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )


    # ==========================================
    # ACTUALIZAR LIBRO
    # ==========================================
    @classmethod
    def actualizar(cls, data):

        libro_actual = cls.get_by_id(
            data["id"]
        )

        if not libro_actual:
            return False

        # Cantidad actualmente prestada
        prestados = (
            libro_actual.cantidad_total
            - libro_actual.cantidad_disponible
        )

        nueva_cantidad_total = int(
            data["cantidad_total"]
        )

        # No permitir tener menos ejemplares
        # que los que actualmente están prestados
        if nueva_cantidad_total < prestados:
            return False

        nueva_disponible = (
            nueva_cantidad_total
            - prestados
        )

        data["cantidad_disponible"] = (
            nueva_disponible
        )

        query = """
            UPDATE libros

            SET isbn = %(isbn)s,
                titulo = %(titulo)s,
                autor = %(autor)s,
                editorial = %(editorial)s,
                anio = %(anio)s,
                cantidad_total = %(cantidad_total)s,
                cantidad_disponible = %(cantidad_disponible)s,
                portada_url = %(portada_url)s,
                categoria_id = %(categoria_id)s

            WHERE id = %(id)s;
        """

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )


    # ==========================================
    # ELIMINAR LIBRO
    # ==========================================
    @classmethod
    def eliminar(cls, libro_id):

        query = """
            DELETE FROM libros
            WHERE id = %(id)s;
        """

        data = {
            "id": libro_id
        }

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            data
        )