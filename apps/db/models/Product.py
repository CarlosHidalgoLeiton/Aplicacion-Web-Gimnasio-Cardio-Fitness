from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Product(db.Model):
    __tablename__ = 'producto'

    ID_Producto = db.Column(db.Integer(11), primary_key=True)
    Nombre = db.Column(db.String(30), nullable=False, unique=True)
    Detalle = db.Column(db.String(255), nullable=True)
    Precio = db.Column(db.Numeric(10,2), nullable=False)
    Cantidad = db.Column(db.Integer(11), nullable=False)
    Imagen = db.Column(db.LONGBLOB, nullable=False)
    Estado = db.Column(db.Boolean, nullable=False)



