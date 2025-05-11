from apps.db.db import db  # Importa la instancia de SQLAlchemy
class Trainer(db.Model):
    __tablename__ = 'entrenador'

    DocumentId = db.Column(db.String(16), primary_key=True, key="DocumentId", name="Cedula")
    Name = db.Column(db.String(30), nullable=False, key="Name", name="Nombre")
    First_LastName = db.Column(db.String(30), nullable=False, key="First_LastName", name="Primer_Apellido")
    Second_LastName = db.Column(db.String(30), nullable=False, key="Second_LastName", name="Segundo_Apellido")
    Date_Birth = db.Column(db.Date, nullable=False, key="Date_Birth", name="Fecha_Nacimiento")
    Age = db.Column(db.Integer, nullable=False, key="Age", name="Edad")
    Mail = db.Column(db.String(150), nullable=False, key="Mail", name="Correo")
    Phone = db.Column(db.String(8), nullable=False, key="Phone", name="Telefono")
    State = db.Column(db.Boolean, nullable=False, default=1, key="State", name="Estado")

    # def __str__(self):
    #     return (f"Trainer(DocumentId={self.DocumentId}, Name={self.Name}, "
    #             f"lastName={self.lastName}, lastName2={self.lastName2}, "
    #             f"DateOfBirth={self.DateOfBirth}, Age={self.Age}, "
    #             f"Email={self.Email}, Phone={self.Phone}, State={self.State})")
