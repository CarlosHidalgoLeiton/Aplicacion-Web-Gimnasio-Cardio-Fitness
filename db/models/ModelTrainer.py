from .entities.Trainer import Trainer

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
