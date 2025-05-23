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

        return cls.ClientRepository.findOne({'DocumentId': documentId})

    @classmethod
    def getNotifications(cls):
        notifications = cls.NotificationRepository.findAll()
        if not notifications:
            raise Exception('No se encontraron notificaciones')
        return notifications

    @classmethod
    def get_all(cls):
        clients = cls.ClientRepository.findAll()
        if not clients:
            raise Exception('No se encontraron clientes')
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
        existing_client = cls.ClientRepository.findOne_any({'DocumentId': request.DocumentId})
        if existing_client:
            return f"Ya existe un cliente registrado con la cédula '{request.DocumentId}'."
        else:
            return  cls.ClientRepository.validateDataForm(request)
            

    @classmethod
    def clientValidatedUpdate(cls, DocumentId, request):
        if DocumentId == request.DocumentId:
            return  cls.ClientRepository.validateDataForm(request)
        else:
            existing_client = cls.ClientRepository.findOne_any({'DocumentId': request.DocumentId})
            if existing_client:
                return f"Ya existe un cliente registrado con la cédula '{request.DocumentId}'."


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
        
    # @classmethod
    # def getDataClient(cls, request):
    #     try:
    #         required_fields = [
    #             'documentId', 'name', 'firstLastName', 'secondLastName',
    #             'Date_Birth', 'mail', 'phone', 'ocupation',
    #             'emergencyPhone', 'adress', 'ailments', 'limitation'
    #         ]

    #         # Nombres en español de los campos
    #         field_names_es = {
    #             'documentId': 'Cedula',
    #             'name': 'Nombre',
    #             'firstLastName': 'Primer_Apellido',
    #             'secondLastName': 'Segundo_Apellido',
    #             'Date_Birth': 'Fecha_Nacimiento',
    #             'age': 'Edad',
    #             'mail': 'Correo',
    #             'phone': 'Telefono',
    #             'ocupation': 'Ocupacion',
    #             'emergencyPhone': 'TelefonoEmergencia',
    #             'adress': 'Direccion',
    #             'ailments': 'Padecimientos',
    #             'limitation': 'Limitacion'
    #             }


    #         # Validar campos vacíos
    #         for field in required_fields:
    #             value = request.form.get(field, '').strip()
    #             if not value:
    #                 nombre_es = field_names_es.get(field, field)
    #                 raise Exception(f"El campo '{nombre_es}' es obligatorio y no puede estar vacío.")

    #         document_id = request.form['documentId']

    #         # Validar que el cliente no exista ya
    #         existing_client = cls.ClientRepository.findOne_any({'DocumentId': document_id})
    #         if existing_client:
    #             raise Exception(f"Ya existe un cliente registrado con la cédula '{document_id}'.")

    #         # Procesar fecha de nacimiento
    #         Date_BirthStr = request.form['Date_Birth']
    #         Date_Birth = datetime.strptime(Date_BirthStr, "%Y-%m-%d").date()
    #         today = datetime.today().date()
    #         age = today.year - Date_Birth.year - ((today.month, today.day) < (Date_Birth.month, Date_Birth.day))

    #         data = {
    #             'DocumentId': document_id,
    #             'Name': request.form['name'],
    #             'First_LastName': request.form['firstLastName'],
    #             'Second_LastName': request.form['secondLastName'],
    #             'Date_Birth': Date_Birth,
    #             'Age': age,
    #             'Mail': request.form['mail'],
    #             'Phone': request.form['phone'],
    #             'Registration_Date': None,
    #             'Occupation': request.form['ocupation'],
    #             'TelephoneEmergency': request.form['emergencyPhone'],
    #             'Address': request.form['adress'],
    #             'Entry_Date': None,
    #             'Ailments': request.form['ailments'],
    #             'Limitation': request.form['limitation'],
    #             'ExpirationMembership': None,
    #             'State': True,
    #             'Membership_ID': None
    #         }

    #         return cls.ClientRepository.create(**data)

    #     except Exception as ve:
    #         raise Exception(f"Validación de formulario fallida: {ve}")

