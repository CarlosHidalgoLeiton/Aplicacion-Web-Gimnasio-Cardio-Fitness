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
                    return 'Inactivo'
            return None
        except Exception as ex:
            print(f"Error en login: {ex}")
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
            print(f"Error en login: {ex}")
            return None

    @classmethod
    def insertUser(cls, user, conexion):
        try:
            cursor = conexion.cursor()

            hashed_password = user.Password  

            sql = """INSERT INTO USUARIO 
                    (`Cedula`, `Contrasena`, `Estado`, `Rol`, `FechaCreacion`, `Correo`) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (user.DocumentId, hashed_password, user.State, user.Role, user.CreationDate, user.Email))

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