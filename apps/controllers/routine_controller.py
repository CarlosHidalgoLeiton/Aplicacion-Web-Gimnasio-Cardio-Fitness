from apps.db.repositories.RoutineRepository import RoutineRepository
from apps.db.repositories.SessionRepository import SessionRepository

class routineController:

    RoutineRepository = RoutineRepository()
    SessionRepository = SessionRepository()

    @classmethod
    def findOneRoutine(cls, idRoutine):

        if not idRoutine:
            raise Exception('El id de la rutina es necesario')
        
        routine = cls.RoutineRepository.get_one(idRoutine)

        if not routine:
            raise Exception('No se encontró la rutina')
        

        return routine
        


