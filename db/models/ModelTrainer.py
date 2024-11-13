from .entities.Trainer import Trainer
from pymysql import IntegrityError
import re
from datetime import datetime
from db.models.ModelUser import ModelUser

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
    def updateTrainer(cls, conection, trainer, id):
        """
            It updates a trainer in the data base.

            This method receives a `Trainer` object and updates it in the database table `Trainer`. 
            It assumes that the `Trainer` object has attributes corresponding to the fields in the table. 
            If the update is successful, it commits the transaction and returns True. If an error occurs 
            during the process, it performs a rollback and returns an error message.
            
            Parameters:
            conection(obj): conection object to the database
            trainer(Trainer): trainer object that contains the data to update
            id(str) -- trainer's identification to update

            Return: 
                `bool`:   `True` if the client was inserted successfuly,
                `string`: `Error Message` an error message.

            Exceptions:
                - IntegrityError: If an integrity error occurs (e.g. duplicate primary key).
                - BaseException: For any other database related errors.
                - Exception: For other general errors that may occur during execution.
        """

        if trainer != None:
            try:
                cursor = conection.cursor()
                
                sql = """UPDATE Entrenador SET Cedula = %s, Nombre = %s, Primer_Apellido = %s, Segundo_Apellido = %s, Fecha_Nacimiento = %s, Edad = %s, Correo = %s, Telefono = %s WHERE Cedula = %s"""
                cursor.execute(sql, (trainer.DocumentId, trainer.Name, trainer.First_LastName, trainer.Second_LastName, trainer.Date_Birth, trainer.Age, trainer.Mail, trainer.Phone, id))
                

                if cursor.rowcount > 0:
                    print(f"Entrenador {trainer.DocumentId} actualizado exitosamente.")

                    user = ModelUser.get_User(conection, id)

                    if user:
                        sql2 = "UPDATE Usuario SET Cedula = %s WHERE Cedula = %s"
                        cursor.execute(sql2, ( trainer.DocumentId ,id))

                        if cursor.rowcount < 0:
                            print("No se pudo actualizar el usuario en updateTrainer.")
                            return "Error"
                        
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar el entrenador.")
                    return "Error"

            except IntegrityError as ex:
                print(f"Error en ModelTrainer updateTrainer: {ex}")
                conection.rollback()
                return "Primary"
            except BaseException as ex:
                print(f"Error en ModelTrainer updateTrainer: {ex}")
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelTrainer updateTrainer: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"

    @classmethod
    def getTrainer(cls, conection, DocumentId):
        try:
            cursor = conection.cursor()
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
                    Mail=row[6],       
                    Phone=row[7],         
                    State=row[8]          
                )
                return trainer
            return None
        except Exception as ex:
            print(f"Error al obtener el entrenador: {ex}")
            return None
    
    @classmethod
    def getTrainerBill(cls, conection, DocumentId):
        try:
            cursor = conection.cursor()
            sql = "SELECT Nombre, Primer_Apellido, Segundo_Apellido FROM Entrenador WHERE Cedula = %s"
            cursor.execute(sql, (DocumentId))
            row = cursor.fetchone()
            if row is not None:
                trainer = Trainer(
                    Name=row[0],        
                    First_LastName=row[1],    
                    Second_LastName=row[2],          
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
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Estado, Edad FROM Entrenador"
            cursor.execute(sql)
            rows = cursor.fetchall()
            trainers = []
            for row in rows:
                trainer = {
                    'DocumentId': row[0],
                    'Name': row[1],
                    'First_LastName': row[2],
                    'Second_LastName':row[3],
                    'State': row[4],
                    'Age': row[5]
                }
                trainers.append(trainer)
            return trainers
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None
        
    @classmethod
    def get_allAble(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Estado FROM Entrenador WHERE Estado = 1"
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
            if re.match("^[a-zA-Z0-9]*$", trainer.DocumentId):
                if len(trainer.DocumentId) < 9 or len(trainer.DocumentId) > 16:
                    return "El número de cédula ingresado no es válido. Cantidad de dígitos no válida."
            else:
                return "El número de cédula no debe contener caracteres especiales."
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
    
    @classmethod
    def disableTrainer(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Entrenador SET Estado = 0  WHERE Cedula = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    
                    return True
                else:
                    print("No se pudo actualizar el entrenador.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar el entrenador {ex}")
                conection.rollback()
                return False
        else:
            return False
        
    @classmethod
    def ableTrainer(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Entrenador SET Estado = 1  WHERE Cedula = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar el entrenador.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar el entrenador {ex}")
                conection.rollback()
                return False
        else:
            return False
