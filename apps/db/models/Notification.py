from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Notification(db.Model):
    __tablename__ = 'notificacion'

    ID_Notificacion  = db.Column(db.Integer, primary_key=True)
    Asunto = db.Column(db.String(255), nullable=False)
    Fecha = db.Column(db.Date, nullable=False)
    Hora = db.Column(db.Time, nullable=False)
    Estado = db.Column(db.Boolean, nullable=False)
