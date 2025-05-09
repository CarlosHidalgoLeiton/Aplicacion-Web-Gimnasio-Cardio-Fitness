"""Notification Module"""

from apps.db.models.Notification import Notification
from apps.db.repositories.RepositoryBase import RepositoryBase


class NotificationRepository(RepositoryBase):

    def __init__(self):
        super().__init__(Notification)

    @classmethod
    def disableNotification(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Notificacion SET Estado = 0  WHERE ID_Notificacion = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    
                    return True
                else:
                    print("No se pudo actualizar la notificacion.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar la notificacion {ex}")
                conection.rollback()
                return False
        else:
            return False
        
    @classmethod
    def ableNotification(cls, conection, DocumentId):
        if DocumentId != None:
            try:
                cursor = conection.cursor()
                sql = """UPDATE Notificacion SET Estado = 1  WHERE ID_Notificacion = %s"""
                cursor.execute(sql, (DocumentId))
                if cursor.rowcount > 0:
                    conection.commit()
                    return True
                else:
                    print("No se pudo actualizar la Notificacion.")
                    conection.rollback()
                    return False

            except Exception as ex:
                print(f"Ocurrió un error en actualizar la Notificacion {ex}")
                conection.rollback()
                return False
        else:
            return False