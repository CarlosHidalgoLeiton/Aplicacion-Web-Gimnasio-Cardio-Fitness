

class Trainer():

    def __init__(self, DocumentId = None, Name = None, First_LastName = None, Second_LastName = None, Date_Birth =  None, Age = None, Mail = None, Phone = None, State = None) -> None:
        self.DocumentId = DocumentId
        self.Name = Name
        self.First_LastName = First_LastName
        self.Second_LastName = Second_LastName
        self.Date_Birth = Date_Birth
        self.Age = Age
        self.Mail = Mail
        self.Phone = Phone
        self.State = State

    # def __str__(self):
    #     return (f"Trainer(DocumentId={self.DocumentId}, Name={self.Name}, "
    #             f"lastName={self.lastName}, lastName2={self.lastName2}, "
    #             f"DateOfBirth={self.DateOfBirth}, Age={self.Age}, "
    #             f"Email={self.Email}, Phone={self.Phone}, State={self.State})")
