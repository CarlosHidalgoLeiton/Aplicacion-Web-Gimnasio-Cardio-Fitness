from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Notification(db.Model):
    __tablename__ = 'notificacion'

    NotificationId  = db.Column(db.Integer, primary_key=True, key='NotificationId', name='ID_Notificacion')
    Subject = db.Column(db.String(255), nullable=False, key='Subject', name='Asunto')
    Date = db.Column(db.Date, nullable=False, key='Date', name='Fecha')
    Hour = db.Column(db.Time, nullable=False, key='Hour', name='Hora')
    State = db.Column(db.Boolean, nullable=False, key='State', name='Estado')
