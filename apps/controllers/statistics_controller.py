from apps.db.repositories.StatisticsRepository import StatisticsRepository
from apps.db.models.Statistics import Statistics

class statisticsController:

    statisticsRepository = StatisticsRepository()
    trainerRepository = TrainerRepository()

    @classmethod
    def insertStatistics(cls, request):
        try:
            data = {
                "FechaMedicion": request.form["Measurement_Date"],
                "Estatura": request.form["Stature"],
                "Peso": request.form["Weight"],
                "IMC": request.form["IMC"],
                "FC_REPOSO": request.form["FC_Repose"],
                "FC_MAX": request.form["FC_MAX"],
                "Presion_Arterial": request.form["Blood_pressure"],
                "BMR": request.form["BMR"],
                "Grasa_Corporal": request.form["Body_Fat"],
                "Porcentaje_Agua": request.form["Percent_Water"],
                "Masa_Muscular": request.form["Muscle_Mass"],
                "Edad_Metabolica": request.form["Metabolic_Age"],
                "Masa_Osea": request.form["Bone_Mass"],
                "Grasa_Visceral": request.form["Visceral_Fat"],
                "Circun_Pecho": request.form["Chest_Circum"],
                "Circun_Brazo_Der": request.form["Right_Arm_Circum"],
                "Circun_Brazo_Izq": request.form["Left_Arm_Circum"],
                "Circun_Cintura": request.form["Circum_Waist"],
                "Circun_Abdomen": request.form["Circum_Abdomen"],
                "Circun_Cadera": request.form["Hip_Circum"],
                "Circun_Muslo_Der": request.form["Circum_Thigh_Right"],
                "Circun_Muslo_Izq": request.form["Circum_Thigh_Left"],
                "Circun_Pantorilla_Der": request.form["Circum_Calf_Right"],
                "Circun_Pantorilla_Izq": request.form["Circum_Calf_Left"],
                "Consideraciones_Especiales": request.form["Special_Considerations"],
                "Deportista": request.form["sportsman"],
                "Objetivo_Entrenamiento": request.form["Training_Goal"],
                "Enfasis_Entrenamiento": request.form["Emphasis_Training"],
                "Disponibilidad": request.form["Disponibilidad"],
                "Estado": request.form["State"],
                "ID_Cliente": request.form["Client_ID"],
                "ID_Entrenador": request.form["Trainer_ID"],
            }

            statistics = statisticsRepository.create(**data)

            return statistics

        except IntegrityError as ex:
            raise Exception(f'Error de integridad: {ex}')
        except Exception as ex:
            raise Exception(f'Error al insertar estadísticas: {ex}')

    @classmethod
    def getTrainerById(cls, trainer_id):
        try:
            trainer = trainerRepository.findOne(filters={"Trainer_ID": trainer_id})

            if trainer:
                return trainer.Trainer_Name
            else:
                return None  # No se encontró el entrenador
        except Exception as ex:
            raise Exception(f'Error al obtener el entrenador por ID: {ex}')
    @classmethod
    def get_statistics_by_client_id(cls, client_id):
        try:
            # Definir los filtros y relaciones que deseas utilizar
            filters = {'ID_Cliente': client_id}
            relations = ['cliente']  # Asegúrate de que 'cliente' esté en la relación

            # Usar el statistics_repository para llamar al método findAll (heredado de RepositoryBase)
            statistics = cls.statistics_repository.findAll(filters=filters, relations=relations)

            # Si no se encuentran estadísticas, lanzar una excepción
            if not statistics:
                raise Exception(f"No se encontraron estadísticas para el cliente con ID {client_id}.")

            return statistics
        except Exception as ex:
            raise Exception(f'Error en StatisticsController.get_statistics_by_client_id: {ex}')


    @classmethod
    def get_statistics_by_id(cls, request):
        try:
            # Obtener el documentId desde la solicitud (request)
            document_id = request.form.get('documentId')  # Suponiendo que usas un formulario

            if not document_id:
                raise Exception("El ID de la estadística es requerido.")

            # Utilizar el método findOne del RepositoryBase para obtener la estadística por ID
            filters = {'ID_Estadistica': document_id}
            statistics = cls.statistics_repository.findOne(filters=filters)

            if not statistics:
                raise Exception(f"No se encontraron estadísticas para el ID {document_id}.")

            # Retornar la estadística encontrada (esto puede ser una respuesta JSON, por ejemplo)
            return statistics

        except Exception as ex:
            raise Exception(f"Error en StatisticsController.get_statistics_by_id: {ex}")


    @classmethod
    def update_statistics(cls, document_id, statistics_data):
        try:
            # Llamamos al método update del RepositoryBase
            updated_statistics = cls.statistics_repository.update(document_id, **statistics_data)

            return updated_statistics  # Devuelve el objeto actualizado

        except Exception as ex:
            raise Exception(f'Error en StatisticsController.update_statistics: {ex}')