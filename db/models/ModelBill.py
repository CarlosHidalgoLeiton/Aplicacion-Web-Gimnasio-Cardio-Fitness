from datetime import datetime, timedelta, date
from collections import defaultdict
import re
from db.models.ModelProduct import ModelProduct
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
                bill.EntityType='General'
                bill.ID_Entity=0
                cursor = conection.cursor()
                sql = """INSERT INTO Factura (Monto, Tipo, TipoEntidad, ID_Entidad, Descripcion, Fecha, Estado)
                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (bill.Amount, bill.Type, bill.EntityType, bill.ID_Entity, bill.Description, date, bill.State))
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
            sql = "SELECT ID_Factura, Monto, Fecha, Tipo, Estado FROM Factura"
            cursor.execute(sql)
            rows = cursor.fetchall()
            bills = []
            for row in rows:
                bill = {
                    'ID_Bill': row[0],
                    'Amount': row[1],
                    'Date': row[2],
                    'Type': row[3],
                    'State': row[4]
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
    def insertProductBill(cls, conection, bill, lot):
        if bill != None:
            try:
                bill.EntityType = 'Producto'
                bill.Type = 'Pago Producto'
                date = datetime.now()
                bill.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Factura (Monto, Tipo, Descripcion, Fecha, TipoEntidad, ID_Entidad, Estado, Cantidad)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (bill.Amount, bill.Type, bill.Description, date, bill.EntityType, bill.ID_Entity, bill.State, bill.Lot))

                if cursor.rowcount > 0:
                    print(f"Factura creada exitosamente.")
                    cursor.close()
                    cursor = conection.cursor()
                    sql2 = "UPDATE Producto set Cantidad = (%s)"
                    cursor.execute(sql2, (lot))

                    if cursor.rowcount > 0:
                        print(f"Producto actualizado exitosamente.")
                        conection.commit()
                        return True
                    else:
                        conection.rollback()
                        return False
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
        Lot = request.form['Amount']

        return Bill(None, Amount, None, Description, None, None,ID_Entity, None, Lot)
    

    @classmethod
    def validateDataFormProduct(cls, bill):
        
        if bill.ID_Entity == "":
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
        
        if bill.Lot != None:
            if "-" in bill.Lot or not bill.Lot.isdigit(): #Valida que sea alfabetico y que no tenga un "-" 
                return "La cantidad ingresada no es válida."
        else:
            return "Debe de ingresar la cantidad."

        return True
    @classmethod
    def insertMembershipBill(cls, conection, bill):
        if bill != None:
            try:
                bill.EntityType = 'Cliente'
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
        ID_Entity = request.form['DocumentIdClient']
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
            SET ID_Membresia = %s, VencimientoMembresia = %s, FechaInscripcion = %s
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
    

    
    @classmethod
    def getStock(cls, conection, productId):
        cursor = conection.cursor()

        sql = "SELECT Cantidad FROM Producto WHERE ID_Producto = (%s)"
        
        cursor.execute(sql, (productId))
        result = cursor.fetchone()

        if result:
            amount = result[0]  # Aquí capturas el tipo de membresía
            return amount
        else:   
            return None
        
    @classmethod
    def validateStock(cls, stock, lot):
        try:
            if int(lot) < int(stock) :
                return True
            else:
                return False
        except Exception as ex:
            print(ex)
            return False

# ---------------Reportes----------------------



    @classmethod
    def get_ProductBills(cls, conection):
        try:
            cursor = conection.cursor()
            sql = "SELECT ID_Factura, Monto, Fecha, Tipo, Descripcion, TipoEntidad, ID_Entidad, Estado, Cantidad FROM Factura WHERE TipoEntidad = 'Producto'"
            cursor.execute(sql)
            rows = cursor.fetchall()
            bills_by_month = defaultdict(list)

            for row in rows:
                product_id = row[6]
                product = ModelProduct.get_product_by_id(conection, product_id)

               
                if product:
                    price = product.Price if product.Price is not None else 0  
                    bill = {
                        'ID_Bill': row[0],
                        'Amount': row[1],
                        'Date': row[2],
                        'Type': row[3],
                        'Description': row[4],
                        'EntityType': row[5],
                        'ID_Entity': product_id,
                        'ProductCode': product.ID_Product,
                        'Price': product.Price,
                        'ProductName': product.Name,
                        'QuantitySold': row[8],
                        'TotalSold': row[8] * price,  
                    }
                    month_year = row[2].strftime('%Y-%m')
                    bills_by_month[month_year].append(bill)

            cursor.close()
            return bills_by_month
        except Exception as ex:
            print(f"Error en get_ProductBills: {ex}") 
            return None


    @classmethod
    def get_reports(cls, connection, group_by):
        try:
            cursor = connection.cursor()
            
            group_sql = {
                'diaria': "DATE(Fecha) AS group_key",  
                'semanal': "YEARWEEK(Fecha, 1) AS group_key",  
                'mensual': "DATE_FORMAT(Fecha, '%Y-%m') AS group_key"  
            }
            
            if group_by not in group_sql:
                raise ValueError("Tipo de reporte no válido.")
            
            sql = f"""
                SELECT {group_sql[group_by]}, ID_Factura, Monto, Tipo, Descripcion, TipoEntidad, ID_Entidad, Estado, Fecha
                FROM Factura
                ORDER BY group_key
            """
            cursor.execute(sql)
            rows = cursor.fetchall()

            reports = {}
            for row in rows:
                group_key = row[0]

                
                if isinstance(group_key, (date, datetime)): 
                    group_key = group_key.strftime('%Y-%m-%d')  
                
                if group_key not in reports:
                    reports[group_key] = []

                report = {
                'ID_Factura': row[1],
                'Monto': row[2],
                'Tipo': row[3],
                'Descripcion': row[4],
                'TipoEntidad': row[5] if row[5] else 'Desconocido',  
                'ID_Entidad': row[6],
                'Estado': row[7],
                'Fecha': row[8]  
                }

                if row[5] == 'Cliente' or row[5] == 'Entrenador':
                    entity_sql = f"SELECT Cedula, Nombre FROM {row[5]} WHERE Cedula = %s"
                    cursor.execute(entity_sql, (row[6],))
                    entity_row = cursor.fetchone()
                    if entity_row:
                        report['Cedula'] = entity_row[0]
                        report['Nombre'] = entity_row[1]
                elif row[5] == 'Producto':
                    product_sql = "SELECT Nombre FROM Producto WHERE ID_Producto = %s"
                    cursor.execute(product_sql, (row[6],))
                    product_row = cursor.fetchone()
                    if product_row:
                        report['Producto'] = product_row[0]

                reports[group_key].append(report)

            return reports

        except Exception as ex:
            print(f"Error en get_reports: {ex}")
            return None











