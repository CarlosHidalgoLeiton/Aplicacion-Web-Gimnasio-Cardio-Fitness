from .entities.Client import client

class ModelCliente:

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
                client = client(
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
                return client(
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