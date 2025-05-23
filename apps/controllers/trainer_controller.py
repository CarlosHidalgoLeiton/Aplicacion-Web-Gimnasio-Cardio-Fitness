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


