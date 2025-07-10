from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.NotificationRepository import NotificationRepository
from datetime import datetime, date


class clientController:

    ClientRepository = ClientRepository()

    NotificationRepository = NotificationRepository()

    @classmethod
    def finOneByDocumentId(cls, documentId):
        if not documentId:
            raise Exception('El número de cédula es requerido')

        client = cls.ClientRepository.findOne({'DocumentId': documentId})

        if not client:
            raise Exception('No se ha encontrado el cliente')

        return client

    @classmethod
    def getNotifications(cls):
        notifications = cls.NotificationRepository.findAll()
       
        return notifications

    @classmethod
    def get_all(cls):
        clients = cls.ClientRepository.findAll()
       
        return clients
        
    @classmethod
    def get_allAble(cls):
        filters = {'State': True}
        clients = cls.ClientRepository.findAll(filters=filters)
       
        return clients



    @classmethod
    def getClientById(cls,id):

        try:
            relations = ['membresia']

            # Obtener la estadística con sus relaciones
            statistic = cls.ClientRepository.get_one(id, relations=relations)

            if not statistic:
                raise Exception(f"Error al obtener el cliente {id}.")

            return statistic
        except Exception as ex:
            raise Exception(f'Error en StatisticsController.get_statistic_by_id: {ex}')
        
    @classmethod
    def getDataClient(cls, request):
            return cls.ClientRepository.getDataClient(request) 

    @classmethod
    def clientValidated(cls, request):
           # Validar que el cliente no exista ya
            existing_client = cls.ClientRepository.findOne({'DocumentId': request.DocumentId})
            if existing_client:
                return f"Ya existe un cliente registrado con la cédula '{request.DocumentId}'."
            else:
                return  cls.ClientRepository.validateDataForm(request)
            

    @classmethod
    def clientValidatedUpdate(cls, DocumentId, request):
        if DocumentId == request.DocumentId:
            return  cls.ClientRepository.validateDataForm(request)
        else:
            existing_client = cls.ClientRepository.findOne({'DocumentId': request.DocumentId})
            if existing_client:
                return f"Ya existe un cliente registrado con la cédula '{request.DocumentId}'."
            return  cls.ClientRepository.validateDataForm(request)
           


    @classmethod
    def create(cls, data):
        dataClient = cls.ClientRepository.to_dict(data)
        cliente = cls.ClientRepository.create(**dataClient)
        return cliente
    
    @classmethod
    def updateClient(cls,id, data):
        dataClient = cls.ClientRepository.to_dict(data)
        cliente = cls.ClientRepository.update(id,**dataClient)
        return cliente

    @classmethod
    def get_one(cls,id):
        return cls.ClientRepository.get_one(id)

    @classmethod
    def disable_client(cls, id):
        return cls.ClientRepository.disable_client(id)
    
    @classmethod
    def able_Client(cls, id):
        return cls.ClientRepository.able_Client(id)
    
    @classmethod
    def able_Entry(cls, id):
        return cls.ClientRepository.able_Entry(id)
    
    


    
        
   