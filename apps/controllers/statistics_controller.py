from apps.db.repositories.StatisticsRepository import StatisticsRepository
from apps.db.repositories.TrainerRepository import TrainerRepository

from apps.db.models.Statistics import Statistics

class statisticsController:

    StatisticsRepository = StatisticsRepository()
    trainerRepository = TrainerRepository()

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
            if not statistic_id:
                raise Exception('El id de la estadística es requerido')

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
            dataStatistic = cls.StatisticsRepository.to_dict(statistics_data)
            del dataStatistic['ID_Statistics']
            updated_statistics = cls.StatisticsRepository.update(document_id, **dataStatistic)

            return updated_statistics

        except Exception as ex:
            raise Exception(f'Error en StatisticsController.update_statistics: {ex}')

    @classmethod
    def create(cls, statistics_data):
        dataStatistic = cls.StatisticsRepository.to_dict(statistics_data)
        statistics = cls.StatisticsRepository.create(**dataStatistic)
        return statistics

    @classmethod
    def disableStatistic(cls, request):
        data = request.get_json()
        statisticId = data.get('statisticsID')

        if not statisticId:
            raise Exception('El id de la estadística es requerido')

        statistic = cls.StatisticsRepository.get_one(statisticId)

        if not statistic:
            raise Exception('No se ha encontrado la rutina')
        
        statisticUpdated = cls.StatisticsRepository.update(statisticId, State = False)

        return statisticUpdated

    @classmethod
    def ableStatistic(cls, request):
        data = request.get_json()
        statisticId = data.get('statisticsID')

        if not statisticId:
            raise Exception('El id de la estadística es requerido')

        statistic = cls.StatisticsRepository.get_one(statisticId)

        if not statistic:
            raise Exception('No se ha encontrado la rutina')
        
        statisticUpdated = cls.StatisticsRepository.update(statisticId, State = True)

        return statisticUpdated
