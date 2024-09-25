from .entities.User import Usuario

class ModelUser():

    @classmethod
    def login(self, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID_Usuario, Cedula, Contrasena, Estado, Rol, FechaCreacion, Correo FROM Usuario WHERE Cedula = '{}'""".format(user.Cedula)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                user = Usuario(row[0], row[1], Usuario.hashPassword(row[2], user.contrasena), row[3], row[4], row[5], row[6])
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_Usuario, Cedula, FROM Usuario WHERE ID_Usuario = {}".format(id)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                return Usuario(row[0], row[1], None, row[2])
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

