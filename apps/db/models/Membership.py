
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Membership(db.Model):
    __tablename__ = 'membresia'

    ID_Membresia  = db.Column(db.Integer(11), primary_key=True)
    Nombre  = db.Column(db.String(30), nullable=False, unique=True)
    Descripcion = db.Column(db.String(30), nullable=True)
    Precio = db.Column(db.Numeric(10,2), nullable=False)
    Duracion_Dias = db.Column(db.Integer(11), nullable=True)  
    Estado = db.Column(db.Boolean, nullable=False)
