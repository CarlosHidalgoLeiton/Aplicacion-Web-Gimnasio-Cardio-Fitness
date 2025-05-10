from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.NotificationRepository import NotificationRepository

class clientController:

    ClientRepository = ClientRepository()

    NotificationRepository = NotificationRepository()

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
            raise Exception('No se encontraron notificaciones')
        return clients
        