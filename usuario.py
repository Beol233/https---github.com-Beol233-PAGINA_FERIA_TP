from mysqlconnection import connectToMySQL

class Usuario:

    def __init__(self,data ):
        self.id = data['id']
        self.nombre = data['nombre']
        self.apellido = data['apellido']
        self.correo = data['correo']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.rol_id = data['rol_id']

def get_all(cls):
       query = "SELECT * FROM Usuario;"

       # Llamamos a función connectToMySQL con el esquema al que te diriges
       resultados = connectToMySQL('biblioteca_db').query_db(query)

       # Creamos una lista vacía para agregar nuestras instancias de mascota
       usuario = []

       # Iteramos sobre los resultados de la base de datos y crear instancias de mascota con cls
       for usuario in resultados:
           usuario.append( cls(usuario) )
       return usuario