from mysqlconnection import connectToMySQL

class libro:
    def __init__(self,data):
        self.id = data[id]
        self.isbn = data["isbn"]
        self.titulo = data["titulo"]
        self.autor = data["autor"]
        self.editorial = data["editorial"] 
        self.anio =  data["anio"]
        self.cantidad_total = data["cantidad_total"]
        self.cantidad_disponible = data["cantidad_disponible"]
        self.categoria_id = data["categoria_id"]
        self.portada = data["portada"]  
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM libros"
        #llamamos a funcion connectToMysql
        resultados = connectToMySQL("biblioteca_db").query_db(query)
        #Creamos lista vacida 
        libros = []
        #Iteramos sobre los resultados de la base de datos
        for libros in resultados:
            libros.append(cls(libros))
            
        return libros   