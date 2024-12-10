from .entities.User import User
from .entities.Client import Client
from .entities.Notification import Notification
from .entities.Trainer import Trainer
from db.conection import Conection
from datetime import datetime
import re
import secrets

class ModelUser:

    @classmethod
    def login(cls, user, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Contrasena, Estado, Rol FROM Usuario WHERE Cedula = %s"
            cursor.execute(sql, (user.DocumentId))
            row = cursor.fetchone()
            if row is not None:
                if row[3] != 0:
                    if User.verifyPassword(row[2], user.Password):
                        return User(row[0], row[1], row[2], None, row[4])
                    else:
                        return "Password"
                else:
                    return 'Inactive'
            else:
                return "Invalid User"
        except BaseException as ex:
            print(f"Error en ModelUser login: {ex}")
            return "DataBase"
        except Exception as ex:
            print(f"Error en ModelUser login: {ex}")
            return None


    @classmethod
    def get_by_id(cls, conexion, id):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Rol, Correo FROM Usuario WHERE ID_Usuario = %s"
            cursor.execute(sql, (id))
            row = cursor.fetchone()
            print(row)
            if row is not None:
                return User(row[0], row[1], None, None, row[2],None,row[3])
            return None
        except Exception as ex:
            print(f"Error en ModelUser en get_by_id: {ex}")
            return None

    #VERIFICAR SI EXISTE LA CEDULA DE ADMIN EN USUARIO
    @classmethod
    def document_exists(cls, conexion, document_id):
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Usuario WHERE Cedula = %s", (document_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    
    @classmethod
    def insertUser(cls, conexion, user):
        try:
            cursor = conexion.cursor()

            sql = """INSERT INTO Usuario
                    (`Cedula`, `Contrasena`, `Estado`, `Rol`, `FechaCreacion`, `Correo`) 
                    VALUES (%s, %s, %s, %s, %s, %s)"""
            
            cursor.execute(sql, (user.DocumentId, user.Password, user.State, user.role, user.CreationDate, user.Email))

            conexion.commit()
            if cursor.rowcount > 0:
                print(f"Usuario {user.DocumentId} creado exitosamente.")
                return True
            else:
                print("No se pudo crear el usuario.")
                return None  

        except Exception as ex:
            print(f"Error al crear usuario: {ex}")
            return None  
        finally:
            cursor.close()


    @classmethod
    def get_Users(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Estado, Rol FROM Usuario"
            cursor.execute(sql)
            rows = cursor.fetchall()
            users = []
            for row in rows:
                user = User(row[0], row[1], None ,row[2], row[3])
                users.append(user)
            return users
        except Exception as ex:
            print(f"Error en get_Users: {ex}")
            return []

    #SE TRRAEN LOS CLIENTES POR EL FILTRO (EXISTE EN USUARIO O NO )
    @classmethod
    def get_Clients(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT * FROM Cliente WHERE NOT EXISTS (SELECT 1 FROM Usuario WHERE Usuario.Cedula = Cliente.Cedula) "
            cursor.execute(sql)
            rows = cursor.fetchall()
            clients = []
            for row in rows:
                client = Client(
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
                clients.append(client)
            return clients
        except Exception as ex:
            print(f"Error al obtener clientes: {ex}")
            return None

    #SE TRRAEN LOS ENTRENADORES POR EL FILTRO (EXISTE EN USUARIO O NO )
    @classmethod
    def get_Trainers(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT * FROM Entrenador WHERE NOT EXISTS (SELECT 1 FROM Usuario WHERE Usuario.Cedula = Entrenador.Cedula) "
            cursor.execute(sql)
            rows = cursor.fetchall()
            trainers = []
            for row in rows:
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
                trainers.append(trainer)
            return trainers
        except Exception as ex:
            print(f"Error al obtener los entrenadores: {ex}")
            return None

    @classmethod
    def get_User(cls, conexion, documentId):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Usuario, Cedula, Estado, Rol, Correo FROM Usuario WHERE Cedula = %s"
            cursor.execute(sql, (documentId,))
            row = cursor.fetchone()
            if row is not None:
                return User(row[0], row[1], None, row[2], row[3], None, row[4])  
            return None
        except Exception as ex:
            print(f"Error en get_User: {ex}")
            return None
        
    @classmethod
    def get_UserU(cls, conexion, documentId):
        try:
            with conexion.cursor() as cursor:
                sql = "SELECT ID_Usuario, Cedula, Contrasena, Estado, Rol, FechaCreacion, Correo FROM Usuario WHERE Cedula = %s"
                cursor.execute(sql, (documentId,))
                row = cursor.fetchone()
                if row is not None:
                    return User(row[0], row[1], row[2], row[3], row[4], row[5],row[6])  
                return None
        except Exception as ex:
            print(f"Error en get_User: {ex}")
            return None

    @classmethod
    def validateDataForm(cls, request):
        role = request.form['role']
        State = request.form['State']# Obtener el rol seleccionado
        DocumentId = None

        # Obtener DocumentId dependiendo del rol
        if role == 'Admin':
            DocumentId = request.form['DocumentId']
        elif role == 'Trainer':
            DocumentId = request.form['DocumentIdTrainer']
        elif role == 'Client':
            DocumentId = request.form['DocumentIdClient']
        
        Password = request.form['Password']
        ConfirmPassword = request.form['ConfirmPassword']
        Email = request.form['Email']
        
        # Validación para DocumentId
        if DocumentId is None:
            return "Debe ingresar el número de cédula."
        
        # Verificar si la cédula ya existe en la base de datos
        conexion = Conection.conectar()
        if conexion is None:
            return "Error en la conexión a la base de datos."
        
        if ModelUser.document_exists(conexion, DocumentId):
            Conection.desconectar()
            return "El número de cédula ya está registrado."
        
        Conection.desconectar()
    
        # Validación para contraseña
        if Password is None or ConfirmPassword is None:
            return "Debe ingresar la contraseña y su confirmación."

        if Password != ConfirmPassword:
            return "Las contraseñas no coinciden."

        if len(Password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."

        if not re.search(r"[A-Z]", Password):
            return "La contraseña debe contener al menos una letra mayúscula."

        if not re.search(r"[a-z]", Password):
            return "La contraseña debe contener al menos una letra minúscula."

        if not re.search(r"[0-9]", Password):
            return "La contraseña debe contener al menos un número."

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", Password):
            return "La contraseña debe contener al menos un carácter especial."
        
        hashPassword = User.generate_password_hash(Password)
        
        # Validación para correo
        if Email is None:
            return "Debe ingresar el correo."
        
        expression = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Validar formato de correo
        if not re.match(expression, Email):
            return "El correo ingresado no es válido."

        # Si todas las validaciones pasan, devuelve el objeto User
        return User(None, DocumentId, hashPassword, State, role, datetime.now(), Email)
    
    @classmethod
    def validateDataFormUpdate(cls, request, user):
        DocumentId = request.form['DocumentId']
        State = request.form['State']
        role = request.form['Role']
        Password = request.form['Password']
        ConfirmPassword = request.form['ConfirmPassword']
        Email = request.form['Email']

        
        if not DocumentId:
            return "Debe seleccionar el cliente."
        
        conexion = Conection.conectar()
        if conexion is None:
            return "Error en la conexión a la base de datos."
        
        if ModelUser.document_exists(conexion, DocumentId) and DocumentId != user.DocumentId:
            Conection.desconectar()
            return "El número de cédula ya está registrado por otro usuario."
        
        Conection.desconectar()

        # Validación para contraseña
        if Password and ConfirmPassword:
            if Password != ConfirmPassword:
                return "Las contraseñas no coinciden."

            if len(Password) < 8:
                return "La contraseña debe tener al menos 8 caracteres."

            if not re.search(r"[A-Z]", Password):
                return "La contraseña debe contener al menos una letra mayúscula."

            if not re.search(r"[a-z]", Password):
                return "La contraseña debe contener al menos una letra minúscula."

            if not re.search(r"[0-9]", Password):
                return "La contraseña debe contener al menos un número."

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", Password):
                return "La contraseña debe contener al menos un carácter especial."
            
            hashPassword = User.generate_password_hash(Password)
        else:
            hashPassword = user.Password  # Mantener la contraseña actual si no se proporciona una nueva
        
        # Validación para correo
        if not Email:
            return "Debe ingresar el correo."
        
        expression = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Validar formato de correo
        if not re.match(expression, Email):
            return "El correo ingresado no es válido."

        # Si todas las validaciones pasan, devuelve el objeto User
        return User(user.id, DocumentId, hashPassword, State, role, user.CreationDate, Email)

    @classmethod
    def update_User(cls, conexion, user, id):
        try:
            cursor = conexion.cursor()
            sql = """UPDATE Usuario 
                    SET Cedula = %s, Contrasena = %s, Estado = %s, Rol = %s, FechaCreacion = %s, Correo = %s
                    WHERE ID_Usuario  = %s"""
            
            cursor.execute(sql, (user.DocumentId, user.Password, user.State, user.role, user.CreationDate, user.Email, id))
            conexion.commit()
            return True
        except Exception as ex:
            print(f"Error en update_User: {ex}")
            return False


    @classmethod
    def disableUser(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Usuario SET Estado = 0  WHERE Cedula = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar el usuario.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar un usuario {ex}")
                conection.rollback()
                return False
        else:
            return False
        
    @classmethod
    def ableUser(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Usuario SET Estado = 1  WHERE Cedula = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar el usuario.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar un usuario {ex}")
                conection.rollback()
                return False
        else:
            return False


    @classmethod
    def get_Notifications(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Notificacion, Asunto, Fecha, Hora, Estado FROM Notificacion"
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

    @classmethod
    def getDataNotification(cls, request):
        Subject = request.form['Subject']
        Date = request.form['Date']
        Hour = request.form['Hour']
        return Notification(None,Subject, Date, Hour, None)

    @classmethod
    def insertNotification(cls, conexion, Notification):
        try:
            cursor = conexion.cursor()
            Notification.State = 1
            
            sql = """INSERT INTO `Notificacion` (`Asunto`, `Fecha`, `Hora`, `Estado`)  
                    VALUES (%s, %s, %s, %s)"""
            
            cursor.execute(sql, (Notification.Subject, Notification.Date, Notification.Hour, Notification.State))
            
            conexion.commit()
            
            if cursor.rowcount > 0:
                print("Notificación creada exitosamente.")
                return True
            else:
                print("No se pudo crear la Notificación.")
                return None

        except Exception as ex:
            print(f"Error al crear Notificación: {ex}")
            return None

        finally:
            if cursor:
                cursor.close()

    
    @classmethod
    def getEmail(cls, conection, DocumentId):
        if DocumentId:
            try:
                cursor = conection.cursor()
                sql = "SELECT Correo FROM Usuario WHERE Cedula = %s"
                cursor.execute(sql, (DocumentId))
                row = cursor.fetchone()

                if row:
                    email = row[0]
                    return email
                else:
                    return None
            except Exception as ex:
                print(f"Error en get_notifications: {ex}")
                return None
    
    @classmethod
    def generateToken(cls):
        token = secrets.token_urlsafe(32)

        return token
    
    @classmethod
    def tokenExist(cls, conection, DocumentId):
        try:
            cursor = conection.cursor()
            sql = "SELECT CedulaUser FROM TokenUsuario WHERE CedulaUser = %s"
            cursor.execute(sql, (DocumentId))
            row = cursor.fetchone()

            if row:
                return True
            else:
                return False
        except Exception as ex:
            print(f"Error en tokenExist: {ex}")
            return False

    @classmethod
    def saveToken(cls, conection, DocumentId, token, action):
        if DocumentId:
            if action == "save":
                currentTime = datetime.datetime.now()

                expiration = currentTime + datetime.timedelta(minutes=30)

                try:
                    cursor = conection.cursor()

                    sql = """INSERT INTO TokenUsuario
                            (`CedulaUser`, `Token`, `Expiration`) 
                            VALUES (%s, %s, %s)"""
                    
                    cursor.execute(sql, (DocumentId, token, expiration))

                    conection.commit()
                    if cursor.rowcount > 0:
                        print(f"Token {token} almacenado exitosamente.")
                        return True
                    else:
                        print("No se pudo guardar el token.")
                        return False  

                except Exception as ex:
                    print(f"Error al almacenar el token: {ex}")
                    return False  
                finally:
                    cursor.close()

            if action == "update":
                currentTime = datetime.datetime.now()

                expiration = currentTime + datetime.timedelta(minutes=30)

                try:
                    cursor = conection.cursor()

                    sql = """Update TokenUsuario SET `CedulaUser` = %s, `Token` = %s, `Expiration` =%s WHERE CedulaUser = %s"""
                    
                    cursor.execute(sql, (DocumentId, token, expiration, DocumentId))

                    conection.commit()
                    if cursor.rowcount > 0:
                        print(f"Token {token} actualizado exitosamente.")
                        return True
                    else:
                        print("No se pudo actualizar el token.")
                        return False  

                except Exception as ex:
                    print(f"Error al actualizar el token: {ex}")
                    return False  
                finally:
                    cursor.close()


    @classmethod
    def getDataPasswords(cls,request):
        password1 = request.form['password1']
        password2 = request.form['password2']
        return {"password1": password1, "password2": password2}


    @classmethod
    def update_Password(cls, conexion, password, DocumentId):
        try:
            cursor = conexion.cursor()
            sql = "UPDATE Usuario SET Contrasena = %s  WHERE Cedula = %s"
            
            cursor.execute(sql, (password,DocumentId))
            conexion.commit()
            return True
        except Exception as ex:
            print(f"Error en update_Password: {ex}")
            return False


    @classmethod               
    def changePassword(cls, conection,DocumentId, Token, passwords):
        try:
            if(DocumentId is None or DocumentId == ""):

                return "No se pudo recuperar la información del cliente. Por favor, inténtelo de nuevo más tarde.";
            else:

                cursor = conection.cursor()
                sql = "SELECT Token FROM TokenUsuario WHERE CedulaUser = %s"
                cursor.execute(sql, (DocumentId))
                row = cursor.fetchone()

                    
                if row:
                    if (Token == row[0]):
                        sqlDate ="SELECT Expiration FROM TokenUsuario WHERE CedulaUser = %s"
                        cursor.execute(sqlDate, (DocumentId))
                        rowDate = cursor.fetchone()
                        current_time = datetime.datetime.now()
                        if rowDate[0] > current_time:

                            if passwords["password1"] == "" or passwords["password2"] == "":
                                return "Por favor, asegúrate de ingresar ambos campos de contraseña."

                            if passwords["password1"] != passwords["password2"]:
                                return "Las contraseñas no coinciden."

                            if len(passwords["password1"]) < 8:
                                return "La contraseña debe tener al menos 8 caracteres."

                            if not re.search(r"[A-Z]", passwords["password1"]):
                                return "La contraseña debe contener al menos una letra mayúscula."

                            if not re.search(r"[a-z]", passwords["password1"]):
                                return "La contraseña debe contener al menos una letra minúscula."

                            if not re.search(r"[0-9]", passwords["password1"]):
                                return "La contraseña debe contener al menos un número."

                            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", passwords["password1"]):
                                return "La contraseña debe contener al menos un carácter especial."
                            
                            hashPassword = User.generate_password_hash(passwords["password1"])

                            update = cls.update_Password(conection, hashPassword,DocumentId)
                            if update is not True:
                                return "No se pudo actualizar la contraseña. Por favor, inténtelo de nuevo más tarde."
                            elif (update == True):
                                return"El cambio de contraseña fue exitosa"
                    else:
                        return "El tiempo ha expirado. Por favor, intente nuevamente."
                else:
                    return "No se pudo obtener la información del cliente. Por favor, intente nuevamente."

        except Exception as ex:
            return "Ocurrió un error en el sistema. Por favor, intenta nuevamente más tarde."

            

