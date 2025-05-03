
from datetime import datetime
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Client(db.Model):
    __tablename__ = 'cliente'

    Cedula = db.Column(db.String(16), primary_key=True)
    Nombre = db.Column(db.String(30), nullable=False)
    Primer_Apellido = db.Column(db.String(30), nullable=False)
    Segundo_Apellido = db.Column(db.String(30), nullable=False)
    Fecha_Nacimiento = db.Column(db.Date, nullable=False)
    Edad = db.Column(db.Integer, nullable=False)
    Correo = db.Column(db.String(150), nullable=False)
    Telefono = db.Column(db.String(8), nullable=False)
    FechaInscripcion = db.Column(db.Date, nullable=False)
    Ocupacion = db.Column(db.String(150), nullable=False)
    TelefonoEmergencia = db.Column(db.String(8), nullable=False)
    Direccion = db.Column(db.String(255), nullable=False)
    FechaIngreso = db.Column(db.Date, nullable=False)
    Padecimientos = db.Column(db.String(255), nullable=False)
    Limitacion = db.Column(db.String(255), nullable=False)
    VencimientoMembresia = db.Column(db.Date, nullable=True)
    Estado = db.Column(db.Boolean, nullable=False)
    ID_Membresia =  db.Column(db.Integer, db.ForeignKey('membresia.ID_Membresia'), nullable=False)
    

    
    def to_dict(self):
        return {
            "DocumentId": self.DocumentId,
            "Name": self.Name,
            "First_LastName": self.First_LastName,
            "Second_LastName": self.Second_LastName,
            "Date_Birth": self.Date_Birth,
            "Age": self.Age,
            "Mail": self.Mail,
            "Phone": self.Phone,
            "Registration_Date": self.Registration_Date,
            "Occupation": self.Occupation,
            "TelephoneEmergency": self.TelephoneEmergency,
            "Address": self.Address,
            "Entry_Date": self.Entry_Date,
            "Ailments": self.Ailments,
            "Limitation": self.Limitation,
            "ExpirationMembership": self.ExpirationMembership,
            "State": self.State,
            "Membership_ID": self.Membership_ID
        }

    def is_member_active(self):
        """
        Verifica si la membresía está activa, comparando la fecha de vencimiento
        """
        if self.ExpirationMembership is not None:
            current_date = datetime.now().date()  
            expiration_date = self.ExpirationMembership
          
            return current_date <= expiration_date 
        
        return False 

