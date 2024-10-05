from .entities.User import User
from .entities.Client import Client
from .entities.Trainer import Trainer
from db.conection import Conection
from datetime import datetime
import re

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
        cursor.execute("SELECT COUNT(*) FROM USUARIO WHERE Cedula = %s", (document_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    
    @classmethod
    def insertUser(cls, conexion, user):
        try:
            cursor = conexion.cursor()

            sql = """INSERT INTO USUARIO 
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
            sql = "SELECT * FROM Cliente WHERE NOT EXISTS (SELECT 1 FROM usuario WHERE usuario.Cedula = Cliente.Cedula) "
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
            sql = "SELECT * FROM Entrenador WHERE NOT EXISTS (SELECT 1 FROM usuario WHERE usuario.Cedula = Entrenador.Cedula) "
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
    def validateDataForm(cls, request):
        role = request.form['role']
        State = request.form['State']# Obtener el rol seleccionado
        DocumentId = None

        # Obtener DocumentId dependiendo del rol
        if role == 'admin':
            DocumentId = request.form['DocumentId']
        elif role == 'trainer':
            DocumentId = request.form['DocumentIdTrainer']
        elif role == 'client':
            DocumentId = request.form['DocumentIdClient']
        
        Password = request.form['Password']
        ConfirmPassword = request.form['ConfirmPassword']
        Email = request.form['Email']
        
        # Validación para DocumentId
        if DocumentId is None:
            return "Debe ingresar el número de cédula."
        
        if "-" not in DocumentId and not any(d.isalpha() for d in DocumentId):  # Valida que sea numérico y no contenga "-"
            if len(DocumentId) < 9:
                return "El número de cédula ingresado no es válido. Debe ingresar 9 dígitos."
        else:
            return "El número de cédula no debe contener letras ni caracteres especiales."
        
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
    