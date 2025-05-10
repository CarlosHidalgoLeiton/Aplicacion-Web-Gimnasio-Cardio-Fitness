from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Statistics(db.Model):
    __tablename__ = 'estadistica'

    ID_Statistics = db.Column("ID_Estadistica",db.Integer, primary_key=True,nullable=False)
    Measurement_Date = db.Column("FechaMedicion",db.Date, nullable=False)
    Stature = db.Column("Estatura",db.String(20), nullable=True)
    Weight = db.Column("Peso",db.String(10), nullable=True)
    IMC  = db.Column("IMC",db.String(10), nullable=True)
    FC_Repose  = db.Column("FC_REPOSO",db.String(20), nullable=True)
    FC_MAX = db.Column("FC_MAX",db.String(20), nullable=True)
    Blood_pressure = db.Column("Presion_Arterial",db.String(20), nullable=True)
    BMR = db.Column("BMR",db.String(10), nullable=True)
    Body_Fat = db.Column("Grasa_Corporal",db.String(10), nullable=True)
    Percent_Water = db.Column("Porcentaje_Agua",db.String(10), nullable=True)
    Muscle_Mass = db.Column("Masa_Muscular",db.String(10), nullable=True)
    Metabolic_Age = db.Column("Edad_Metabolica",db.String(10), nullable=True)
    Bone_Mass = db.Column("Masa_Osea",db.String(10), nullable=True)
    Visceral_Fat = db.Column("Grasa_Visceral",db.String(10), nullable=True)
    Chest_Circum = db.Column("Circun_Pecho",db.String(10), nullable=True)
    Right_Arm_Circum = db.Column("Circun_Brazo_Der",db.String(10), nullable=True)
    Left_Arm_Circum = db.Column("Circun_Brazo_Izq",db.String(10), nullable=True)
    Circum_Waist = db.Column("Circun_Cintura",db.String(10), nullable=True)
    Circum_Abdomen = db.Column("Circun_Abdomen",db.String(10), nullable=True)
    Hip_Circum = db.Column("Circun_Cadera",db.String(10), nullable=True)
    Circum_Thigh_Right = db.Column("Circun_Muslo_Der",db.String(10), nullable=True)
    Circum_Thigh_Left = db.Column("Circun_Muslo_Izq",db.String(10), nullable=True)
    Circum_Calf_Right = db.Column("Circun_Pantorilla_Der",db.String(10), nullable=True)
    Circum_Calf_Left = db.Column("Circun_Pantorilla_Izq",db.String(10), nullable=True)
    Special_Considerations  = db.Column("Consideraciones_Especiales",db.String(255), nullable=True)
    sportsman = db.Column("Deportista",db.Boolean, nullable=True)
    Training_Goal = db.Column("Objetivo_Entrenamiento",db.String(10), nullable=True)
    Emphasis_Training = db.Column("Enfasis_Entrenamiento",db.String(10), nullable=True)
    Disponibilidad = db.Column("Disponibilidad",db.String(10), nullable=True)
    State = db.Column("Estado",db.Boolean, nullable=False, default=1)
    Client_ID = db.Column("ID_Cliente",db.String(16),db.ForeignKey('cliente.DocumentId'), nullable=False)
    Trainer_ID = db.Column("ID_Entrenador",db.String(16),db.ForeignKey('entrenador.Cedula'), nullable=False)

    entrenador = db.relationship('Trainer', backref='estadisticas', lazy='joined')
    cliente = db.relationship('Client', backref='estadisticas', lazy='joined')



            


