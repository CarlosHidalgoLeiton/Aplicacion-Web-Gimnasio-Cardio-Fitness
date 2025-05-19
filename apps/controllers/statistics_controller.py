from apps.db.repositories.StatisticsRepository import StatisticsRepository
from apps.db.repositories.TrainerRepository import TrainerRepository

from apps.db.models.Statistics import Statistics

class statisticsController:

    StatisticsRepository = StatisticsRepository()
    trainerRepository = TrainerRepository()

    # @classmethod
    # def insertStatistics(cls, request):
    #     try:
    #         data = {
    #             "FechaMedicion": request.form["Measurement_Date"],
    #             "Estatura": request.form["Stature"],
    #             "Peso": request.form["Weight"],
    #             "IMC": request.form["IMC"],
    #             "FC_REPOSO": request.form["FC_Repose"],
    #             "FC_MAX": request.form["FC_MAX"],
    #             "Presion_Arterial": request.form["Blood_pressure"],
    #             "BMR": request.form["BMR"],
    #             "Grasa_Corporal": request.form["Body_Fat"],
    #             "Porcentaje_Agua": request.form["Percent_Water"],
    #             "Masa_Muscular": request.form["Muscle_Mass"],
    #             "Edad_Metabolica": request.form["Metabolic_Age"],
    #             "Masa_Osea": request.form["Bone_Mass"],
    #             "Grasa_Visceral": request.form["Visceral_Fat"],
    #             "Circun_Pecho": request.form["Chest_Circum"],
    #             "Circun_Brazo_Der": request.form["Right_Arm_Circum"],
    #             "Circun_Brazo_Izq": request.form["Left_Arm_Circum"],
    #             "Circun_Cintura": request.form["Circum_Waist"],
    #             "Circun_Abdomen": request.form["Circum_Abdomen"],
    #             "Circun_Cadera": request.form["Hip_Circum"],
    #             "Circun_Muslo_Der": request.form["Circum_Thigh_Right"],
    #             "Circun_Muslo_Izq": request.form["Circum_Thigh_Left"],
    #             "Circun_Pantorilla_Der": request.form["Circum_Calf_Right"],
    #             "Circun_Pantorilla_Izq": request.form["Circum_Calf_Left"],
    #             "Consideraciones_Especiales": request.form["Special_Considerations"],
    #             "Deportista": request.form["sportsman"],
    #             "Objetivo_Entrenamiento": request.form["Training_Goal"],
    #             "Enfasis_Entrenamiento": request.form["Emphasis_Training"],
    #             "Disponibilidad": request.form["Disponibilidad"],
    #             "Estado": request.form["State"],
    #             "ID_Cliente": request.form["Client_ID"],
    #             "ID_Entrenador": request.form["Trainer_ID"],
    #         }

    #         statistics = statisticsRepository.create(**data)

    #         return statistics

    #     except IntegrityError as ex:
    #         raise Exception(f'Error de integridad: {ex}')
    #     except Exception as ex:
    #         raise Exception(f'Error al insertar estadísticas: {ex}')

    # @classmethod
    # def getTrainerById(cls, trainer_id):
    #     try:
    #         trainer = trainerRepository.findOne(filters={"Trainer_ID": trainer_id})

    #         if trainer:
    #             return trainer.Trainer_Name
    #         else:
    #             return None  # No se encontró el entrenador
    #     except Exception as ex:
    #         raise Exception(f'Error al obtener el entrenador por ID: {ex}')
        
    @classmethod
    def getStatisticsByClientId(cls, client_id):
        try:
            filters = {'Client_ID': client_id}
            relations = ['entrenador', 'cliente'] 

            statistics = cls.StatisticsRepository.findAll(filters=filters, relations=relations)

            # Verificar si las relaciones 'entrenador' o 'cliente' son nulas o vacías
            for stat in statistics:
                if not stat.get('entrenador') or not stat.get('cliente'):
                    raise Exception(f"Error: La relación de 'entrenador' o 'cliente' es nula o vacía para la estadística con ID {stat['ID_Estadistica']}.")


            return statistics
        except Exception as ex:
            raise Exception(f'Error en StatisticsController.get_statistics_by_client_id: {ex}')



    @classmethod
    def getStatisticById(cls, statistic_id):
        try:
            relations = ['entrenador', 'cliente']

            # Obtener la estadística con sus relaciones
            statistic = cls.StatisticsRepository.get_one(statistic_id, relations=relations)

            if not statistic:
                raise Exception(f"Error al obtener las estadísticas del cliente {statistic_id}.")

            # Validar que las relaciones no sean nulas
            if not getattr(statistic, 'entrenador', None) or not getattr(statistic, 'cliente', None):
                raise Exception(f"La relación 'entrenador' o 'cliente' es nula para la estadística con ID {statistic_id}.")

            return statistic
        except Exception as ex:
            raise Exception(f'Error en StatisticsController.get_statistic_by_id: {ex}')



    @classmethod
    def update_statistics(cls, document_id, statistics_data):
        try:
            # Llamamos al método update del RepositoryBase
            updated_statistics = cls.statistics_repository.update(document_id, **statistics_data)

            return updated_statistics  # Devuelve el objeto actualizado

        except Exception as ex:
            raise Exception(f'Error en StatisticsController.update_statistics: {ex}')