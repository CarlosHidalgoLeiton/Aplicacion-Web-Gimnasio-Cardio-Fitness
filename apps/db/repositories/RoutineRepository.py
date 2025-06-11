from apps.db.models.Routine import Routine
from pymysql import IntegrityError
from apps.db.models.Routine import Routine

from apps.db.repositories.RepositoryBase import RepositoryBase

class RoutineRepository(RepositoryBase):
    
    def __init__(self):
        super().__init__(Routine)

    @classmethod
    def updateRoutine(cls, conection, indications, routineId):
        if indications is not None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE rutina SET Indicaciones = %s WHERE ID_Rutina = %s"""
                cursor.execute(sql, (indications, routineId))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Rutina {routineId} actualizada exitosamente.")
                    return True
                else:
                    print("No se pudo actualizar la rutina.")
                    return "Error"

            except IntegrityError as ex:
                print(f"Error en RoutineRepository updateRoutine: {ex}")
                conection.rollback()
                return "Primary"
            except BaseException as ex:
                print(f"Error en RoutineRepository updateRoutine: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en RoutineRepository updateRoutine: {ex}")
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
    def get_routine(cls, conexion, RoutineId):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Rutina, ID_Cliente, ID_Entrenador, Indicaciones, Fecha, Estado FROM Rutina WHERE ID_Rutina = %s"
            cursor.execute(sql, (RoutineId))
            row = cursor.fetchone()
            
            if row:
                return Routine(
                    RoutineId=row[0],
                    ClientId=row[1],
                    TrainerId=row[2],
                    Indications=row[3],
                    Date=row[4],
                    State=row[5],
                )
            else:    
                return None
        except Exception as ex:
            print(f"Error en get_routine: {ex}")
            return None

    @classmethod
    def deleteRoutine(cls, conection, routine_id):
        try:
            cursor = conection.cursor()
            sql = "DELETE FROM Rutina WHERE ID_Rutina = %s"
            cursor.execute(sql, (routine_id,))
            conection.commit()
            print(f"Rutina {routine_id} eliminada exitosamente.")
        except Exception as e:
            print(f"Error al eliminar la rutina {routine_id}: {e}")
            conection.rollback()
    @classmethod
    def disableRoutine(cls, conection, RoutineId):
        if RoutineId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Rutina SET Estado = 0  WHERE ID_Rutina = %s"""
                cursor.execute(sql, (RoutineId))
                if cursor.rowcount > 0:
                    conection.commit()
                    
                    return True
                else:
                    print("No se pudo actualizar la rutina.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar la rutina {ex}")
                conection.rollback()
                return False
        else:
            return False
        
    @classmethod
    def ableRoutine(cls, conection, RoutineId):
        if RoutineId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Rutina SET Estado = 1  WHERE ID_Rutina = %s"""
                cursor.execute(sql, (RoutineId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar la rutina.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar la rutina {ex}")
                conection.rollback()
                return False
        else:
            return False
