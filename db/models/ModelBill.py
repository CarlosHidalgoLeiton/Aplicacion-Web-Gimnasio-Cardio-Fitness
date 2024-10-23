from datetime import datetime, timedelta
import re
from .entities.Bill import Bill
from .entities.Client import Client
class ModelBill:

    @classmethod
    def insertTrainerBill(cls, conection, bill):
        if bill != None:
            try:
                bill.EntityType = 'Entrenador'
                bill.Type = 'Pago Entrenador'
                date = datetime.now()
                bill.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Factura (Monto, Tipo, Descripcion, Fecha, TipoEntidad, ID_Entidad, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (bill.Amount, bill.Type, bill.Description, date, bill.EntityType, bill.ID_Entity, bill.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Factura creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la factura.")
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelBill insertTrainerBill: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelBill insertTrainerBill: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
        
    @classmethod
    def insertGeneralBill(cls, conection, bill):
        if bill != None:
            try:
                bill.Type = 'Pago General'
                date = datetime.now()
                bill.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Factura (Monto, Tipo, Descripcion, Fecha, Estado)
                VALUES (%s, %s, %s, %s, %s)"""
                cursor.execute(sql, (bill.Amount, bill.Type, bill.Description, date, bill.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Factura creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la factura.")
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelBill insertTrainerBill: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelBill insertTrainerBill: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
        
    @classmethod
    def getDataTrainerBill(cls, request):
        ID_Entity = request.form['DocumentIdTrainer']
        Amount = request.form['AmountTrainerBill']
        Description = request.form['Description']

        return Bill(None, Amount, None, Description, None, None, ID_Entity, None)

    @classmethod
    def getDataGeneralBill(cls, request):
        Amount = request.form['AmountGeneralBill']
        Description = request.form['Description']

        return Bill(None, Amount, None, Description, None, None, None, None)

    @classmethod
    def validateDataFormTrainer(cls, bill):
        
        if not bill.ID_Entity:
            return "Debe seleccionar el entrenador."
        
        if bill.Amount != None:
            if "-" in bill.Amount or not bill.Amount.isdigit(): #Valida que sea alfabetico y que no tenga un "-" 
                return "El monto ingresado no es válido."
        else:
            return "Debe de ingresar el monto."
        
        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    
    @classmethod
    def validateDataFormGeneral(cls, bill):
        
        if bill.Amount != None:
            if "-" in bill.Amount and not any( m.isalpha() for m in bill.Amount): #Valida que sea alfabetico y que no tenga un "-" 
                return "El monto ingresado no es válido."
        else:
            return "Debe de ingresar el monto."
        
        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    
    @classmethod
    def getDataGeneralBill(cls, request):
        Amount = request.form['AmountGeneralBill']
        Description = request.form['Description']

        return Bill(None, Amount, None, Description, None, None, None, None)
    
    @classmethod
    def get_all(cls, conection):
        try:
            cursor = conection.cursor()
            sql = "SELECT ID_Factura, Monto, Fecha, Estado FROM Factura"
            cursor.execute(sql)
            rows = cursor.fetchall()
            bills = []
            for row in rows:
                bill = {
                    'ID_Bill': row[0],
                    'Amount': row[1],
                    'Date': row[2],
                    'State': row[3]
                }
                bills.append(bill)
            return bills
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None

    @classmethod
    def getBill(cls, conection, ID_Bill):
        try:
            cursor = conection.cursor()
            sql = "SELECT ID_Factura, Monto, Fecha, Tipo, Descripcion, TipoEntidad, ID_Entidad FROM Factura WHERE ID_Factura = (%s)"
            cursor.execute(sql, (ID_Bill))
            row = cursor.fetchone() 
            if row:
                return Bill(
                    ID_Bill= row[0],
                    Amount= row[1],
                    Date= row[2],
                    Type= row[3],
                    Description= row[4],
                    EntityType= row[5],
                    ID_Entity= row[6]
                )
            return None
        except Exception as ex:
            print(f"Error en getBill: {ex}")
            return None


    @classmethod
    def insertProductBill(cls, conection, bill):
        if bill != None:
            try:
                bill.EntityType = 'Producto'
                bill.Type = 'Pago Producto'
                date = datetime.now()
                bill.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Factura (Monto, Tipo, Descripcion, Fecha, TipoEntidad, ID_Entidad, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (bill.Amount, bill.Type, bill.Description, date, bill.EntityType, bill.ID_Entity, bill.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Factura creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la factura.")
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelBill insertProductBill: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelBill insertProductBill: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
    
    @classmethod
    def getDataProductBill(cls, request):
        ID_Entity = request.form['DocumentIdProduct']
        Amount = request.form['AmountProductBill']
        Description = request.form['Description']

        return Bill(None, Amount, None, Description, None, None,ID_Entity, None)
    

    @classmethod
    def validateDataFormProduct(cls, bill):
        
        if not bill.ID_Entity:
            return "Debe seleccionar el producto."
        
        if bill.Amount:
            # Remueve cualquier espacio en blanco alrededor del monto
            amount = bill.Amount.strip()
    
            # Verifica si el monto comienza con el signo de colones (₡) y quítalo para validar los números
            if amount.startswith("₡"):
                amount = amount[1:].strip()  # Elimina el símbolo de colón

            # Valida que el monto no contenga un "-" y que el resto sea un número
            try:
                amount_float = float(amount)  # Intenta convertir a número decimal
                if amount_float < 0:
                    return "El monto ingresado no es válido."
                
                # Actualiza el valor de bill.Amount con el monto limpio
                bill.Amount = amount_float  # Sobrescribimos el valor limpio sin el símbolo
            except ValueError:
                return "El monto ingresado no es válido."
        else:
            return "Debe ingresar un monto."


        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    @classmethod
    def insertMembershipBill(cls, conection, bill):
        if bill != None:
            try:
                bill.EntityType = 'Membresia'
                bill.Type = 'Pago Membresia'
                date = datetime.now()
                bill.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Factura (Monto, Tipo, Descripcion, Fecha, TipoEntidad, ID_Entidad, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (bill.Amount, bill.Type, bill.Description, date, bill.EntityType, bill.ID_Entity, bill.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Factura creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la factura.")
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelBill insertMembershipBill: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelBill insertMembershipBill: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
        

    @classmethod
    def getDataMembershipBill(cls, request):
        ID_Entity = request.form['DocumentIdMembresia']
        Amount = request.form['AmountMembershipBill']
        Description = request.form['Description']

        return Bill(None, Amount, None, Description, None, None,ID_Entity, None)
    
    @classmethod
    def validateDataFormMembership(cls, bill):
        
        if not bill.ID_Entity:
            return "Debe seleccionar el producto."
        
        if bill.Amount:
            # Remueve cualquier espacio en blanco alrededor del monto
            amount = bill.Amount.strip()
    
            # Verifica si el monto comienza con el signo de colones (₡) y quítalo para validar los números
            if amount.startswith("₡"):
                amount = amount[1:].strip()  # Elimina el símbolo de colón

            # Valida que el monto no contenga un "-" y que el resto sea un número
            try:
                amount_float = float(amount)  # Intenta convertir a número decimal
                if amount_float < 0:
                    return "El monto ingresado no es válido."
                
                # Actualiza el valor de bill.Amount con el monto limpio
                bill.Amount = amount_float  # Sobrescribimos el valor limpio sin el símbolo
            except ValueError:
                return "El monto ingresado no es válido."
        else:
            return "Debe ingresar un monto."


        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    
    @classmethod
    def updateClientMembership(cls, conection, client):
        try:
            # Actualizar el cliente en la base de datos
            cursor = conection.cursor()
            sql = """
            UPDATE Cliente
            SET ID_Membresia = %s, VencimientoMembresia = %s, FechaIngreso = %s
            WHERE Cedula = %s
            """
            cursor.execute(sql, (client.Membership_ID, client.ExpirationMembership, client.Entry_Date, client.DocumentId))
            conection.commit()
            
            if cursor.rowcount > 0:
                print("Cliente actualizado correctamente.")
                return True
            else:
                print("No hubo cambios en los datos del cliente.")
                return True
        except Exception as ex:
            print(f"Error en updateClientMembership: {ex}")
            conection.rollback()
            return "Error"
        
        
    @classmethod
    def getMembershipday(cls, connection, membershipId):
        try:
            if connection is None:
                print("La conexión a la base de datos no está establecida.")

            cursor = connection.cursor()

            # membershipId = int(membershipId.strip())
            print(f"Buscando tipo de membresía con ID: {membershipId}")  # Depuración

            # Consulta SQL para obtener el tipo de membresía usando el ID
            sql = "SELECT Duracion_Dias FROM Membresia WHERE ID_Membresia = %s"
            cursor.execute(sql, (membershipId))
            result = cursor.fetchone()
            print(f"Resultado de la consulta: {result}")  # Verifica lo que se devuelve


            if result:
                membership_type = result[0]  # Aquí capturas el tipo de membresía
                return membership_type
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener el tipo de membresía: {ex}")
            return None
        finally:
            cursor.close()


    @classmethod
    def getDataMembershipClient(cls, connection, request):
        documentId = request.form['DocumentIdClient']
        membershipId = request.form['DocumentIdMembresia']
        membership_days = cls.getMembershipday(connection,membershipId)

        if membership_days is None:
            return "Tipo de membresía no encontrado"
        # Obtener la fecha actual
        fecha_ingreso = datetime.now()

        # Calcular la fecha de vencimiento sumando los días de la membresía
        vencimiento_membresia = fecha_ingreso + timedelta(days=membership_days)


        # Retornar el objeto Client con la información necesaria
        return Client(
            documentId, None, None, None, None, None, None, None, 
            None, None, None, None, fecha_ingreso, None, None, 
            vencimiento_membresia, None, membershipId
        )
    
    classmethod
    def validateDataFormMembershipClient(client):
        # Validaciones del formulario
        if not client.DocumentId:
            return "Debe seleccionar un cliente."
        
        if not client.Membership_ID:
            return "Debe seleccionar una membresía."
        
        if not client.Entry_Date:
            return "No se logro obtener la fecha actual"
        
        if not client.ExpirationMembership:
            return "No se logro obtener la duracion"
        return True