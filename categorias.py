from mysqlconnection import connectToMySQL

class Categorias:

    def __init__(self,data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.updated_at = data['updated_at']
        self.created_at = data['created_at']

@classmethod
def get_all(cls):
    query = "SELECT * FROM categorias;"

    resultados = connectToMySQL('biblioteca_db').query_db(query)

    Categorias = []

    for categoria in resultados:
        Categorias.append(cls(categoria))

    return Categorias

