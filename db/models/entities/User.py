from werkzeug.security import check_password_hash
from flask_login import UserMixin


class Usuario(UserMixin):

    #Aunque en la base de datos salga con otro nombre el id, acá hay que colocarlo como id para que el flask_login lo reconozca
    def __init__(self, id = None, Cedula = None, Contrasena = None, Estado = None, Rol = None, FechaCreacion = None, Correo = None) -> None:
        self.id = id
        self.Cedula = Cedula
        self.Contrasena = Contrasena
        self.Estado = Estado
        self.Rol = Rol
        self.FechaCreacion = FechaCreacion
        self.Correo = Correo

    @classmethod
    def verifyPassword(self, hash_password, password):
        return check_password_hash(hash_password, password)
    

