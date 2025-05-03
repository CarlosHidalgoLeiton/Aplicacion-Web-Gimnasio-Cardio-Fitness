from apps.db.db import db  # Importa la instancia de SQLAlchemy


class Bill(db.Model):
    __tablename__ = 'factura'

    ID_Factura = db.Column(db.Integer(11), primary_key=True)
    Monto = db.Column(db.Numeric(10,2), nullable=False)
    Tipo = db.Column(db.String(60), nullable=False)
    Descripcion = db.Column(db.String(255), nullable=False)
    Fecha = db.Column(db.Date, nullable=False)
    TipoEntidad = db.Column(db.String(50), nullable=False)
    ID_Entidad = db.Column(db.String(255), nullable=False)
    Estado = db.Column(db.Boolean, nullable=False)
    Lot = db.Column(db.String(50), nullable=False)
