from mysqlconnection import connectToMySQL

class Usuario:

    def __init__(self,data ):
        self.id = data['id']
        self.nombre = data['nombre']
        