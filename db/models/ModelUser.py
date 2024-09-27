from .entities.User import Usuario

class ModelUser:

    @classmethod
    def login(cls, user, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Contrasena, Estado FROM Usuario WHERE Cedula = %s"
            cursor.execute(sql, (user.Cedula))
            row = cursor.fetchone()
            if row is not None:
                if row[3] != 0:
                    if Usuario.verifyPassword(row[2], user.Contrasena):
                        return Usuario(row[0], row[1], row[2])
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
            sql = "SELECT ID_Usuario, Cedula, Rol FROM Usuario WHERE Cedula = %s"
            cursor.execute(sql, (id))
            row = cursor.fetchone()
            if row is not None:
                return Usuario(row[0], row[1], None, None, row[2])
            return None
        except Exception as ex:
            print(f"Error en login: {ex}")
            return None