from apps.db.db import db  # Importa la instancia de SQLAlchemy

class CancelledBill(db.Model):
    __tablename__ = 'facturaanulada'

    ID_CancelledBill = db.Column(db.Integer, primary_key=True, key="ID_CancelledBill", name="ID_FacturaAnulada")
    Motive = db.Column(db.String(255), nullable=False, key="Motive", name="Motivo")
    CancelledDate = db.Column(db.Date, nullable=False, key="CancelledDate", name="FechaAnulacion")
    ID_Bill = db.Column(db.Integer, db.ForeignKey('factura.ID_Bill'), nullable=False, key="ID_Bill", name="ID_Factura")


