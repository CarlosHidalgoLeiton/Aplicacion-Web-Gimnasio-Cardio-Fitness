from .entities.Session import Session
from datetime import datetime
from pymysql import IntegrityError
import json
class ModelSession:

   

    @classmethod
    def insertSession(cls, conection, session):
        if session is not None:
            try:
                cursor = conection.cursor()
                sql = """INSERT INTO Sesion (Indicaciones, Ejercicios, ID_Rutina, Nombre)
                        VALUES (%s, %s, %s, %s)"""

                # Convertir la lista de ejercicios a JSON, asegurándonos que sea válido
                ejercicios_json = json.dumps(session['Exercises'])

                # Imprimir los datos para depuración
                print(f"Datos de la sesión: Indicaciones={session['Indications']}, Ejercicios={ejercicios_json}, ID_Rutina={session['Routine_ID']}, Nombre={session['Name']}")

                # Ejecutar la inserción con los datos convertidos
                cursor.execute(sql, (session['Indications'], ejercicios_json, session['Routine_ID'], session['Name']))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Sesión {session['Name']} creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la sesión.")
                    return "Error"

            except IntegrityError as ex:
                print(f"Error de integridad al insertar la sesión: {ex}")
                conection.rollback()
                return "Unique"
            except BaseException as ex:
                print(f"Error en la base de datos al insertar la sesión: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error general al insertar la sesión: {ex}")
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
            sql = "SELECT ID_Sesion, Indicaciones, Ejercicios, ID_Rutina, Nombre FROM Sesion"
            cursor.execute(sql)
            rows = cursor.fetchall()
            sessions = []
            for row in rows:
                session = Session(
                    Session_ID=row[0],
                    Indications=row[1],
                    Exercises=row[2],
                    Routine_ID=row[3],
                    Name=row[4],
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
            sql = "SELECT ID_Sesion, Indicaciones, Ejercicios, ID_Rutina, Nombre FROM Sesion WHERE ID_Rutina = %s "
            cursor.execute(sql, (routineId))
            rows = cursor.fetchall()
            sessions = []
            for row in rows:
                session = Session(
                    Session_ID=row[0],
                    Indications=row[1],
                    Exercises=row[2],
                    Routine_ID=row[3],
                    Name=row[4],
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
            sql = """SELECT ID_Sesion, Indicaciones, Ejercicios, ID_Rutina, Nombre
                    FROM Sesion WHERE ID_Sesion = %s"""
            cursor.execute(sql, (ID_Sesion,))
            row = cursor.fetchone()

            if row:
                return Session(
                    Session_ID=row[0],
                    Indications=row[1],
                    Exercises=row[2],  # Esto es un string JSON
                    Routine_ID=row[3],
                    Name=row[4],
                )
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener session por ID: {ex}")
            return None

    @classmethod
    def deleteSessionsByRoutineID(cls, conexion, routineId):
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM Sesion WHERE ID_Rutina = %s"
            cursor.execute(sql, (routineId,))
            conexion.commit() 
            return True
        
        except Exception as ex:
            print(f"Error in deleteSessionsByRoutineID: {ex}")
            conexion.rollback() 
            return False
        
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