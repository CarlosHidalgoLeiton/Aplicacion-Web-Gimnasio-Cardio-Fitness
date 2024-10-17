from .entities.Session import Session
from datetime import datetime
import re
from pymysql import IntegrityError

class ModelProduct:

    @classmethod
    def insertProduct(cls, conection, session):
        if session != None:
            try:
                cursor = conection.cursor()
                sql = """INSERT INTO Sesion (Indicaciones, Ejercicios, ID_Rutina)
                    VALUES (%s, %s, %s)"""
                cursor.execute(sql, (session.Indicaciones, session.Ejercicios, session.ID_Rutina))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Sesion {session.Name} creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la sesion.")
                    return "Error"
                
            except IntegrityError as ex:
                print(f"Error en ModelProduct updateClient: {ex}")
                conection.rollback()
                return "Unique"
            except BaseException as ex:
                print(f"Error en ModelProduct insertProduct: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelProduct insertProduct: {ex}")
                conection.rollback()
                return "Error"
        else:
            return "Error"
    
    @classmethod
    def updateProduct(cls, conection, session, ID_Sesion):
        if session != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Sesion SET Indicaciones = %s, Ejercicios = %s, ID_Rutina = %s WHERE ID_Sesion = %s"""
                cursor.execute(sql, (session.Indicaciones, session.Ejercicios, session.ID_Rutina, ID_Sesion))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Sesion {session.Name} actualizada exitosamente.")
                    return True
                else:
                    print("No se pudo actualizar la sesion.")
                    return "Error"
                
            except IntegrityError as ex:
                print(f"Error en ModelProduct updateClient: {ex}")
                conection.rollback()
                return "Unique"
            except BaseException as ex:
                print(f"Error en ModelProduct updateProduct: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelProduct updateProduct: {ex}")
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
                    ID_Sesion=row[0],
                    Indicaciones=row[1],
                    Ejercicios=row[2],
                    ID_Rutina=row[3],
                )
                sessions.append(session)
            return sessions
        
        except Exception as ex:
            print(f"Error in get_all: {ex}")
            return None
        
    @classmethod
    def get_product_by_id(cls, conexion, ID_Sesion):
        try:
            cursor = conexion.cursor()
            sql = """SELECT ID_Sesion, Indicaciones, Ejercicios, ID_Rutina
                    FROM Sesion WHERE ID_Sesion = %s"""
            cursor.execute(sql, (ID_Sesion))
            row = cursor.fetchone()

            if row:
                return Session(
                    ID_Sesion=row[0],
                    Indicaciones=row[1],
                    Ejercicios=row[2],
                    ID_Rutina=row[3],
                )
            else:
                return None
        except Exception as ex:
            print(f"Error al obtener session por cédula: {ex}")
            return None
    
    @classmethod
    def getDataProduct(cls, request):
        name = request.form['Name']
        detail = request.form['Detail']
        price = request.form['Price']
        stock = request.form['Stock']
        image_file = request.files['Image']
        image_blob = None
        
        if image_file:
            image_blob = image_file.read()

        return Session(None, name, detail, price, stock, image_blob)

    @classmethod
    def validateDataForm(cls, session):
        # Validar que la imagen no sea None o esté vacía
        if not session.Image:
            print("La imagen del sesion es requerida.")
            return False
        
        if session.Price is not None:
            if any(p.isalpha() for p in str(session.Price)):
                return "El precio no debe contener letras."
            elif any(p in "-$" for p in str(session.Price)):  # Verifica si contiene caracteres no permitidos
                return "El precio no debe contener caracteres especiales como '-'."
        else:
            return "Debe ingresar el precio en número."
       
        return True
            
        
        
