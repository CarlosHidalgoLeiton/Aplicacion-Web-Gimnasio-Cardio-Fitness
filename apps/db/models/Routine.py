
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Routine(db.Model):
    __tablename__ = 'rutina'

    RoutineId = db.Column(db.Integer, primary_key=True, key='RoutineId', name='ID_Rutina')
    ClientId = db.Column(db.String, db.ForeignKey('cliente.DocumentId'), nullable=False, key='ClientId', name='ID_Cliente')
    TrainerId = db.Column(db.String, db.ForeignKey('entrenador.DocumentId'), nullable=False, key='TrainerId', name='ID_Entrenador')
    Indications = db.Column(db.String(255), nullable=True, key='Indications', name='Indicaciones')
    Date = db.Column(db.Date, nullable=False, key='Date', name='Fecha')
    State = db.Column(db.Boolean, nullable=False, key='State', name='Estado')

    entrenador = db.relationship('Trainer', backref='rutina', lazy='joined')
    cliente = db.relationship('Client', backref='rutina', lazy='joined')

    def to_dict(self):
        return {
            "RoutineId": self.RoutineId,
            "ClientId": self.ClientId,
            "TrainerId": self.TrainerId,
            "Indications": self.Indications,
            "Date": self.Date,
            "State": self.State,
        }  

