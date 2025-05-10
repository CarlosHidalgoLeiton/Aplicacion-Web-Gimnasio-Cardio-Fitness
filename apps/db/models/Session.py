
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Session(db.Model):
    __tablename__ = 'sesion'

    Session_ID = db.Column(db.Integer, primary_key=True, key='Session_ID', name='ID_Sesion')
    Name = db.Column(db.String(100), nullable=False, key='Name', name='Nombre')
    Indications = db.Column(db.String(255), nullable=True, key='Indications', name='Indicaciones')
    Exercises = db.Column(db.Text, nullable=True, key='Exercises', name='Ejercicios')
    Routine_ID = db.Column(db.String, db.ForeignKey('rutina.ID_Rutina'), nullable=False, key='Routine_ID', name='ID_Rutina')

    def to_dict(self):
        return {
            "Session_ID": self.Session_ID,
            "Indications": self.Indications,
            "Exercises": self.Exercises,
            "Routine_ID": self.Routine_ID,
            "Name": self.Name
        }