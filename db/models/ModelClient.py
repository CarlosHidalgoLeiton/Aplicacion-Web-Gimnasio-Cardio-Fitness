from .entities.Client import Client
from datetime import datetime
import re

class ModelCliente:

    @classmethod
    def insertClient(cls, conection, client):
        if client != None:
            try:

                cursor = conection.cursor()
                sql = """INSERT INTO Cliente (Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, Telefono, Ocupacion, TelefonoEmergencia, Direccion, FechaIngreso, Padecimientos, Limitacion, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (client.Cedula, client.Nombre, client.Primer_Apellido, client.Segundo_Apellido, client.Fecha_Nacimiento, client.Edad, client.Correo, client.Telefono, client.Ocupacion, client.TelefonoEmergencia, client.Direccion, client.FechaIngreso, client.Padecimientos, client.Limitacion, client.Estado))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Cliente {client.Cedula} creado exitosamente.")
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
        bornDateStr = request.form['bornDate']
        bornDate = datetime.strptime(bornDateStr, "%Y-%m-%d").date()
        mail = request.form['mail']
        phone = request.form['phone']
        ocupation = request.form['ocupation']
        emergencyPhone = request.form['emergencyPhone']
        direction = request.form['direction']
        incomeDate = datetime.now()
        ailments = request.form['ailments']
        limitation = request.form['limitation']
        age = datetime.now().year - bornDate.year
        state = 1

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
        
        #Validation for bornDate
        if bornDate != None:
            if datetime.strptime(bornDateStr, "%Y-%m-%d") > datetime.now():
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
        if direction == None:
            return "Debe ingresar la dirección."
        
        return Client(documentId, name, firstLastName, secondLastName, bornDate, age, mail, phone, None, ocupation, emergencyPhone, direction, incomeDate, ailments, limitation, None, state)
        
