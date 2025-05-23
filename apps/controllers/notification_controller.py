from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.NotificationRepository import NotificationRepository
from datetime import datetime, date
from apps.db.models.Notification import Notification

class notificationController:

    NotificationRepository = NotificationRepository()

    @classmethod
    def getNotifications(cls):
        notifications = cls.NotificationRepository.findAll()
        if not notifications:
            raise Exception('No se encontraron notificaciones')
        return notifications

    @classmethod
    def get_all(cls):
        notifications = cls.NotificationRepository.findAll()
        if not notifications:
            raise Exception('No se encontraron notificaciones')
        return notifications
        

    @classmethod
    def create(cls, data):
        dataNotification = cls.NotificationRepository.to_dict(data)
        notification = cls.NotificationRepository.create(**dataNotification)
        return notification
    
        
 

    @classmethod
    def CreateData(cls, request):
        subject = request.form['Subject']
        date_str = request.form['Date']
        hour_str = request.form['Hour']

        # Convertir cadenas a tipos nativos
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        hour = datetime.strptime(hour_str, "%H:%M").time()

        # Crear la instancia del modelo Notification
        notification_instance = Notification(
            Subject=subject,
            Date=date,
            Hour=hour,
            State=True
        )

        # Guardar la instancia en la base de datos
        notification = cls.create(notification_instance)
        return notification



        
        

           


    @classmethod
    def updateClient(cls,id, data):
        dataClient = cls.NotificationRepository.to_dict(data)
        cliente = cls.NotificationRepository.update(id,**dataClient)
        return cliente

    @classmethod
    def get_one(cls,id):
         return cls.NotificationRepository.get_one(id)

    @classmethod
    def disableNotification(cls, id):
         return cls.NotificationRepository.disableNotification(id)
    
    @classmethod
    def ableNotification(cls, id):
         return cls.NotificationRepository.ableNotification(id)
        
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
    #         existing_client = cls.ClientRepository.findOne({'DocumentId': document_id})
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

