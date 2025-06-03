from apps.db.models.Statistics import Statistics
from datetime import datetime
import re
from pymysql import IntegrityError
from apps.db.repositories.RepositoryBase import RepositoryBase


class StatisticsRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Statistics)


    @classmethod
    def updateStatistics(cls, connection, statistics,documentId):
        try:
            cursor = connection.cursor()
            sql = """UPDATE Estadistica
                     SET FechaMedicion = %s, Estatura = %s, Peso = %s, IMC = %s, FC_REPOSO = %s, FC_MAX = %s,
                         Presion_Arterial = %s, BMR = %s, Grasa_Corporal = %s, Porcentaje_Agua = %s, 
                         Masa_Muscular = %s, Edad_Metabolica = %s, Masa_Osea = %s, Grasa_Visceral = %s,
                         Circun_Pecho = %s, Circun_Brazo_Der = %s, Circun_Brazo_Izq = %s, Circun_Cintura = %s, 
                         Circun_Abdomen = %s, Circun_Cadera = %s, Circun_Muslo_Der = %s, Circun_Muslo_Izq = %s, 
                         Circun_Pantorilla_Der = %s, Circun_Pantorilla_Izq = %s, Consideraciones_Especiales = %s, 
                         Deportista = %s, Objetivo_Entrenamiento = %s, Enfasis_Entrenamiento = %s, 
                         Disponibilidad = %s WHERE ID_Estadistica = %s"""
            
            cursor.execute(sql, (
                statistics.Measurement_Date, statistics.Stature, statistics.Weight, statistics.IMC, 
                statistics.FC_Repose, statistics.FC_MAX, statistics.Blood_pressure, statistics.BMR, 
                statistics.Body_Fat, statistics.Percent_Water, statistics.Muscle_Mass, statistics.Metabolic_Age, 
                statistics.Bone_Mass, statistics.Visceral_Fat, statistics.Chest_Circum, statistics.Right_Arm_Circum, 
                statistics.Left_Arm_Circum, statistics.Circum_Waist, statistics.Circum_Abdomen, statistics.Hip_Circum, 
                statistics.Circum_Thigh_Right, statistics.Circum_Thigh_Left, statistics.Circum_Calf_Right, 
                statistics.Circum_Calf_Left, statistics.Special_Considerations, statistics.sportsman, 
                statistics.Training_Goal, statistics.Emphasis_Training, statistics.Disponibilidad, documentId
            ))
            
            connection.commit()
            
            if cursor.rowcount > 0:
                print(f"Estadística actualizada exitosamente.")
                return True
            else:
                print("No se encontraron registros para actualizar.")
                return "NoUpdate"
                
        except IntegrityError as ex:
            print(f"Error en ModelStatistics updateStatistics: {ex}")
            connection.rollback()
            return "Primary"
        except BaseException as ex:
            print(f"Error en ModelStatistics updateStatistics: {ex}")
            connection.rollback()
            return "DataBase"
        except Exception as ex:
            print(f"Error en ModelStatistics updateStatistics: {ex}")
            connection.rollback()
            return "Error"


    @classmethod
    def getClientById(cls, connection, client_id):
        if client_id is not None:
            try:
                cursor = connection.cursor()
                sql_cliente = """
                SELECT 
                    c.Nombre AS NombreCliente,
                    c.Primer_Apellido AS Primer_ApellidoCliente,
                    c.Segundo_Apellido,
                    c.Edad
                FROM 
                    Cliente c
                WHERE 
                    c.Cedula = %s;
                """
                cursor.execute(sql_cliente, (client_id,))
                client = cursor.fetchone()
                cursor.close()
                return client
                
            except BaseException as ex:
                print(f"Error en ModelStatistics getClientById: {ex}")
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelStatistics getClientById: {ex}")
                return "Error"
        else:
            return "Error"

    
    @classmethod
    def getDataStatisticsUpdate(cls, request):
        # Extraer datos del formulario
        Measurement_DateStr = request.form.get('Measurement_Date')
        Measurement_Date = datetime.strptime(Measurement_DateStr, "%Y-%m-%d").date() if Measurement_DateStr else None
        Stature = request.form['Stature']
        Weight = request.form['Weight']
        IMC = request.form['IMC']
        FC_Repose = request.form['FC_Repose']
        FC_MAX = request.form['FC_MAX']
        Blood_pressure = request.form['Blood_pressure']
        BMR = request.form['BMR']
        Body_Fat = request.form['Body_Fat']
        Percent_Water = request.form['Percent_Water']
        Muscle_Mass = request.form['Muscle_Mass']
        Metabolic_Age = request.form['Metabolic_Age']
        Bone_Mass = request.form['Bone_Mass']
        Visceral_Fat = request.form['Visceral_Fat']
        Chest_Circum = request.form['Chest_Circum']
        Right_Arm_Circum = request.form['Right_Arm_Circum']
        Left_Arm_Circum = request.form['Left_Arm_Circum']
        Circum_Waist = request.form['Circum_Waist']
        Circum_Abdomen = request.form['Circum_Abdomen']
        Hip_Circum = request.form['Hip_Circum']
        Circum_Thigh_Right = request.form['Circum_Thigh_Right']
        Circum_Thigh_Left = request.form['Circum_Thigh_Left']
        Circum_Calf_Right = request.form['Circum_Calf_Right']
        Circum_Calf_Left = request.form['Circum_Calf_Left']
        Special_Considerations = request.form['Special_Considerations']
        sportsman = request.form['sportsman']
        Training_Goal = request.form['Training_Goal']
        Emphasis_Training = request.form['Emphasis_Training']
        Disponibilidad = request.form['Disponibilidad']
    

        # Retornar una instancia de Statistics
        return Statistics(
            Measurement_Date=Measurement_Date,
            Stature=Stature,
            Weight=Weight,
            IMC=IMC,
            FC_Repose=FC_Repose,
            FC_MAX=FC_MAX,
            Blood_pressure=Blood_pressure,
            BMR=BMR,
            Body_Fat=Body_Fat,
            Percent_Water=Percent_Water,
            Muscle_Mass=Muscle_Mass,
            Metabolic_Age=Metabolic_Age,
            Bone_Mass=Bone_Mass,
            Visceral_Fat=Visceral_Fat,
            Chest_Circum=Chest_Circum,
            Right_Arm_Circum=Right_Arm_Circum,
            Left_Arm_Circum=Left_Arm_Circum,
            Circum_Waist=Circum_Waist,
            Circum_Abdomen=Circum_Abdomen,
            Hip_Circum=Hip_Circum,
            Circum_Thigh_Right=Circum_Thigh_Right,
            Circum_Thigh_Left=Circum_Thigh_Left,
            Circum_Calf_Right=Circum_Calf_Right,
            Circum_Calf_Left=Circum_Calf_Left,
            Special_Considerations=Special_Considerations,
            sportsman=sportsman,
            Training_Goal=Training_Goal,
            Emphasis_Training=Emphasis_Training,
            Disponibilidad=Disponibilidad
        )
        
    @classmethod
    def validateDataFormUpdate(cls, statistics):

        if statistics.Measurement_Date is None:
            return "La fecha de medición no debe estar vacía."    


        if statistics.sportsman not in ["si", "Si", "SI", "No", "no", "NO",None,""]:
            return "Error: El valor de ¿Es deportista? debe ser 'si' o 'No'."

        return True
        
      
    @classmethod
    def disableStatistics(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Estadistica SET Estado = 0  WHERE ID_Estadistica = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar la estadística.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar la estadística {ex}")
                conection.rollback()
                return False
        else:
            return False
        
    @classmethod
    def ableStatistics(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Estadistica SET Estado = 1  WHERE ID_Estadistica = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar la estadística.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar la estadística {ex}")
                conection.rollback()
                return False
        else:
            return False
