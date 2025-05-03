from apps.db.db import db  # Importa la instancia de SQLAlchemy

class CancelledBill(db.Model):
    __tablename__ = 'facturaanulada'

    ID_FacturaAnulada = db.Column(db.Integer, primary_key=True)
    Motivo = db.Column(db.String(255), nullable=False)
    FechaAnulacion = db.Column(db.Date, nullable=False)
    ID_Factura = db.Column(db.Integer, db.ForeignKey('factura.ID_Factura'), nullable=False)




