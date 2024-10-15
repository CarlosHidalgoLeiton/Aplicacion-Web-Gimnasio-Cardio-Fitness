from .entities.Trainer import Trainer
from pymysql import IntegrityError
import re
from datetime import datetime

class ModelTrainer:

    @classmethod
    def insertTrainer(cls, conection, trainer):
        if trainer != None:
            try:
                trainer.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Entrenador (Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, Telefono, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (trainer.DocumentId, trainer.Name, trainer.First_LastName, trainer.Second_LastName, trainer.Date_Birth, trainer.Age, trainer.Mail, trainer.Phone, trainer.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Entrenador {trainer.DocumentId} creado exitosamente.")
                    return True
                else:
                    print("No se pudo crear el entrenador.")
                    return "Error"
                
            except IntegrityError as ex:
                print(f"Error en Modeltrainere inserttrainer: {ex}")
                conection.rollback()
                return "Primary"
            except BaseException as ex:
                print(f"Error en Modeltrainer inserttrainer: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en Modeltrainer inserttrainer: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"

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
                    First_LastName=row[2],    
                    Second_LastName=row[3],   
                    Date_Birth=row[4],   
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
    def get_all(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Estado FROM Entrenador"
            cursor.execute(sql)
            rows = cursor.fetchall()
            trainers = []
            for row in rows:
                trainer = {
                    'DocumentId': row[0],
                    'Name': row[1],
                    'First_LastName': row[2],
                    'Second_LastName':row[3],
                    'State': row[4]
                }
                trainers.append(trainer)
            return trainers
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None
    
    @classmethod
    def getDataTrainer(cls, request):
        documentId = request.form['documentId']
        name = request.form['name']
        firstLastName = request.form['firstLastName']
        secondLastName = request.form['secondLastName']
        Date_BirthStr = request.form['Date_Birth']
        Date_Birth = datetime.strptime(Date_BirthStr, "%Y-%m-%d").date()
        mail = request.form['mail']
        phone = request.form['phone']
        age = datetime.now().year - Date_Birth.year

        return Trainer(documentId, name, firstLastName, secondLastName, Date_Birth, age, mail, phone)

    @classmethod
    def validateDataForm(cls, trainer):

        #Validation for documentID 
        if trainer.DocumentId != None:
            print(all(m.isalpha() for m in trainer.DocumentId))
            if "-" not in trainer.DocumentId and not any(m.isalpha() for m in trainer.DocumentId): #Valida que no sea alfabetico y que no tenga un "-"
                if len(trainer.DocumentId) < 9:
                    return "El número de cédula ingresado no es válido. Debe ingresar 9 dígitos."
            else:
                return "El número de cédula no debe contener letras ni caracteres especiales."
        else:
            return "Debe ingresar el número de cédula."
        
        #Validation for name
        if trainer.Name != None:
            if not trainer.Name.isalpha():
                return "El nombre no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el nombre."
        
        #Validation for firstLastName
        if trainer.First_LastName != None:
            if not trainer.First_LastName.isalpha():
                return "El apellido 1 no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el apellido 1."
        
        #Validation for secondLastName
        if trainer.Second_LastName != None:
            if not trainer.Second_LastName.isalpha():
                return "El apellido 2 no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el apellido 2."
        
        #Validation for Date_Birth
        if trainer.Date_Birth != None:
            if trainer.Date_Birth > datetime.now().date():
                return "La fecha ingresada no es válida."
        else:
            return "Debe ingresar la fecha de nacimiento."
        
        #Validation for mail
        if trainer.Mail != None:
            expression = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' #To validate mail format
            if not re.match(expression, trainer.Mail):
                return "El correo ingresado no es válido."
        else:
            return "Debe ingresar el correo."
        
        #Validation for phone
        if trainer.Phone != None:
            if "-" not in trainer.Phone and not any( p.isalpha() for p in trainer.Phone): #Valida que sea alfabetico y que no tenga un "-"
                if len(trainer.Phone) != 8:
                    return "El número de teléfono ingresado no es válido. Debe ingresar 8 dígitos."
            else:
                return "El número de teléfono no debe contener letras o caracteres especiales."
        else:
            return "Debe ingresar el número de teléfono."
    
        return True