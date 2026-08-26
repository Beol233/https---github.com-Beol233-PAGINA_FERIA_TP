from config import DB_NAME
from mysqlconnection import connectToMySQL


class Categoria:

    def __init__(self, data):
        self.id = data["id"]
        self.nombre = data["nombre"]
        self.descripcion = data["descripcion"]
        self.updated_at = data["updated_at"]
        self.created_at = data["created_at"]


    @classmethod
    def get_all(cls):

        query = """
            SELECT *
            FROM categorias
            ORDER BY nombre;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(query)

        categorias = []

        if resultados:

            for categoria in resultados:

                categorias.append(
                    cls(categoria)
                )

        return categorias