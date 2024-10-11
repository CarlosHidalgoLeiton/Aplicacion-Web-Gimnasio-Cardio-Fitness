from .entities.Membership import Membership
from pymysql import IntegrityError

class ModelMembership:

    @classmethod
    def insertMembership(cls, conection, membership):
        if membership != None:
            try:
                membership.State = 1
                cursor = conection.cursor()
                sql = """INSERT INTO Membresia (Nombre, Descripcion, Precio, Estado)
                VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (membership.Name, membership.Description, membership.Price, membership.State))
                conection.commit()

                if cursor.rowcount > 0:
                    print(f"Membresia {membership.id} creada exitosamente.")
                    return True
                else:
                    print("No se pudo crear la Membresia.")
                    return "Error"
                
            except BaseException as ex:
                print(f"Error en ModelMembership insertMembership: {ex}")
                conection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelMembership insertMembership: {ex}")
                conection.rollback()
                return "Error"
            finally:
                cursor.close()
        else:
            return "Error"
    
    @classmethod
    def get_all(cls, conexion):
        try:
            cursor = conexion.cursor()
            sql = "SELECT ID_Membresia, Nombre, Descripcion, Precio, Estado FROM Membresia"
            cursor.execute(sql)
            rows = cursor.fetchall()
            memberships = []
            for row in rows:
                member = {
                    'id': row[0],
                    'Name': row[1],
                    'Description': row[2],
                    'Precio':row[3],
                    'State': row[4],
                }
                memberships.append(member)
            return memberships
        except Exception as ex:
            print(f"Error en get_all: {ex}")
            return None

    @classmethod
    def getDataClient(cls, request):
        name = request.form['Nombre']
        description = request.form['Descripcion']
        price = request.form['Precio']

        return Membership(None, name, description, price, None)
    
    @classmethod
    def validateDataForm(cls, membership):

        if membership.Name != None:
            if not all(m.isalpha() for m in membership.Name if m != ' '):
                return "El nombre ingresado no es válido."
        else:
            return "Debe ingresar el nombre de la membresia."
        
        if membership.Description != None:
            if not all(m.isalpha() for m in membership.Description if m != ' '):
                return "La descripción ingresada no es válida."
        else:
            return "Debe ingresar la descripción de la membresia."
        
        if membership.Price != None:
            if "-" in membership.Price or any(m.isalpha() for m in membership.Price):
                return "El precio ingresado no es válido."
        else:
            return "Debe ingresar el precio de la membresia."

        return True
    
    @classmethod
    def disableMembership(cls, conection, membershipId):
        if membershipId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Membresia SET Estado = 0  WHERE ID_Membresia = %s"""
                cursor.execute(sql, (membershipId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar el cliente.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar un cliente {ex}")
                conection.rollback()
                return False
            finally:
                cursor.close()
        else:
            return False
        
    @classmethod
    def ableMembership(cls, conection, membershipId):
        if membershipId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Membresia SET Estado = 1  WHERE ID_Membresia = %s"""
                cursor.execute(sql, (membershipId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar la membresía.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar la membresía. {ex}")
                conection.rollback()
                return False
            finally:
                cursor.close()
        else:
            return False

