from .entities.Client import Client
from datetime import datetime
import re

class ModelClient:

    @classmethod
    def insertClient(cls, conection, client):
        if client != None:
            try:
                Entry_Date = datetime.now()
                client.Entry_Date = Entry_Date
                client.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Cliente (Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, Telefono, Ocupacion, TelefonoEmergencia, Direccion, FechaIngreso, Padecimientos, Limitacion, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (client.DocumentId, client.Name, client.First_LastName, client.Second_LastName, client.Date_Birth, client.Age, client.Mail, client.Phone, client.Occupation, client.TelephoneEmergency, client.Address, client.Entry_Date, client.Ailments, client.Limitation, client.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Cliente {client.DocumentId} creado exitosamente.")
                    return True
                else:
                    print("No se pudo crear el cliente.")
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en insertar un cliente {ex}")
                # conection.rollback()
                return False
        else:
            return False
    
    @classmethod
    def updateClient(cls, conection, client, id):
        if client != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Cliente SET Cedula = %s, Nombre = %s, Primer_Apellido = %s, Segundo_Apellido = %s, Fecha_Nacimiento = %s, Edad = %s, Correo = %s, Telefono = %s, Ocupacion = %s, TelefonoEmergencia = %s, Direccion = %s, Padecimientos = %s, Limitacion = %s WHERE Cedula = %s"""
                cursor.execute(sql, (client.DocumentId, client.Name, client.First_LastName, client.Second_LastName, client.Date_Birth, client.Age, client.Mail, client.Phone, client.Occupation, client.TelephoneEmergency, client.Address, client.Ailments, client.Limitation, id))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Cliente {client.DocumentId} actualizado exitosamente.")
                    return True
                else:
                    print("No se pudo actualizar el cliente.")
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar un cliente {ex}")
                # conection.rollback()
                return False
        else:
            return False


    @classmethod
    def get_all_clients(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, Telefono, FechaInscripcion, Ocupacion, TelefonoEmergencia, Direccion, FechaIngreso, Padecimientos, Limitacion, VencimientoMembresia, Estado, ID_Membresia FROM Cliente"
            cursor.execute(sql)
            rows = cursor.fetchall()

            clientes = []
            for row in rows:
                # Crear un objeto `cliente` por cada fila

                client = Client(
                    Cedula=row[0],
                    Nombre=row[1],
                    Primer_Apellido=row[2],
                    Segundo_Apellido=row[3],
                    Fecha_Nacimiento=row[4],
                    Edad=row[5],
                    Correo=row[6],
                    Telefono=row[7],
                    FechaInscripcion=row[8],
                    Ocupacion=row[9],
                    TelefonoEmergencia=row[10],
                    Direccion=row[11],
                    FechaIngreso=row[12],
                    Padecimientos=row[13],
                    Limitacion=row[14],
                    VencimientoMembresia=row[15],
                    Estado=row[16],
                    ID_Membresia=row[17]
                )
                clientes.append(client)

            return clientes
        except Exception as ex:
            print(f"Error al obtener clientes: {ex}")
            return None


    @classmethod
    def get_all(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Ocupacion FROM Cliente"
            cursor.execute(sql)
            rows = cursor.fetchall()
            clients = []
            for row in rows:
                client = {
                    'DocumentId': row[0],
                    'Name': row[1],
                    'First_LastName': row[2],
                    'Second_LastName':row[3],
                    'Occupation': row[4]
                }
                clients.append(client)
            return clients
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None
        
    @classmethod
    def get_cliente_by_cedula(cls, conexion, DocumentId):
        try:
            cursor = conexion.cursor()
            sql = """SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, 
                    Telefono, FechaInscripcion, Ocupacion, TelefonoEmergencia, Direccion, FechaIngreso, 
                    Padecimientos, Limitacion, VencimientoMembresia, Estado, ID_Membresia 
                    FROM Cliente WHERE Cedula = %s"""
            cursor.execute(sql, (DocumentId))
            row = cursor.fetchone()

            if row:
                # Crear y devolver un objeto cliente
                return Client(
                    DocumentId=row[0],
                    Name=row[1],
                    First_LastName=row[2],
                    Second_LastName=row[3],
                    Date_Birth=row[4],
                    Age=row[5],
                    Mail=row[6],
                    Phone=row[7],
                    Registration_Date=row[8],
                    Occupation=row[9],
                    TelephoneEmergency=row[10],
                    Address=row[11],
                    Entry_Date=row[12],
                    Ailments=row[13],
                    Limitation=row[14],
                    ExpirationMembership=row[15],
                    State=row[16],
                    Membership_ID=row[17]
                )
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener cliente por cédula: {ex}")
            return None
    

    @classmethod
    def validateDataForm(cls,request):
        documentId = request.form['documentId']
        name = request.form['name']
        firstLastName = request.form['firstLastName']
        secondLastName = request.form['secondLastName']
        Date_BirthStr = request.form['Date_Birth']
        Date_Birth = datetime.strptime(Date_BirthStr, "%Y-%m-%d").date()
        mail = request.form['mail']
        phone = request.form['phone']
        ocupation = request.form['ocupation']
        emergencyPhone = request.form['emergencyPhone']
        adress = request.form['adress']
        ailments = request.form['ailments']
        limitation = request.form['limitation']
        age = datetime.now().year - Date_Birth.year

        #Validation for documentID 
        if documentId != None:
            if "-" not in documentId and not any( d.isalpha() for d in documentId): #Valida que sea alfabetico y que no tenga un "-"
                if len(documentId) < 9:
                    return "El número de cédula ingresado no es válido. Debe ingresar 9 dígitos."
            else:
                return "El número de cédula no debe contener letras ni caracteres especiales."
        else:
            return "Debe ingresar el número de cédula."
        
        #Validation for name
        if name != None:
            if not name.isalpha():
                return "El nombre no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el nombre."
        
        #Validation for firstLastName
        if firstLastName != None:
            if not firstLastName.isalpha():
                return "El apellido 1 no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el apellido 1."
        
        #Validation for secondLastName
        if secondLastName != None:
            if not secondLastName.isalpha():
                return "El apellido 2 no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el apellido 2."
        
        #Validation for Date_Birth
        if Date_Birth != None:
            if datetime.strptime(Date_BirthStr, "%Y-%m-%d") > datetime.now():
                return "La fecha ingresada no es válida."
        else:
            return "Debe ingresar la fecha de nacimiento."
        
        #Validation for mail
        if mail != None:
            expression = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$' #To validate mail format
            if not re.match(expression, mail):
                return "El correo ingresado no es válido."
        else:
            return "Debe ingresar el correo."
        
        #Validation for phone
        if phone != None:
            if "-" not in phone and not any( p.isalpha() for p in phone): #Valida que sea alfabetico y que no tenga un "-"
                if len(phone) != 8:
                    return "El número de teléfono ingresado no es válido. Debe ingresar 8 dígitos."
            else:
                return "El número de teléfono no debe contener letras o caracteres especiales."
        else:
            return "Debe ingresar el número de teléfono."
        
        #Validation for ocupation
        if ocupation != None:
            if not ocupation.isalpha():
                return "La ocupación no debe contener números ni caracteres especiales"
        else:
            return "Debe ingresar la ocupación."
        
        #Validation for emergencyPhone
        if emergencyPhone != None:
            if "-" not in emergencyPhone and not any( p.isalpha() for p in emergencyPhone): #Valida que sea alfabetico y que no tenga un "-"
                if len(emergencyPhone) != 8:
                    return "El número de teléfono de emergencia ingresado no es válido. Debe ingresar 8 dígitos."
            else:
                return "El número de teléfono de emergencia no debe contener letras o caracteres especiales."
        else:
            return "Debe ingresar el número de teléfono de emergencia."
        
        #Validation for direction
        if adress == None:
            return "Debe ingresar la dirección."
        
        #Validation for ailments
        if ailments == None:
            return "Debe ingresar los padecimientos. En caso de que no tenga unicamente ingrese 'Ningúno'."
        
        #Validation for limitation
        if limitation == None:
            return "Debe ingresar las limitaciones. En caso de que no tenga unicamente ingrese 'Ningúno'."
        
        return Client(documentId, name, firstLastName, secondLastName, Date_Birth, age, mail, phone, None, ocupation, emergencyPhone, adress, None, ailments, limitation, None, None)
        
