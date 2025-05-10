from werkzeug.security import check_password_hash, generate_password_hash
from apps.db.db import db  # Importa la instancia de SQLAlchemy
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'Usuario'
    id = db.Column(db.Integer, primary_key=True, key='id', name='ID_Usuario')
    DocumentId = db.Column(db.String(60), nullable=False, key='DocumentId', name='Cedula')
    Password = db.Column(db.String(102), nullable=False, key='Password', name='Contrasena')
    State = db.Column(db.SmallInteger, nullable=False, default=1, key='State', name='Estado')
    role = db.Column(db.String(50), nullable=False, key='role', name='Rol')
    CreationDate = db.Column(db.Date, nullable=False, key='CreationDate', name='FechaCreacion')
    Email = db.Column(db.String(150), nullable=False, key='Email', name="Correo")

    def get_id(self):
        return str(self.id)

    @classmethod
    def verifyPassword(self, hash_password, password):
        return check_password_hash(hash_password, password)
    
    @classmethod
    def generate_password_hash(self, password):
        return generate_password_hash(password)