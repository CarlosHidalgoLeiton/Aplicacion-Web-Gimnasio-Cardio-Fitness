from flask_login import UserMixin


class Trainer(UserMixin):

    def __init__(self, DocumentId = None, Name = None, lastName = None, lastName2 = None, DateOfBirth =  None, Age = None, Email = None, Phone = None, State = None) -> None:
        self.DocumentId = DocumentId
        self.Name = Name
        self.lastName = lastName
        self.lastName2 = lastName2
        self.DateOfBirth = DateOfBirth
        self.Age = Age
        self.Email = Email
        self.Phone = Phone
        self.State = State

    def __str__(self):
        return (f"Trainer(DocumentId={self.DocumentId}, Name={self.Name}, "
                f"lastName={self.lastName}, lastName2={self.lastName2}, "
                f"DateOfBirth={self.DateOfBirth}, Age={self.Age}, "
                f"Email={self.Email}, Phone={self.Phone}, State={self.State})")
