from .entities.Session import Session
from datetime import datetime
from pymysql import IntegrityError

class ModelSession:

    @classmethod
    def insertSession(cls, conection, session):
        if session != None:
            try:
                cursor = conection.cursor()
                sql = """INSERT INTO Sesion (Indicaciones, Ejercicios, ID_Rutina)
                    VALUES (%s, %s, %s)"""
                cursor.execute(sql, (session.Indications, session.Exercises, session.Routine_ID))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Sesion {session.Name} creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la sesion.")
                    return "Error"
                
            except IntegrityError as ex:
                print(f"Error en ModelSession updateSession: {ex}")
                conection.rollback()
                return "Unique"
            except BaseException as ex:
                print(f"Error en ModelSession insertSession: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelSession insertSession: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
    
    @classmethod
    def updateSession(cls, conection, session, ID_Sesion):
        if session != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Sesion SET Indicaciones = %s, Ejercicios = %s, ID_Rutina = %s WHERE ID_Sesion = %s"""
                cursor.execute(sql, (session.Indications, session.Exercises, session.Routine_ID, ID_Sesion))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Sesion {session.Name} actualizada exitosamente.")
                    return True
                else:
                    print("No se pudo actualizar la sesion.")
                    return "Error"
                
            except IntegrityError as ex:
                print(f"Error en ModelSession updateSession: {ex}")
                conection.rollback()
                return "Unique"
            except BaseException as ex:
                print(f"Error en ModelSession updateSession: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelSession updateSession: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"

    @classmethod
    def get_all(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Sesion, Indicaciones, Ejercicios, ID_Rutina FROM Sesion"
            cursor.execute(sql)
            rows = cursor.fetchall()
            sessions = []
            for row in rows:
                session = Session(
                    Session_ID=row[0],
                    Indications=row[1],
                    Exercises=row[2],
                    Routine_ID=row[3],
                )
                sessions.append(session)
            return sessions
        
        except Exception as ex:
            print(f"Error in get_all: {ex}")
            return None
        
    @classmethod
    def get_sesssion_by_Routine(cls, conexion, routineId):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Sesion, Indicaciones, Ejercicios, ID_Rutina FROM Sesion WHERE ID_Rutina = %s "
            cursor.execute(sql, (routineId))
            rows = cursor.fetchall()
            sessions = []
            for row in rows:
                session = Session(
                    Session_ID=row[0],
                    Indications=row[1],
                    Exercises=row[2],
                    Routine_ID=row[3],
                )
                sessions.append(session)
            return sessions
        
        except Exception as ex:
            print(f"Error in get_all: {ex}")
            return None
        
    @classmethod
    def get_sesssion_by_id(cls, conexion, ID_Sesion):
        try:
            cursor = conexion.cursor()
            sql = """SELECT ID_Sesion, Indicaciones, Ejercicios, ID_Rutina
                    FROM Sesion WHERE ID_Sesion = %s"""
            cursor.execute(sql, (ID_Sesion))
            row = cursor.fetchone()

            if row:
                return Session(
                    Session_ID=row[0],
                    Indications=row[1],
                    Exercises=row[2],
                    Routine_ID=row[3],
                )
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener session por cédula: {ex}")
            return None
    
    @classmethod
    def getDataSession(cls, request):
        indications = request.form['Indications']
        exercises = request.form['Exercises']
        routine_ID = request.form['Routine_ID']
        
        return Session(None, indications, exercises, routine_ID)

    @classmethod
    def validateDataForm(cls, session):
        # Validar que datos
       True