
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Routine(db.Model):
    __tablename__ = 'rutina'

    ID_Rutina = db.Column(db.Integer, primary_key=True)
    ID_Cliente = db.Column(db.String, db.ForeignKey('cliente.Cedula'), nullable=False)
    ID_Entrenador = db.Column(db.String, db.ForeignKey('entrenador.Cedula'), nullable=False)
    Indicaciones = db.Column(db.String(255), nullable=True)
    Fecha = db.Column(db.Date, nullable=False)
    Estado = db.Column(db.Boolean, nullable=False)


    def to_dict(self):
        return {
            "RoutineId": self.RoutineId,
            "ClientId": self.ClientId,
            "TrainerId": self.TrainerId,
            "Indications": self.Indications,
            "Date": self.Date,
            "State": self.State,
        }  

