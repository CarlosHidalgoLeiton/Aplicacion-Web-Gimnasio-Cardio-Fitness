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
    
    @classmethod
    def getData(cls, request):
        return cls.TrainerRepository.getDataTrainer(request)
    
    @classmethod
    def validateDataForm(cls, request):
        existing_trainer = cls.TrainerRepository.findOne({'DocumentId': request.DocumentId})
        if existing_trainer:
            return f"Ya existe un entrenador registrado con la cédula '{request.DocumentId}'."
        else:
            return  cls.TrainerRepository.validateDataForm(request)
        
    @classmethod
    def create(cls, data):
        dataTrainer = cls.TrainerRepository.to_dict(data)
        trainer = cls.TrainerRepository.create(**dataTrainer)
        return trainer
    
    @classmethod
    def updateTrainer(cls,id, data):
        dataTriner = cls.TrainerRepository.to_dict(data)
        trainer = cls.TrainerRepository.update(id,**dataTriner)
        return trainer
    
    @classmethod
    def get_one(cls,id):
         return cls.TrainerRepository.get_one(id)
    
    @classmethod
    def TrainertValidatedUpdate(cls, DocumentId, request):
        if DocumentId == request.DocumentId:
             return  cls.TrainerRepository.validateDataForm(request)
        else:
            existing_client = cls.TrainerRepository.findOne_any({'DocumentId': request.DocumentId})
            if existing_client:
                return f"Ya existe un entrenador registrado con la cédula '{request.DocumentId}'."
            return  cls.TrainerRepository.validateDataForm(request)
        
    @classmethod
    def disable_trainer(cls, id):
         return cls.TrainerRepository.disable_trainer(id)
    @classmethod
    def able_trainer(cls, id):
         return cls.TrainerRepository.able_trainer(id)

            

   
           