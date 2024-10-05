from .entities.User import User

class ModelUser:

    @classmethod
    def login(cls, user, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Contrasena, Estado, Rol FROM Usuario WHERE Cedula = %s"
            cursor.execute(sql, (user.DocumentId))
            row = cursor.fetchone()
            if row is not None:
                if row[3] != 0:
                    if User.verifyPassword(row[2], user.Password):
                        return User(row[0], row[1], row[2], None, row[4])
                    else:
                        return "Password"
                else:
                    return 'Inactive'
            else:
                return "Invalid User"
        except BaseException as ex:
            print(f"Error en ModelUser login: {ex}")
            return "DataBase"
        except Exception as ex:
            print(f"Error en ModelUser login: {ex}")
            return None


    @classmethod
    def get_by_id(cls, conexion, id):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Rol, Correo FROM Usuario WHERE ID_Usuario = %s"
            cursor.execute(sql, (id))
            row = cursor.fetchone()
            print(row)
            if row is not None:
                return User(row[0], row[1], None, None, row[2],None,row[3])
            return None
        except Exception as ex:
            
            print(f"Error en ModelUser en get_by_id: {ex}")
            return None

    @classmethod
    def insertUser(cls, user, conexion):
        try:
            cursor = conexion.cursor()

            hashed_password = user.Password  

            sql = """INSERT INTO USUARIO 
                    (`Cedula`, `Contrasena`, `Estado`, `Rol`, `FechaCreacion`, `Correo`) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (user.DocumentId, hashed_password, user.State, user.role, user.CreationDate, user.Email))

            conexion.commit()
            if cursor.rowcount > 0:
                print(f"Usuario {user.DocumentId} creado exitosamente.")
            else:
                print("No se pudo crear el usuario.")
                return None  

        except Exception as ex:
            print(f"Error al crear usuario: {ex}")
            return None  
        finally:
            cursor.close()


    @classmethod
    def get_Users(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Estado, Rol FROM Usuario"
            cursor.execute(sql)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                user = User(row[0], row[1], None ,row[2], row[3])
                users.append(user)
            return users
        except Exception as ex:
            print(f"Error en get_Users: {ex}")
            return []
     

    @classmethod
    def get_User(cls, conexion, documentId):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Estado, Rol, Correo FROM Usuario WHERE Cedula = %s"
            cursor.execute(sql, (documentId,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2], row[3], None, row[4])  
            return None
        except Exception as ex:
            print(f"Error en get_User: {ex}")
            return None