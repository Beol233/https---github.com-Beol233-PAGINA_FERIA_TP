from mysqlconnection import connectToMySQL
class roles:
    def __init__(self,data)
    self.id = data["id"]
    self.nombre = data["nombre"]
    self.descripcion = data["descripcion"]
    self.updated_at = data["updated_at"]
    self.created_at = data["created_at"]
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM roles"
        
        resultados = connectToMySQL("biblioteca_db").query_db(query)
        
        roles = []
        
        for roles in roles:
            roles.append(cls(roles))
        return roles
        
        