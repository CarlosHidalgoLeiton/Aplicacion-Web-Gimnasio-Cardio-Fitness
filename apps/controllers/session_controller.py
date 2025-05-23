from apps.db.repositories.SessionRepository import SessionRepository

class sessionController:

    SessionRepository = SessionRepository()

    @classmethod
    def findAllByIdRoutine(cls, idRoutine):

        if not idRoutine:
            raise Exception('El id de la rutina es requerido')

        relations = ['routine']

        sessions = cls.SessionRepository.findAll(filters = {'Routine_ID': idRoutine}, relations = relations)

        return sessions

    @classmethod
    def findOneById(cls, idSession):

        if not idSession:
            raise Exception('El id de la sesión es requerido')

        relations = ['routine']

        session = cls.SessionRepository.get_one(idSession, relations = relations)

        if not session:
            raise Exception('No se encontró la sesión')

        return session
