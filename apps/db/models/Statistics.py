from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Statistics(db.Model):
    __tablename__ = 'estadistica'

    ID_Estadistica  = db.Column(db.Integer, primary_key=True,nullable=False)
    FechaMedicion = db.Column(db.Date, nullable=False)
    Estatura = db.Column(db.String(20), nullable=True)
    Peso = db.Column(db.String(10), nullable=True)
    IMC = db.Column(db.String(10), nullable=True)
    FC_REPOSO = db.Column(db.String(20), nullable=True)
    FC_MAX = db.Column(db.String(20), nullable=True)
    Presion_Arterial = db.Column(db.String(20), nullable=True)
    BMR = db.Column(db.String(10), nullable=True)
    Grasa_Corporal = db.Column(db.String(10), nullable=True)
    Porcentaje_Agua = db.Column(db.String(10), nullable=True)
    Masa_Muscular = db.Column(db.String(10), nullable=True)
    Edad_Metabolica = db.Column(db.String(10), nullable=True)
    Masa_Osea = db.Column(db.String(10), nullable=True)
    Grasa_Visceral = db.Column(db.String(10), nullable=True)
    Circun_Pecho = db.Column(db.String(10), nullable=True)
    Circun_Brazo_Der = db.Column(db.String(10), nullable=True)
    Circun_Brazo_Izq = db.Column(db.String(10), nullable=True)
    Circun_Cintura = db.Column(db.String(10), nullable=True)
    Circun_Abdomen = db.Column(db.String(10), nullable=True)
    Circun_Cadera = db.Column(db.String(10), nullable=True)
    Circun_Muslo_Der = db.Column(db.String(10), nullable=True)
    Circun_Muslo_Izq = db.Column(db.String(10), nullable=True)
    Circun_Pantorilla_Der = db.Column(db.String(10), nullable=True)
    Circun_Pantorilla_Izq = db.Column(db.String(10), nullable=True)
    Consideraciones_Especiales = db.Column(db.String(255), nullable=True)
    Deportista = db.Column(db.Boolean, nullable=True)
    Objetivo_Entrenamiento = db.Column(db.String(10), nullable=True)
    Enfasis_Entrenamiento = db.Column(db.String(10), nullable=True)
    Disponibilidad = db.Column(db.String(10), nullable=True)
    Estado = db.Column(db.Boolean, nullable=False, default=1)
    ID_Cliente  = db.Column(db.String(16),db.ForeignKey('cliente.Cedula'), nullable=False)
    ID_Entrenador  = db.Column(db.String(16),db.ForeignKey('entrenador.Cedula'), nullable=False)

            


