from .entities.Routine import Routine
from datetime import datetime
from pymysql import IntegrityError

class ModelRoutine:

    @classmethod
    def insertRoutine(cls, conection, routine):
        if routine != None:
            try:
                routine.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Rutina ( ID_Cliente, ID_Entrenador, Indicaciones, Fecha, Estado)
                VALUES ( %s, %s, %s, %s, %s)"""
                cursor.execute(sql, ( routine.ClientId, routine.TrainerId, routine.Indications, routine.Date, routine.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Rutina {routine.RoutineId} creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la rutina.")
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelRoutin insertRoutin: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelRoutin insertRoutin: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
    
    @classmethod
    def updateRoutine(cls, conection, routine, id):
        if routine != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Routine SET ID_Rutina = %s, ID_Cliente = %s, ID_Entrenador = %s, Indicaciones = %s, Fecha = %s, Estado = %s WHERE ID_Rutina = %s"""
                cursor.execute(sql, (routine.RoutineId, routine.ClientId, routine.TrainerId, routine.Indications, routine.Date, routine.State, id))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Rutina {routine.RoutineId} actualizada exitosamente.")
                    return True
                else:
                    print("No se pudo actualizar la rutina.")
                    return "Error"

            except IntegrityError as ex:
                print(f"Error en ModelCLiente updateRoutin: {ex}")
                conection.rollback()
                return "Primary"
            except BaseException as ex:
                print(f"Error en ModelRoutin updateRoutin: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelRoutin updateRoutin: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"

    @classmethod
    def get_all(cls, conexion, ID_Cliente):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Rutina, ID_Cliente, ID_Entrenador, Indicaciones, Fecha, Estado FROM Rutina WHERE ID_Cliente = %s"
            cursor.execute(sql, (ID_Cliente,))
            rows = cursor.fetchall()
            routines = []
            
            for row in rows:
                routine = Routine(
                    RoutineId=row[0],
                    ClientId=row[1],
                    TrainerId=row[2],
                    Indications=row[3],
                    Date=row[4],
                    State=row[5],
                )
                routines.append(routine)
            
            return routines
        
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None
        
    @classmethod
    def getDataRoutine(cls, request):
        ClientId = request.form['ClientId']
        TrainerId = request.form['TrainerId']
        Indications = request.form['Indications']
        Date = datetime.now()

        return Routine(None, ClientId, TrainerId, Indications, Date)

    @classmethod
    def validateDataForm(cls, routine):

        #Validation for Client
        if routine.ClientId == None:
            return "Debe contener ID cliente"
        
        #Validation for Trainer
        if routine.TrainerId == None:
            return "Debe contener ID de entrenador"
        
        #Validation for Indications
        if routine.Indications == None:
            return "Debe ingresar las indicaciones."
    
        return True
        