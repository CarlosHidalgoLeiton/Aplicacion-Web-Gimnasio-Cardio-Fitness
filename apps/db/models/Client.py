
from datetime import datetime
from apps.db.db import db  # Importa la instancia de SQLAlchemy

class Client(db.Model):
    __tablename__ = 'cliente'

    DocumentId = db.Column(db.String(16), primary_key=True, key="DocumentId", name="Cedula")
    Name = db.Column(db.String(30), nullable=False, key="Name", name="Nombre")
    First_LastName = db.Column(db.String(30), nullable=False, key="First_LastName", name="Primer_Apellido")
    Second_LastName = db.Column(db.String(30), nullable=False, key="Second_LastName", name="Segundo_Apellido")
    Date_Birth = db.Column(db.Date, nullable=False, key="Date_Birth", name="Fecha_Nacimiento")
    Age = db.Column(db.Integer, nullable=False, key="Age", name="Edad")
    Mail = db.Column(db.String(150), nullable=False, key="Mail", name="Correo")
    Phone = db.Column(db.String(8), nullable=False, key="Phone", name="Telefono")
    Registration_Date = db.Column(db.Date, nullable=False, key="Registration_Date", name="FechaInscripcion")
    Occupation = db.Column(db.String(150), nullable=False, key="Occupation", name="Ocupacion")
    TelephoneEmergency = db.Column(db.String(8), nullable=False, key="TelephoneEmergency", name="TelefonoEmergencia")
    Address = db.Column(db.String(255), nullable=False, key="Address", name="Direccion")
    Entry_Date = db.Column(db.Date, nullable=False, key="Entry_Date", name="FechaIngreso")
    Ailments = db.Column(db.String(255), nullable=False, key="Ailments", name="Padecimientos")
    Limitation = db.Column(db.String(255), nullable=False, key="Limitation", name="Limitacion")
    ExpirationMembership = db.Column(db.Date, nullable=True, key="ExpirationMembership", name="VencimientoMembresia")
    State = db.Column(db.Boolean, nullable=False, key="State", name="Estado")
    Membership_ID = db.Column(db.Integer, db.ForeignKey('membresia.id'), nullable=False, key="Membership_ID", name="ID_Membresia")

    

    
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

