from apps.db.models.User import User
from apps.db.models.Client import Client
from apps.db.models.Trainer import Trainer
from apps.db.conection import Conection
from datetime import datetime, timedelta
import re

from apps.db.repositories.RepositoryBase import RepositoryBase

class UserRepository(RepositoryBase):

    def __init__(self):
        super().__init__(User)
        
    @classmethod
    def getDataUser(cls, request):
        DocumentId = None

        role = request.form['Role']
        State = request.form['State']
        
        if role == 'Admin':
            DocumentId = request.form.get('DocumentId')
        elif role == 'Trainer':
            DocumentId = request.form.get('DocumentIdTrainer')
        elif role == 'Client':
            DocumentId = request.form.get('DocumentIdClient')

        Password = request.form.get('Password')
        ConfirmPassword = request.form.get('ConfirmPassword')
        
        
        CreationDate = datetime.now()
        Email = request.form.get('Email')

        user = User(
            DocumentId=DocumentId,
            Password=Password,
            State=State,
            role=role,
            CreationDate=CreationDate,
            Email=Email
        )
        
         # Esto es clave: agregar el campo temporalmente
        user.ConfirmPassword = ConfirmPassword

        return user


    @classmethod
    def getDataUserUpdate(cls, request):

        DocumentId = request.form['DocumentId']
        State = request.form['State']
        role = request.form['Role']
        Password = request.form['Password']
        ConfirmPassword = request.form['ConfirmPassword']
        Email = request.form['Email']
        CreationDate = request.form['CreationDate']

        user = User(
            DocumentId=DocumentId,
            Password=Password,
            State=State,
            role=role,
            CreationDate=CreationDate,
            Email=Email
        )
        
         # Esto es clave: agregar el campo temporalmente
        user.ConfirmPassword = ConfirmPassword

        return user

    
    @classmethod
    def document_exists(cls, conexion, document_id):
        cursor = conexion.cursor()
        cursor.execute("SELECT COUNT(*) FROM Usuario WHERE Cedula = %s", (document_id,))
        count = cursor.fetchone()[0]
        cursor.close()
        return count > 0
    
 
    def disable_user(self, DocumentId):
        return self.update(DocumentId, State=0) 

    def able_user(self, DocumentId):
        return self.update(DocumentId, State=1) 

