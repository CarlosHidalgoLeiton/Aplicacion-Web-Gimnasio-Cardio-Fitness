"""Client Module"""

from apps.db.models.Client import Client
from datetime import datetime
from apps.db.models.Notification import Notification
import re
from pymysql import IntegrityError
from datetime import date

from apps.db.repositories.RepositoryBase import RepositoryBase


class ClientRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Client)

    @classmethod
    def getDataClient(cls, request):
        Date_BirthStr = request.form['Date_Birth']
        Date_Birth = datetime.strptime(Date_BirthStr, "%Y-%m-%d").date()
        age = datetime.now().year - Date_Birth.year - ((datetime.now().month, datetime.now().day) < (Date_Birth.month, Date_Birth.day))

        return Client(
            DocumentId=request.form['documentId'],
            Name=request.form['name'],
            First_LastName=request.form['firstLastName'],
            Second_LastName=request.form['secondLastName'],
            Date_Birth=Date_Birth,
            Age=age,
            Mail=request.form['mail'],
            Phone=request.form['phone'],
            Registration_Date=None,
            Occupation=request.form['ocupation'],
            TelephoneEmergency=request.form['emergencyPhone'],
            Address=request.form['adress'],
            Entry_Date= date.today(),
            Ailments=request.form['ailments'],
            Limitation=request.form['limitation'],
            ExpirationMembership=None,
            State=True,
            Membership_ID=None,
            EntranceDoor=None
        )


    @classmethod
    def validateDataForm(cls, client):
        """
            Validates the data in a `Client` object.

            This method performs a series of validations on the attributes of the 
            provided `Client` object. It checks for proper format, required fields, 
            and constraints (e.g., length, characters). If any validation fails, 
            an appropriate error message is returned. If all validations pass, 
            the method returns `True`.

            Parameters:
            client (Client): The `Client` object to validate.

            Returns:
            str: An error message if any validation fails.
            True: If all validations pass.

            Notes:
            - The method expects the `Client` object to have the following fields:
            `DocumentId`, `Name`, `First_LastName`, `Second_LastName`, `Date_Birth`, 
            `Mail`, `Phone`, `Occupation`, `TelephoneEmergency`, `Address`, `Ailments`, 
            and `Limitation`.
            - The method uses regular expressions to validate fields like `DocumentId`, `Mail`, 
            and `Phone`.
        """

        #Validation for documentID 
        if client.DocumentId != None:
            print(all(m.isalpha() for m in client.DocumentId))
            if re.match("^[a-zA-Z0-9]*$", client.DocumentId):
                if len(client.DocumentId) < 9 or len(client.DocumentId) > 16:
                    return "El número de cédula ingresado no es válido. Cantidad de dígitos no válida."
            else:
                return "El número de cédula no debe contener caracteres especiales."
        else:
            return "Debe ingresar el número de cédula."
        
        #Validation for name
        if client.Name != None:
             if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", client.Name.strip()):
                 return "El nombre solo debe contener letras y espacios (sin caracteres especiales ni números)."
        else:
            return "Debe ingresar el nombre."
        
        #Validation for firstLastName
        if client.First_LastName != None:
               if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", client.First_LastName.strip()):
                return "El apellido 1 solo debe contener letras y espacios (sin números ni caracteres especiales)."
        else:
            return "Debe ingresar el apellido 1."
        
        #Validation for secondLastName
        if client.Second_LastName != None:
            if not re.fullmatch(r"[A-Za-zÁÉÍÓÚáéíóúÑñ ]+", client.Second_LastName.strip()):
                return "El apellido 2 solo debe contener letras y espacios (sin números ni caracteres especiales)."
        else:
            return "Debe ingresar el apellido 2."
        
        #Validation for Date_Birth
        if client.Date_Birth != None:
            if client.Date_Birth > datetime.now().date():
                return "La fecha ingresada no es válida."
        else:
            return "Debe ingresar la fecha de nacimiento."
        
        #Validation for mail
        if client.Mail != None:
            expression = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' #To validate mail format
            if not re.match(expression, client.Mail):
                return "El correo ingresado no es válido."
        else:
            return "Debe ingresar el correo."
        
        #Validation for phone
        if client.Phone != None:
            if "-" not in client.Phone and not any( p.isalpha() for p in client.Phone): #Valida que sea alfabetico y que no tenga un "-"
                if len(client.Phone) != 8:
                    return "El número de teléfono ingresado no es válido. Debe ingresar 8 dígitos."
            else:
                return "El número de teléfono no debe contener letras o caracteres especiales."
        else:
            return "Debe ingresar el número de teléfono."
        
        #Validation for ocupation
        if client.Occupation != None:
            if not all(c.isalpha() or c.isspace() for c in client.Occupation):
                return "La ocupación no debe contener números ni caracteres especiales"
        else:
            return "Debe ingresar la ocupación."
        
        #Validation for emergencyPhone
        if client.TelephoneEmergency != None:
            if "-" not in client.TelephoneEmergency and not any( p.isalpha() for p in client.TelephoneEmergency): #Valida que sea alfabetico y que no tenga un "-"
                if len(client.TelephoneEmergency) != 8:
                    return "El número de teléfono de emergencia ingresado no es válido. Debe ingresar 8 dígitos."
            else:
                return "El número de teléfono de emergencia no debe contener letras o caracteres especiales."
        else:
            return "Debe ingresar el número de teléfono de emergencia."
        
        #Validation for direction
        if client.Address == None:
            return "Debe ingresar la dirección."
        
        #Validation for ailments
        if client.Ailments == None:
            return "Debe ingresar los padecimientos. En caso de que no tenga unicamente ingrese 'Ningúno'."
        
        #Validation for limitation
        if client.Limitation == None:
            return "Debe ingresar las limitaciones. En caso de que no tenga unicamente ingrese 'Ningúno'."
    
        return True
        
        
    def disable_client(self, client_id):
        return self.update(client_id, State=0) 

    def able_Client(self, client_id):
        return self.update(client_id, State=1) 
    
    def able_Entry(self, client_id):
        today = date.today()
        return self.update(client_id, EntranceDoor=today) 

