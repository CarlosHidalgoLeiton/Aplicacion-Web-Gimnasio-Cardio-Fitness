from werkzeug.security import check_password_hash
from flask_login import UserMixin


class Usuario(UserMixin):


    def __init__(self, ID_Usuario, Cedula, Contrasena, Estado, Rol, FechaCreacion, Correo) -> None:
        self.ID_Usuario = ID_Usuario
        self.Cedula = Cedula
        self.Contrasena = Contrasena
        self.Estado = Estado
        self.Rol = Rol
        self.FechaCreacion = FechaCreacion
        self.Correo = Correo

    @classmethod
    def hashPassword(self, hash_password, password):
        return check_password_hash(hash_password, password)
