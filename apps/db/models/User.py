from werkzeug.security import check_password_hash, generate_password_hash
from apps.db.db import db  # Importa la instancia de SQLAlchemy
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    ID_Usuario = db.Column(db.Integer, primary_key=True)
    Cedula = db.Column(db.String(60), nullable=False)
    Contrasena = db.Column(db.String(102), nullable=False)
    Estado = db.Column(db.SmallInteger, nullable=False, default=1)
    Rol = db.Column(db.String(50), nullable=False)
    FechaCreacion = db.Column(db.Date, nullable=False)
    Correo = db.Column(db.String(150), nullable=False)

    # def __init__(self, id = None, DocumentId = None, Password = None, State = None, role = None, CreationDate = None, Email = None) -> None:
    #     self.id = id
    #     self.DocumentId = DocumentId
    #     self.Password = Password
    #     self.State = State
    #     self.role = role
    #     self.CreationDate = CreationDate
    #     self.Email = Email

    def get_id(self):
        return str(self.ID_Usuario)

    @classmethod
    def verifyPassword(self, hash_password, password):
        return check_password_hash(hash_password, password)
    
    @classmethod
    def generate_password_hash(self, password):
        return generate_password_hash(password)