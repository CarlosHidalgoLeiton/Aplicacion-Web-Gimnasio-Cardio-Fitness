from apps.db.models.Trainer import Trainer
from pymysql import IntegrityError
import re
from datetime import datetime
from apps.db.repositories.UserRepository import UserRepository
from apps.db.repositories.RepositoryBase import RepositoryBase




class TrainerRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Trainer)
    
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
        age = datetime.now().year - Date_Birth.year - (
            (datetime.now().month, datetime.now().day) < (Date_Birth.month, Date_Birth.day)
        )
        state = True

        return Trainer(
            DocumentId=documentId,
            Name=name,
            First_LastName=firstLastName,
            Second_LastName=secondLastName,
            Date_Birth=Date_Birth,
            Age=age,
            Mail=mail,
            Phone=phone,
            State=state
        )


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
    


    classmethod
    def disable_trainer(self, trainer_id):
        return self.update(trainer_id, State=0) 

    classmethod
    def able_trainer(self, trainer_id):
        return self.update(trainer_id, State=1) 
