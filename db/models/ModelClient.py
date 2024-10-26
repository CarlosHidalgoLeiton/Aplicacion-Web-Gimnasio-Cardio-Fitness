"""Client Module"""

from .entities.Client import Client
from datetime import datetime
from .entities.Notification import Notification
import re
from pymysql import IntegrityError

class ModelClient:
    """It has the methods over Client."""

    @classmethod
    def insertClient(cls, conection, client):
        """
            It inserts a new client in the data base.

            This method receives a `Client` object and inserts it into the database table `Cliente`. 
            It assumes that the `Client` object has attributes corresponding to the fields in the table. 
            If the insert is successful, it commits the transaction and returns True. If an error occurs 
            during the process, it performs a rollback and returns an error message.
            
            Parameters:
            conection(obj): conection object to the database
            client(Client): client object that contains the data to insert

            Return: 
                `bool`:   `True` if the client was inserted successfuly,
                `string`: `Error Message` an error message.

            Exceptions:
                - IntegrityError: If an integrity error occurs (e.g. duplicate primary key).
                - BaseException: For any other database related errors.
                - Exception: For other general errors that may occur during execution.
        """
        

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
                    return "Error"
                
            except IntegrityError as ex:
                print(f"Error en ModelCLiente insertClient: {ex}")
                conection.rollback()
                return "Primary"
            except BaseException as ex:
                print(f"Error en ModelClient insertClient: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelClient insertClient: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
    
    @classmethod
    def updateClient(cls, conection, client, id):
        """
            It updates a client in the data base.

            This method receives a `Client` object and updates it in the database table `Cliente`. 
            It assumes that the `Client` object has attributes corresponding to the fields in the table. 
            If the update is successful, it commits the transaction and returns True. If an error occurs 
            during the process, it performs a rollback and returns an error message.
            
            Parameters:
            conection(obj): conection object to the database
            client(Client): client object that contains the data to update
            id(str) -- client's identification to update

            Return: 
                `bool`:   `True` if the client was inserted successfuly,
                `string`: `Error Message` an error message.

            Exceptions:
                - IntegrityError: If an integrity error occurs (e.g. duplicate primary key).
                - BaseException: For any other database related errors.
                - Exception: For other general errors that may occur during execution.
        """

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
                    return "Error"

            except IntegrityError as ex:
                print(f"Error en ModelCLiente updateClient: {ex}")
                conection.rollback()
                return "Primary"
            except BaseException as ex:
                print(f"Error en ModelClient updateClient: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelClient updateClient: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"

    @classmethod
    def get_all(cls, conexion):
        """
            It get all the clients.

            This method executes a sql query to get all the clients in the table `Cliente` and returns a dictionary list,
            where each of dictionary represents a `Client` with the fields of `DocumentId`, `Name`, 
            `First_LastName`, `Second_LastName`, `Occupation`, y `State`.
            
            Parameters:
            conection(obj): conection object to the database

            Return: 
                `list`: an dictionary list that contains the information about the clients.
                `None`: if occurs an error return `None`

            Exceptions:
                - Exception: General errors that may occur during execution.
        """

        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Ocupacion, Estado FROM Cliente"
            cursor.execute(sql)
            rows = cursor.fetchall()
            clients = []
            for row in rows:
                client = {
                    'DocumentId': row[0],
                    'Name': row[1],
                    'First_LastName': row[2],
                    'Second_LastName':row[3],
                    'Occupation': row[4],
                    'State': row[5]
                }
                clients.append(client)
            return clients
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None
    
    @classmethod
    def get_allAble(cls, conexion):
        """
            It get all the clients that are availabe.

            This method executes a sql query to get all the clients in the table `Cliente` and returns a dictionary list,
            where each of dictionary represents a `Client` with the fields of `DocumentId`, `Name`, 
            `First_LastName`, `Second_LastName`, `Occupation`, y `State`.
            
            Parameters:
            conection(obj): conection object to the database

            Return: 
                `list`: an dictionary list that contains the information about the clients.
                `None`: if occurs an error return `None`

            Exceptions:
                - Exception: General errors that may occur during execution.
        """

        try:
            cursor = conexion.cursor()
            sql = "SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Ocupacion, Estado FROM Cliente WHERE Estado = 1"
            cursor.execute(sql)
            rows = cursor.fetchall()
            clients = []
            for row in rows:
                client = {
                    'DocumentId': row[0],
                    'Name': row[1],
                    'First_LastName': row[2],
                    'Second_LastName':row[3],
                    'Occupation': row[4],
                    'State': row[5]
                }
                clients.append(client)
            return clients
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None

    @classmethod
    def getClient(cls, conexion, DocumentId):
        """
            Retrieves a specific client from the database using their ID (DocumentId).

            This method executes a SQL query to fetch a client from the `Cliente` table 
            in the database. If the client is found, it returns a `Client` object with 
            the corresponding fields. If the client is not found or an error occurs, it returns `None`.

            Parameters:
            conexion (obj): The database connection object.
            DocumentId (str): The client's ID (Cedula) to search for.

            Returns:
            Client: A `Client` object containing the client's data if found.
            None: If the client is not found or an error occurs during execution.

            Exceptions:
                - Exception: Captures general errors that may occur during the execution 
                of the query or while creating the `Client` object.
        """

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
    def getClientBill(cls, conexion, DocumentId):
        """
            Retrieves the client's name and last names for billing purposes from the database.

            This method executes a SQL query to fetch a client's basic information 
            (Name, First Last Name, and Second Last Name) from the `Cliente` table using 
            the provided `DocumentId`. It returns a `Client` object with the relevant 
            fields if the client is found, otherwise it returns `None`.

            Parameters:
            conexion (obj): The database connection object.
            DocumentId (str): The client's ID (Cedula) to search for.

            Returns:
            Client: A `Client` object containing the client's basic information if found.
            None: If the client is not found or an error occurs during execution.

            Exceptions:
            - Exception: Captures any general errors that may occur during the execution 
            of the query or while creating the `Client` object.
        """
        
        try:
            cursor = conexion.cursor()
            sql = """SELECT Nombre, Primer_Apellido, Segundo_Apellido FROM Cliente WHERE Cedula = %s"""
            cursor.execute(sql, (DocumentId))
            row = cursor.fetchone()

            if row:
                # Crear y devolver un objeto cliente
                return Client(
                    Name=row[0],
                    First_LastName=row[1],
                    Second_LastName=row[2],
                )
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener cliente por cédula: {ex}")
            return None
    

    @classmethod
    def disableClient(cls, conection, clientId):
        """
            Disables a client by setting their status to 0 (inactive) in the database.

            This method executes an SQL query to update the `Estado` (status) of a client 
            to 0 (inactive) in the `Cliente` table based on the provided `clientId`. 
            If the update is successful, it commits the transaction and returns `True`. 
            If no rows are affected or an error occurs, it rolls back the transaction and returns `False`.

            Parameters:
            conection (obj): The database connection object.
            clientId (str): The client's ID (Cedula) to disable.

            Returns:
            bool: `True` if the client was successfully disabled, 
                `False` if no client was updated or an error occurred.

            Exceptions:
            - Exception: Captures any general errors that may occur during the update 
            process, such as issues with the SQL query or database connection.
        """

        if clientId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Cliente SET Estado = 0  WHERE Cedula = %s"""
                cursor.execute(sql, (clientId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar el cliente.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar un cliente {ex}")
                conection.rollback()
                return False
        else:
            return False
        
    @classmethod
    def ableClient(cls, conection, clientId):
        """
            Re-enables a client by setting their status to 1 (active) in the database.

            This method executes an SQL query to update the `Estado` (status) of a client 
            to 1 (active) in the `Cliente` table based on the provided `clientId`. 
            If the update is successful, it commits the transaction and returns `True`. 
            If no rows are affected or an error occurs, it rolls back the transaction and returns `False`.

            Parameters:
            conection (obj): The database connection object.
            clientId (str): The client's ID (Cedula) to re-enable.

            Returns:
            bool: `True` if the client was successfully re-enabled, 
                `False` if no client was updated or an error occurred.

            Exceptions:
            - Exception: Captures any general errors that may occur during the update 
            process, such as issues with the SQL query or database connection.
        """

        if clientId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Cliente SET Estado = 1  WHERE Cedula = %s"""
                cursor.execute(sql, (clientId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar el cliente.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar un cliente {ex}")
                conection.rollback()
                return False
        else:
            return False
    
    @classmethod
    def getDataClient(cls, request):
        """
            Extracts client data from a form request and creates a `Client` object.

            This method retrieves client-related information from the form data in 
            the provided `request` object, processes the necessary fields (e.g., 
            date of birth to calculate age), and returns a `Client` object populated 
            with the extracted data.

            Parameters:
            request (obj): The form request object containing the client data.

            Returns:
            Client: A `Client` object with the data extracted from the form.

            Notes:
            - The date of birth is expected to be in the format "YYYY-MM-DD", 
            and the method calculates the age based on the current year and the 
            client's date of birth.
            - If any fields are missing or in an incorrect format, the method 
            assumes the form is well-validated beforehand, or additional error handling 
            can be added as needed.
        """

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

        return Client(documentId, name, firstLastName, secondLastName, Date_Birth, age, mail, phone, None, ocupation, emergencyPhone, adress, None, ailments, limitation, None, None)


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
            if not client.Name.isalpha():
                return "El nombre no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el nombre."
        
        #Validation for firstLastName
        if client.First_LastName != None:
            if not client.First_LastName.isalpha():
                return "El apellido 1 no debe contener números o caracteres especiales."
        else:
            return "Debe ingresar el apellido 1."
        
        #Validation for secondLastName
        if client.Second_LastName != None:
            if not client.Second_LastName.isalpha():
                return "El apellido 2 no debe contener números o caracteres especiales."
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
        
        
        
    
    @classmethod
    def get_Notifications(cls, conexion):
        """
            Retrieves all notifications from the `notificacion` table in the database.

            This method executes an SQL query to fetch all rows from the `notificacion` table, 
            which includes notification ID, subject, date, time, and status. 
            Each row is used to create a `Notification` object, and the list of notifications 
            is returned.

            Parameters:
            conexion (obj): The database connection object.

            Returns:
            list: A list of `Notification` objects containing the notifications from the database.
            - If an error occurs, an empty list is returned.

            Exceptions:
            - Exception: Catches any errors that occur during the database query or connection.
        """

        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Notificacion, Asunto, Fecha, Hora, Estado FROM notificacion"
            cursor.execute(sql)
            rows = cursor.fetchall()
            notifications = []
            for row in rows:
                notification = Notification(row[0], row[1],row[2], row[3],row[4])
                notifications.append(notification)
            return notifications
        except Exception as ex:
            print(f"Error en get_notifications: {ex}")
            return []