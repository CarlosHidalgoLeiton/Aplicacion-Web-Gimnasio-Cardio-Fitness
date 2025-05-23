from apps.db.repositories.TrainerRepository import TrainerRepository
from apps.db.repositories.RoutineRepository import RoutineRepository
from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.SessionRepository import SessionRepository
from datetime import datetime
import json
from apps.db.db import db
class trainerController:

    TrainerRepository = TrainerRepository()
    RoutineRepository = RoutineRepository()
    ClientRepository = ClientRepository()
    SessionRepository = SessionRepository()

    @classmethod
    def get_all(cls):
        trainers = cls.TrainerRepository.findAll()

        return trainers
    
    @classmethod
    def getTrainer(cls, documentId):
        trainer = cls.TrainerRepository.findOne(filters={'DocumentId': documentId})

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

            

   
           
    
    @classmethod
    def getRoutineClient(cls, clientId):

        if not clientId:
            raise Exception('El id del cliente es requerido')
        
        relations = ['entrenador', 'cliente']
        routines = cls.RoutineRepository.findAll(filters={'ClientId': clientId}, relations = relations)

        return routines

    @classmethod
    def createRoutine(cls, request):

        ClientId = request.form['ClientId']
        TrainerId = request.form['TrainerId']
        Indications = request.form['Indications']
        sessions = request.form.get('sessions')

        if not ClientId:
            raise Exception('El id del cliente es requerido')
        
        if not TrainerId:
            raise Exception('El id del entrenador es requerido')
        
        if not sessions or sessions == '[]':
            raise Exception('Debe ingresar al menos una sesión')
        
        routine = cls.RoutineRepository.create(ClientId = ClientId, TrainerId = TrainerId, Indications = Indications, Date = datetime.now(), State = 1)

        sessions_data = json.loads(sessions)
        
        for session in sessions_data:
            session['Routine_ID'] = routine.RoutineId
            session['Exercises'] = json.dumps(session['Exercises'])
            cls.SessionRepository.create(Name = session['Name'], Indications = session['Indications'], Exercises = session['Exercises'], Routine_ID=session['Routine_ID'])
        
        return routine


