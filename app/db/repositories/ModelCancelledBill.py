from .entities.CancelledBill import CancelledBill
from datetime import datetime
from pymysql import IntegrityError


class ModelCancelledBill():

    @classmethod
    def insertCancelledBill(cls, conection, cancelledBill):
        if cancelledBill != None:
            try:
                cancelDate = datetime.now()
                cursor = conection.cursor()
                sql = """INSERT INTO FacturaAnulada (Motivo, FechaAnulacion, ID_Factura)
                VALUES (%s, %s, %s)"""
                cursor.execute(sql, (cancelledBill.Motive, cancelDate, cancelledBill.ID_Bill))
                conection.commit()

                if cursor.rowcount > 0:
                    cursor.close()
                    state = 0
                    cursor = conection.cursor()
                    sql = """UPDATE Factura SET Estado = (%s) WHERE ID_Factura = (%s)"""
                    cursor.execute(sql, (state, cancelledBill.ID_Bill))
                    conection.commit()

                    if cursor.rowcount > 0:
                        print(f"Factura anulada correctamente")
                        return True
                    else:
                        print("No se pudo cambiar el estado de la factura.")
                        conection.rollback()
                        return "Error"
                else:
                    print("No se pudo crear la factura anulada.")
                    conection.rollback()
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelCancelledBill insertCancelledBill: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelCancelledBill insertCancelledBill: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
    
    @classmethod
    def getDataCanceledBill(cls, request):
        motive = request.form['Motive']
        idBill = request.form['ID_Bill']

        return CancelledBill(None, motive, None, idBill)
    
    @classmethod
    def validateDataForm(cls, cancelledBill):
        if cancelledBill.Motive == None:
            return "Debe ingresar el motivo de la anulación de la factura."
        
        if cancelledBill.ID_Bill == None:
            return "No se encontró el número de factura."
        
        return True
    
    
    @classmethod
    def getCancelBill(cls, conection, ID_Bill):
        try:
            cursor = conection.cursor()
            sql = "SELECT Motivo, FechaAnulacion FROM FacturaAnulada WHERE ID_Factura = (%s)"
            cursor.execute(sql, (ID_Bill))
            row = cursor.fetchone() 
            if row:
                return CancelledBill(
                    Motive= row[0],
                    CancelledDate= row[1],
                )
            return None
        except Exception as ex:
            print(f"Error en getCancelBill: {ex}")
            return None