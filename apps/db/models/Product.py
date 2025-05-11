from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Product(db.Model):
    __tablename__ = 'producto'
    
    ID_Product = db.Column(db.Integer, primary_key=True, key="ID_Product", name="ID_Producto")
    Name = db.Column(db.String(30), nullable=False, unique=True, key="Name", name="Nombre")
    Detail = db.Column(db.String(255), nullable=True, key="Detail", name="Detalle")
    Price = db.Column(db.Numeric(10,2), nullable=False, key="Price", name="Precio")
    Stock = db.Column(db.Integer, nullable=False, key="Stock", name="Cantidad")
    Image = db.Column(db.LargeBinary, nullable=False, key="Image", name="Imagen")
    State = db.Column(db.Boolean, nullable=False, key="State", name="Estado")

