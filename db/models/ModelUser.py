from .entities.User import Usuario

class ModelUser:

    @classmethod
    def login(cls, user, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Contrasena, Estado, Rol, FechaCreacion, Correo FROM Usuario WHERE Cedula = %s"
            cursor.execute(sql, (user.Cedula,))
            row = cursor.fetchone()
            if row is not None:
                if Usuario.verifyPassword(row[2], user.Contrasena):
                    return Usuario(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
            return None
        except Exception as ex:
            print(f"Error en login: {ex}")
            return None