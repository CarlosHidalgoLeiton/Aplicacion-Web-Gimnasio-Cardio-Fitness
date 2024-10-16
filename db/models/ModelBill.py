from datetime import datetime
import re
from .entities.Bill import Bill

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
    def getDataTrainerBill(cls, request):
        ID_Entity = request.form['DocumentIdTrainer']
        Amount = request.form['AmountTrainerBill']
        Description = request.form['Description']

        return Bill(None, Amount, None, Description, None, None, ID_Entity, None)

    @classmethod
    def validateDataFormTrainer(cls, bill):
        
        if bill.ID_Entity == None:
            return "Debe seleccionar el entrenador."
        
        if bill.Amount != None:
            if "-" in bill.Amount and any( m.isalpha() for m in bill.Amount): #Valida que sea alfabetico y que no tenga un "-" 
                return "El monto ingresado no es válido."
        else:
            return "Debe de ingresar el monto."
        
        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    
    @classmethod
    def getDataGeneralBill(cls, request):
        Amount = request.form['AmountTrainerBill']
        Description = request.form['Description']

        return Bill(None, Amount, None, Description, None, None, None, None)

    @classmethod
    def validateDataFormTrainer(cls, bill):
        
        if bill.Amount != None:
            if "-" in bill.Amount and any( m.isalpha() for m in bill.Amount): #Valida que sea alfabetico y que no tenga un "-" 
                return "El monto ingresado no es válido."
        else:
            return "Debe de ingresar el monto."
        
        if bill.Description == None:
            return "Debe de ingresar la descripción."
        
        return True
    
    @classmethod
    def get_all(cls, conexion):
        try:
            cursor = conexion.cursor()
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


