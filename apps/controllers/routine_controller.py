from apps.db.repositories.TrainerRepository import TrainerRepository
from apps.db.repositories.RoutineRepository import RoutineRepository
from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.SessionRepository import SessionRepository
from datetime import datetime
import json

class routineController:

    RoutineRepository = RoutineRepository()
    SessionRepository = SessionRepository()
    TrainerRepository = TrainerRepository()
    ClientRepository = ClientRepository()

    @classmethod
    def findOneRoutine(cls, idRoutine):

        if not idRoutine:
            raise Exception('El id de la rutina es necesario')
        
        routine = cls.RoutineRepository.get_one(idRoutine)

        if not routine:
            raise Exception('No se encontró la rutina')
        

        return routine

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

    @classmethod
    def updateRoutine(cls, request, routineId):

        trainer_id = request.form.get('TrainerId')

        if not trainer_id:
            raise Exception('El id del entrenador es requerido')

        indications = request.form.get('Indications')

        routine_updated = cls.RoutineRepository.update(routineId, TrainerId = trainer_id, Indications = indications)

        sessions_data = request.form.get('sessions')
        delete_ids_str = request.form.getlist('delete')

        delete_ids = []
        if delete_ids_str:
            delete_ids = json.loads(delete_ids_str[0]) if delete_ids_str else []
        
        if delete_ids:
            cls.SessionRepository.deleteSession(routineId, delete_ids)
        
        if sessions_data:
            sessions_data = json.loads(sessions_data)

            for session in sessions_data:
                session['Exercises'] = json.dumps(session['Exercises'])

                if session.get('insert', False):
                    session['Routine_ID'] = routineId
                    cls.SessionRepository.create(Name = session['Name'], Indications = session['Indications'], Exercises = session['Exercises'], Routine_ID=session['Routine_ID'])
                else:
                    cls.SessionRepository.update(session['Session_ID'], Name = session['Name'], Indications = session['Indications'], Exercises = session['Exercises'])

        return routine_updated
    
    @classmethod
    def disableRoutine(cls, request):
        data = request.get_json()
        routineId = data.get('routineID')

        if not routineId:
            raise Exception('El id de la rutina es requerido')

        routine = cls.RoutineRepository.get_one(routineId)

        if not routine:
            raise Exception('No se ha encontrado la rutina')
        
        routineUpdated = cls.RoutineRepository.update(routineId, State = False)

        return routineUpdated
    
    @classmethod
    def ableRoutine(cls, request):
        data = request.get_json()
        routineId = data.get('routineID')

        if not routineId:
            raise Exception('El id de la rutina es requerido')

        routine = cls.RoutineRepository.get_one(routineId)

        if not routine:
            raise Exception('No se ha encontrado la rutina')
        
        routineUpdated = cls.RoutineRepository.update(routineId, State = True)

        return routineUpdated

        


