from flask_login import UserMixin


class Client(UserMixin):

    def __init__(self, DocumentId = None, Name = None, First_LastName = None, Second_LastName = None, Date_Birth =  None, Age = None, Mail = None, Phone = None, Registration_Date = None, Occupation = None, TelephoneEmergency= None, Address = None, Entry_Date = None, Ailments = None, Limitation = None, ExpirationMembership = None, State = None, Membership_ID = None) -> None:
        self.DocumentId = DocumentId
        self.Name = Name
        self.First_LastName = First_LastName
        self.Second_LastName = Second_LastName
        self.Date_Birth = Date_Birth
        self.Age = Age
        self.Mail = Mail
        self.Phone = Phone
        self.Registration_Date = Registration_Date
        self.Occupation = Occupation
        self.TelephoneEmergency = TelephoneEmergency
        self.Address = Address 
        self.Entry_Date = Entry_Date
        self.Ailments = Ailments
        self.Limitation = Limitation
        self.ExpirationMembership = ExpirationMembership
        self.State = State
        self.Membership_ID = Membership_ID


