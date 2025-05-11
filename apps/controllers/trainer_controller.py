from apps.db.repositories.TrainerRepository import TrainerRepository

class trainerController:

    TrainerRepository = TrainerRepository()



    @classmethod
    def get_all(cls):
        trainers = cls.TrainerRepository.findAll()
        if not trainers:
            raise Exception('No se encontraron notificaciones')
        return trainers
        