from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id = None, DocumentId = None, Password = None, State = None, role = None, CreationDate = None, Email = None) -> None:
        self.id = id
        self.DocumentId = DocumentId
        self.Password = Password
        self.State = State
        self.role = role
        self.CreationDate = CreationDate
        self.Email = Email

    @classmethod
    def verifyPassword(self, hash_password, password):
        return check_password_hash(hash_password, password)
    
    @classmethod
    def generate_password_hash(self, password):
        return generate_password_hash(password)