from apps.db.db import db  # Importa la instancia de SQLAlchemy
from apps.db.models.Trainer import Trainer
from apps.db.models.Client import Client

class Statistics(db.Model):
    __tablename__ = 'estadistica'

    ID_Statistics = db.Column(db.Integer, primary_key=True, nullable=False, key="ID_Statistics", name="ID_Estadistica")
    Measurement_Date = db.Column(db.Date, nullable=False, key="Measurement_Date", name="FechaMedicion")
    Stature = db.Column(db.String(20), nullable=True, key="Stature", name="Estatura")
    Weight = db.Column(db.String(10), nullable=True, key="Weight", name="Peso")
    IMC = db.Column(db.String(10), nullable=True, key="IMC", name="IMC")
    FC_Repose = db.Column(db.String(20), nullable=True, key="FC_Repose", name="FC_REPOSO")
    FC_MAX = db.Column(db.String(20), nullable=True, key="FC_MAX", name="FC_MAX")
    Blood_pressure = db.Column(db.String(20), nullable=True, key="Blood_pressure", name="Presion_Arterial")
    BMR = db.Column(db.String(10), nullable=True, key="BMR", name="BMR")
    Body_Fat = db.Column(db.String(10), nullable=True, key="Body_Fat", name="Grasa_Corporal")
    Percent_Water = db.Column(db.String(10), nullable=True, key="Percent_Water", name="Porcentaje_Agua")
    Muscle_Mass = db.Column(db.String(10), nullable=True, key="Muscle_Mass", name="Masa_Muscular")
    Metabolic_Age = db.Column(db.String(10), nullable=True, key="Metabolic_Age", name="Edad_Metabolica")
    Bone_Mass = db.Column(db.String(10), nullable=True, key="Bone_Mass", name="Masa_Osea")
    Visceral_Fat = db.Column(db.String(10), nullable=True, key="Visceral_Fat", name="Grasa_Visceral")
    Chest_Circum = db.Column(db.String(10), nullable=True, key="Chest_Circum", name="Circun_Pecho")
    Right_Arm_Circum = db.Column(db.String(10), nullable=True, key="Right_Arm_Circum", name="Circun_Brazo_Der")
    Left_Arm_Circum = db.Column(db.String(10), nullable=True, key="Left_Arm_Circum", name="Circun_Brazo_Izq")
    Circum_Waist = db.Column(db.String(10), nullable=True, key="Circum_Waist", name="Circun_Cintura")
    Circum_Abdomen = db.Column(db.String(10), nullable=True, key="Circum_Abdomen", name="Circun_Abdomen")
    Hip_Circum = db.Column(db.String(10), nullable=True, key="Hip_Circum", name="Circun_Cadera")
    Circum_Thigh_Right = db.Column(db.String(10), nullable=True, key="Circum_Thigh_Right", name="Circun_Muslo_Der")
    Circum_Thigh_Left = db.Column(db.String(10), nullable=True, key="Circum_Thigh_Left", name="Circun_Muslo_Izq")
    Circum_Calf_Right = db.Column(db.String(10), nullable=True, key="Circum_Calf_Right", name="Circun_Pantorilla_Der")
    Circum_Calf_Left = db.Column(db.String(10), nullable=True, key="Circum_Calf_Left", name="Circun_Pantorilla_Izq")
    Special_Considerations = db.Column(db.String(255), nullable=True, key="Special_Considerations", name="Consideraciones_Especiales")
    sportsman = db.Column(db.Boolean, nullable=True, key="sportsman", name="Deportista")
    Training_Goal = db.Column(db.String(10), nullable=True, key="Training_Goal", name="Objetivo_Entrenamiento")
    Emphasis_Training = db.Column(db.String(10), nullable=True, key="Emphasis_Training", name="Enfasis_Entrenamiento")
    Disponibilidad = db.Column(db.String(10), nullable=True, key="Disponibilidad", name="Disponibilidad")
    State = db.Column(db.Boolean, nullable=False, default=1, key="State", name="Estado")
    Client_ID = db.Column(db.String(16), db.ForeignKey('cliente.DocumentId'), nullable=False, key="Client_ID", name="ID_Cliente")
    Trainer_ID = db.Column(db.String(16), db.ForeignKey('entrenador.DocumentId'), nullable=False, key="Trainer_ID", name="ID_Entrenador")

    entrenador = db.relationship('Trainer', backref='estadisticas', lazy='joined')
    cliente = db.relationship('Client', backref='estadisticas', lazy='joined')

  



            


