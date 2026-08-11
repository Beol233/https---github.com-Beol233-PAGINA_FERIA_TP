from mysqlconnection import connectToMySQL

class Prestamos:
   def __init__( self , data ):
       self.id = data['id']
       self.usuario_id = data['usuario_id']
       self.libro_id = data['libro_id']
       self.created_at = data['created_at']
       self.updated_at = data['updated_at']
       self.fecha_dev_esperada = data['fecha_dev_esperada']

   @classmethod                                             
   def get_all(cls):
       query = "SELECT * FROM prestamo;"

       resultados = connectToMySQL('primera_flask').query_db(query)

       prestamo = []

       for prestamo in resultados:
           prestamo.append( cls(prestamo) )
       return prestamo