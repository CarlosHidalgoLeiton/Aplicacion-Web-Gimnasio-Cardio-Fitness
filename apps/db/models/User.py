from werkzeug.security import check_password_hash, generate_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User():
    Id = db.Column(db.Integer, primary_key=True)
    DocumentId = db.Column(db.String(60), nullable=False)
    Password = db.Column(db.String(102), nullable=False)
    State = db.Column(db.SmallInteger, nullable=False, default=1)
    Role = db.Column(db.String(50), nullable=False)
    CreationDate = db.Column(db.Date, nullable=False)
    Email = db.Column(db.String(150), nullable=False)

    # def __init__(self, id = None, DocumentId = None, Password = None, State = None, role = None, CreationDate = None, Email = None) -> None:
    #     self.id = id
    #     self.DocumentId = DocumentId
    #     self.Password = Password
    #     self.State = State
    #     self.role = role
    #     self.CreationDate = CreationDate
    #     self.Email = Email

    @classmethod
    def verifyPassword(self, hash_password, password):
        return check_password_hash(hash_password, password)
    
    @classmethod
    def generate_password_hash(self, password):
        return generate_password_hash(password)