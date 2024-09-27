from werkzeug.security import check_password_hash
from flask_login import UserMixin


class Usuario(UserMixin):


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
    

