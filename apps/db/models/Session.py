
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Session(db.Model):
    __tablename__ = 'sesion'

    ID_Sesion = db.Column(db.Integer, primary_key=True)
    Nombre = db.Column(db.String(100), nullable=False)
    Indicaciones = db.Column(db.String(255), nullable=True)
    Ejercicios = db.Column(db.Text, nullable=True)
    ID_Rutina = db.Column(db.String, db.ForeignKey('rutina.ID_Rutina'), nullable=False)


    def to_dict(self):
        return {
            "Session_ID": self.Session_ID,
            "Indications": self.Indications,
            "Exercises": self.Exercises,
            "Routine_ID": self.Routine_ID,
            "Name": self.Name
        }