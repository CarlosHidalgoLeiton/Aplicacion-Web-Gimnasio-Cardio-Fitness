from .entities.Client import cliente

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
                client = cliente(
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
            clientes = []
            for row in rows:
                cliente = {
                    'Cedula': row[0],
                    'Nombre': row[1],
                    'Primer_Apellido': row[2],
                    'Segundo_Apellido': row[3],
                    'Ocupacion': row[4]
                }
                clientes.append(cliente)
            return clientes
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None
        
    @classmethod
    def get_cliente_by_cedula(cls, conexion, cedula):
        try:
            cursor = conexion.cursor()
            sql = """SELECT Cedula, Nombre, Primer_Apellido, Segundo_Apellido, Fecha_Nacimiento, Edad, Correo, 
                     Telefono, FechaInscripcion, Ocupacion, TelefonoEmergencia, Direccion, FechaIngreso, 
                     Padecimientos, Limitacion, VencimientoMembresia, Estado, ID_Membresia 
                     FROM Cliente WHERE Cedula = %s"""
            cursor.execute(sql, (cedula,))
            row = cursor.fetchone()

            if row:
                # Crear y devolver un objeto cliente
                return cliente(
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
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener cliente por cédula: {ex}")
            return None