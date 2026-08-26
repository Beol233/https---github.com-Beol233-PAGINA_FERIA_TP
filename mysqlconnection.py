import pymysql.cursors


class MySQLConnection:

    def __init__(self, db):

        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="root",
            db=db,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )


    # =====================================================
    # EJECUTAR CONSULTAS
    # =====================================================
    def query_db(self, query, data=None):

        try:

            with self.connection.cursor() as cursor:

                # Mostrar consulta en consola solamente
                consulta_mostrada = cursor.mogrify(
                    query,
                    data
                )

                print(
                    "Running Query:",
                    consulta_mostrada
                )

                # Ejecutar la consulta ORIGINAL
                cursor.execute(
                    query,
                    data
                )

                tipo_query = query.strip().lower()


                # ==========================================
                # SELECT
                # ==========================================
                if tipo_query.startswith("select"):

                    resultado = cursor.fetchall()

                    return resultado


                # ==========================================
                # INSERT
                # ==========================================
                elif tipo_query.startswith("insert"):

                    self.connection.commit()

                    # Devuelve ID del elemento creado
                    return cursor.lastrowid


                # ==========================================
                # UPDATE / DELETE
                # ==========================================
                elif (
                    tipo_query.startswith("update")
                    or tipo_query.startswith("delete")
                ):

                    self.connection.commit()

                    # Devuelve número de filas modificadas
                    return cursor.rowcount


                # ==========================================
                # OTRAS CONSULTAS
                # ==========================================
                else:

                    self.connection.commit()

                    return cursor.rowcount


        except Exception as e:

            self.connection.rollback()

            print(
                "Something went wrong:",
                e
            )

            return False


        finally:

            self.connection.close()


# =========================================================
# CREAR CONEXIÓN A MYSQL
# =========================================================
def connectToMySQL(db):

    return MySQLConnection(db)