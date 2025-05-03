from apps.db.db import db  # Importa la instancia de SQLAlchemy
class Trainer(db.Model):
    __tablename__ = 'entrenador'

    Cedula = db.Column(db.String(16), primary_key=True)
    Nombre = db.Column(db.String(30), nullable=False)
    Primer_Apellido = db.Column(db.String(30), nullable=False)
    Segundo_Apellido = db.Column(db.String(30), nullable=False)
    Fecha_Nacimiento = db.Column(db.Date, nullable=False)
    Edad = db.Column(db.Integer, nullable=False)
    Correo = db.Column(db.String(150), nullable=False)
    Telefono = db.Column(db.String(8), nullable=False)
    Estado = db.Column(db.Boolean, nullable=False, default=1)

    # def __str__(self):
    #     return (f"Trainer(DocumentId={self.DocumentId}, Name={self.Name}, "
    #             f"lastName={self.lastName}, lastName2={self.lastName2}, "
    #             f"DateOfBirth={self.DateOfBirth}, Age={self.Age}, "
    #             f"Email={self.Email}, Phone={self.Phone}, State={self.State})")
