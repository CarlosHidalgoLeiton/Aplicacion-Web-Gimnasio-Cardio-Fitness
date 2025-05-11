from apps.db.repositories.TrainerRepository import TrainerRepository

class trainerController:

    TrainerRepository = TrainerRepository()

    @classmethod
    def get_all(cls):
        trainers = cls.TrainerRepository.findAll()
        if not trainers:
            raise Exception('No se encontraron notificaciones')
        return trainers
    
    @classmethod
    def getTrainer(cls, documentId):
        trainer = cls.TrainerRepository.findOne(filters={'DocumentId': documentId})
        
        if not trainer:
            raise Exception('No se pudo obtenr la información del perfil')
        return trainer
        