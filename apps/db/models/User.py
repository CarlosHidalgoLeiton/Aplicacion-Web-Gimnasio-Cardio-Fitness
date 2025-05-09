from werkzeug.security import check_password_hash, generate_password_hash
from apps.db.db import db  # Importa la instancia de SQLAlchemy
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    id = db.Column("ID_Usuario", db.Integer, primary_key=True)
    DocumentId = db.Column("Cedula", db.String(60), nullable=False)
    Password = db.Column("Contrasena", db.String(102), nullable=False)
    State = db.Column("Estado", db.SmallInteger, nullable=False, default=1)
    role = db.Column("Rol", db.String(50), nullable=False)
    CreationDate = db.Column("FechaCreacion", db.Date, nullable=False)
    Email = db.Column("Correo", db.String(150), nullable=False)

    def get_id(self):
        return str(self.id)

    @classmethod
    def verifyPassword(self, hash_password, password):
        return check_password_hash(hash_password, password)
    
    @classmethod
    def generate_password_hash(self, password):
        return generate_password_hash(password)