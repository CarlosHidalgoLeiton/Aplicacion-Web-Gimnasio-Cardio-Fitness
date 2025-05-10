
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Membership(db.Model):
    __tablename__ = 'membresia'

    id  = db.Column(db.Integer, primary_key=True, key='id', name='ID_Membresia')
    Name  = db.Column(db.String(30), nullable=False, unique=True, key='Name', name='Nombre')
    Description = db.Column(db.String(30), nullable=True, key='Description', name='Descripcion')
    Price = db.Column(db.Numeric(10,2), nullable=False, key='Price', name='Precio')
    Time = db.Column(db.Integer, nullable=True, key='Time', name='Duracion_Dias')  
    State = db.Column(db.Boolean, nullable=False, key='State', name='Estado')
