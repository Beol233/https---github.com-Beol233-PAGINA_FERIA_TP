from config import DB_NAME
from mysqlconnection import connectToMySQL

class Libro:
    def __init__(self,data):
        self.id = data["id"]
        self.isbn = data["isbn"]
        self.titulo = data["titulo"]
        self.autor = data["autor"]
        self.editorial = data["editorial"] 
        self.anio =  data["anio"]
        self.cantidad_total = data["cantidad_total"]
        self.cantidad_disponible = data["cantidad_disponible"]
        self.categoria_id = data["categoria_id"]
        self.portada_url = data["portada_url"] 
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM libros ORDER BY titulo;"

        #llamamos a funcion connectToMysql
        resultados = connectToMySQL(DB_NAME).query_db(query)
        #Creamos lista vacida 
        libros = []
        #Iteramos sobre los resultados de la base de datos
        
        if resultados:
            for libro in resultados:
                libros.append(cls(libro))
            
        return libros   

    @classmethod
    def get_by_id(cls, libro_id):

        query = """
            SELECT *
            FROM libros
            WHERE id = %(id)s;
        """

        datos = {
            "id": libro_id
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

        datos = {
            "texto": f"%{texto}%"
        }

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )

        libros = []

        if resultados:

            for libro in resultados:
                libros.append(
                    cls(libro)
                )

        return libros

    @classmethod
    def buscar_por_codigo(cls, codigo):

        query = """
            SELECT DISTINCT
                libros.*

            FROM libros

            LEFT JOIN codigo_de_barras
                ON codigo_de_barras.libro_id = libros.id

            WHERE libros.isbn = %(codigo)s
               OR codigo_de_barras.codigo = %(codigo)s

            LIMIT 1;
        """

        datos = {
            "codigo": codigo
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
    @classmethod
    def actualizar(cls, data):

        # Primero obtenemos el libro actual
        libro_actual = cls.get_by_id(
            data["id"]
        )

        if not libro_actual:
            return False

        # Cantidad que actualmente está prestada
        cantidad_prestada = (
            libro_actual.cantidad_total
            - libro_actual.cantidad_disponible
        )

        nueva_cantidad_total = int(
            data["cantidad_total"]
        )

        # No permitir que el total quede menor
        # a la cantidad actualmente prestada
        if nueva_cantidad_total < cantidad_prestada:

            return False

        nueva_disponible = (
            nueva_cantidad_total
            - cantidad_prestada
        )

        datos = {
            "id": data["id"],
            "isbn": data["isbn"],
            "titulo": data["titulo"],
            "autor": data["autor"],
            "editorial": data["editorial"],
            "anio": data["anio"],
            "cantidad_total": nueva_cantidad_total,
            "cantidad_disponible": nueva_disponible,
            "portada_url": data["portada_url"],
            "categoria_id": data["categoria_id"]
        }

        query = """
            UPDATE libros

            SET
                isbn = %(isbn)s,
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
            datos
        )

    @classmethod
    def eliminar(cls, libro_id):

        query = """
            DELETE FROM libros
            WHERE id = %(id)s;
        """

        datos = {
            "id": libro_id
        }

        return connectToMySQL(
            DB_NAME
        ).query_db(
            query,
            datos
        )