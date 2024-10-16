from .entities.Statistics import Statistics
from datetime import datetime
import re
from pymysql import IntegrityError
class ModelStatistics:

    @classmethod
    def insertStatistics(cls, connection, statistics):
        if statistics is not None:
            try:
                cursor = connection.cursor()
                sql = """INSERT INTO estadistica (FechaMedicion, Estatura, Peso, IMC, FC_REPOSO, FC_MAX, Presion_Arterial, BMR, Grasa_Corporal, Porcentaje_Agua, Masa_Muscular, Edad_Metabolica, Masa_Osea, Grasa_Visceral, Circun_Pecho, Circun_Brazo_Der, Circun_Brazo_Izq, Circun_Cintura, Circun_Abdomen, Circun_Cadera, Circun_Muslo_Der, Circun_Muslo_Izq, Circun_Pantorilla_Der, Circun_Pantorilla_Izq, Consideraciones_Especiales, Deportista, Objetivo_Entrenamiento, Enfasis_Entrenamiento, Disponibilidad, Estado, ID_Cliente , ID_Entrenador)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"""
                cursor.execute(sql, (
                    statistics.Measurement_Date, statistics.Stature, statistics.Weight, statistics.IMC, statistics.FC_Repose, statistics.FC_MAX, statistics.Blood_pressure, statistics.BMR, statistics.Body_Fat, statistics.Percent_Water, statistics.Muscle_Mass, statistics.Metabolic_Age, statistics.Bone_Mass, statistics.Visceral_Fat, statistics.Chest_Circum, statistics.Right_Arm_Circum, statistics.Left_Arm_Circum, statistics.Circum_Waist, statistics.Circum_Abdomen, statistics.Hip_Circum, statistics.Circum_Thigh_Right, statistics.Circum_Thigh_Left, statistics.Circum_Calf_Right, statistics.Circum_Calf_Left, statistics.Special_Considerations, statistics.sportsman, statistics.Training_Goal, statistics.Emphasis_Training, statistics.Disponibilidad, statistics.State, statistics.Client_ID, statistics.Trainer_ID
                ))
                connection.commit()

                if cursor.rowcount > 0:
                    print(f"Estadísticas para el cliente {statistics.Client_ID} creadas exitosamente.")
                    return True
                else:
                    print("No se pudieron crear las estadísticas.")
                    return "Error"
                    
            except IntegrityError as ex:
                print(f"Error en ModelStatistics insertStatistics: {ex}")
                connection.rollback()
                return "Primary"
            except BaseException as ex:
                print(f"Error en ModelStatistics insertStatistics: {ex}")
                connection.rollback()
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelStatistics insertStatistics: {ex}")
                connection.rollback()
                return "Error"
        else:
            return "Error"
        

    @staticmethod
    def getTrainerById(conection, trainer_id):
        cursor = conection.cursor()
        query = "SELECT Trainer_Name FROM Trainers WHERE Trainer_ID = %s"
        cursor.execute(query, (trainer_id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    @classmethod
    def getStatisticsByClientId(cls, connection, client_id):
        if client_id is not None:
            try:
                cursor = connection.cursor()
                sql ="""
                SELECT 
                    e.ID_Estadistica, 
                    e.FechaMedicion, 
                    t.Nombre,
                    t.Primer_Apellido
                FROM 
                    estadistica e
                JOIN 
                    entrenador t 
                ON 
                    e.ID_Entrenador = t.Cedula
                WHERE 
                    e.ID_Cliente = %s;
                """
                cursor.execute(sql, (client_id,))
                statistics = cursor.fetchall()
                cursor.close()
                

                if statistics:
                    # Retornar los registros encontrados
                    return statistics
                else:
                    print(f"No se encontraron estadísticas para el cliente con ID {client_id}.")
                    return None
            
            except BaseException as ex:
                print(f"Error en ModelStatistics getStatisticsByClientId: {ex}")
                return "DataBase"
            except Exception as ex:
                print(f"Error en ModelStatistics getStatisticsByClientId: {ex}")
                return "Error"
        else:
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
                    cliente c
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
    def getDataStatistics(cls, request):
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
        State = request.form['State']
        Client_ID = request.form['Client_ID']
        Trainer_ID = request.form['Trainer_ID']

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
            Disponibilidad=Disponibilidad,
            State=State,
            Client_ID=Client_ID,
            Trainer_ID=Trainer_ID
        )

  
    @classmethod
    def validateDataForm(cls, statistics):

        #Validation for Measurement_Date
        if statistics.Measurement_Date is not None:
            # Convertir a datetime si es un string
            if isinstance(statistics.Measurement_Date, str):
                measurement_date = datetime.strptime(statistics.Measurement_Date, '%Y-%m-%d').date()
            else:
                measurement_date = statistics.Measurement_Date

            # Imprimir para depuración
            print("Fecha ingresada:", measurement_date)
            print("Fecha actual:", datetime.now().date())

            # Comprobar si la fecha obtenida es diferente de la fecha actual
            if measurement_date != datetime.now().date():
                return "La fecha de medición debe ser la fecha actual."
        else:
            return "No se logro obtener la fecha de medición "
                        
            #Validation for documentID 
        if statistics.Client_ID != None:
            if "-" not in statistics.Client_ID and not any( d.isalpha() for d in statistics.Client_ID): #Valida que no sea alfabetico y que no tenga un "-"
                if len(statistics.Client_ID) < 9:
                    return "No se logro enlazar con el cliente, por favor inténtalo más tarde.."
            else:
                return "No se logro enlazar con el cliente por motivos que se detectaron caracteres especiales."
        else:
            return "No se logro enlazar con el cliente, por favor inténtalo más tarde."
        
        if statistics.Trainer_ID != None:
            if "-" not in statistics.Trainer_ID and not any( d.isalpha() for d in statistics.Trainer_ID): #Valida que no sea alfabetico y que no tenga un "-"
                if len(statistics.Trainer_ID) < 9:
                    return "No se logro enlazar con el entrenador, por favor inténtalo más tarde."
            else:   
                return "No se logro enlazar con el cliente por motivos que se detectaron caracteres especiales."
        else:
            return "No se logro enlazar con el cliente, por favor inténtalo más tarde."
        
       
        return True
        