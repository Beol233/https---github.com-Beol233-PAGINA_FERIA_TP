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

     