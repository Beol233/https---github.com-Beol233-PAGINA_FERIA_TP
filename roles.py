from config import DB_NAME
from mysqlconnection import connectToMySQL


class Rol:

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
            FROM roles
            ORDER BY nombre;
        """

        resultados = connectToMySQL(
            DB_NAME
        ).query_db(query)

        roles = []

        if resultados:

            for rol in resultados:

                roles.append(
                    cls(rol)
                )

        return roles


    @classmethod
    def get_by_nombre(cls, nombre):

        query = """
            SELECT *
            FROM roles
            WHERE nombre = %(nombre)s
            LIMIT 1;
        """

        datos = {
            "nombre": nombre
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