from .entities.Trainer import Trainer
from .entities.Client import Client

class ModelTrainer:

    @classmethod
    def getTrainer(cls, conexion, DocumentId):
        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, Telefono, Estado FROM Entrenador WHERE Cedula = %s"
            cursor.execute(sql, (DocumentId))
            row = cursor.fetchone()
            if row is not None:
                trainer = Trainer(
                    DocumentId=row[0],  
                    Name=row[1],        
                    lastName=row[2],    
                    lastName2=row[3],   
                    DateOfBirth=row[4],   
                    Age=row[5],           
                    Email=row[6],       
                    Phone=row[7],         
                    State=row[8]          
                )
                return trainer
            return None
        except Exception as ex:
            print(f"Error al obtener el entrenador: {ex}")
            return None

    @classmethod
    def get_all_clients(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, Telefono, FechaInscripcion, Ocupacion, TelefonoEmergencia, Direccion, FechaIngreso, Padecimientos, Limitacion, VencimientoMembresia, Estado, ID_Membresia FROM Cliente WHERE NOT EXISTS (SELECT 1 FROM usuario WHERE usuario.Cedula = Cliente.Cedula) "
            cursor.execute(sql)
            rows = cursor.fetchall()

            clientes = []
            for row in rows:
                # Crear un objeto `cliente` por cada fila

                client = Client(
                    DocumentId=row[0],
                    Name=row[1],
                    lastName=row[2],
                    lastName2=row[3],
                    DateOfBirth=row[4],
                    Age=row[5],
                    Email=row[6],
                    Phone=row[7],
                    RegistrationDate=row[8],
                    Occupation=row[9],
                    TelephoneEmergency=row[10],
                    Address=row[11],
                    EntryDate=row[12],
                    Ailments=row[13],
                    Limitation=row[14],
                    ExpirationMembership=row[15],
                    State=row[16],
                    Membership_ID=row[17]
                )
                clientes.append(client)

            return clientes
        except Exception as ex:
            print(f"Error al obtener clientes: {ex}")
            return None
        
    @classmethod
    def get_all_trainers(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, Telefono, Estado FROM Entrenador WHERE NOT EXISTS (SELECT 1 FROM usuario WHERE usuario.Cedula = Entrenador.Cedula) "
            cursor.execute(sql)
            rows = cursor.fetchall()
            trainers = []
            for row in rows:
                trainer = Trainer(
                    DocumentId=row[0],
                    Name=row[1],
                    lastName=row[2],
                    lastName2=row[3],
                    DateOfBirth=row[4],
                    Age=row[5],
                    Email=row[6],
                    Phone=row[7],
                    State=row[8]
                )
                trainers.append(trainer)
            return trainers
        except Exception as ex:
            print(f"Error al obtener los entrenadores: {ex}")
            return None