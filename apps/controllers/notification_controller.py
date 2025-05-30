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
    def get_one(cls,id):
         return cls.NotificationRepository.get_one(id)

    @classmethod
    def disableNotification(cls, id):
         return cls.NotificationRepository.disableNotification(id)
    
    @classmethod
    def ableNotification(cls, id):
         return cls.NotificationRepository.ableNotification(id)
   
