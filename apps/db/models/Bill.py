from apps.db.db import db  # Importa la instancia de SQLAlchemy


class Bill(db.Model):
    __tablename__ = 'factura'

    ID_Bill = db.Column(db.Integer, primary_key=True, key="ID_Bill", name="ID_Factura")
    Amount = db.Column(db.Numeric(10,2), nullable=False, key="Amount", name="Monto")
    Type = db.Column(db.String(60), nullable=False, key="Type", name="Tipo")
    Description = db.Column(db.String(255), nullable=False, key="Description", name="Descripcion")
    Date = db.Column(db.Date, nullable=False, key="Date", name="Fecha")
    EntityType = db.Column(db.String(50), nullable=False, key="EntityType", name="TipoEntidad")
    ID_Entity = db.Column(db.String(255), nullable=False, key="ID_Entity", name="ID_Entidad")
    State = db.Column(db.Boolean, nullable=False, key="State", name="Estado")
    Lot = db.Column(db.String(50), nullable=False, key="Lot", name="Lot")
