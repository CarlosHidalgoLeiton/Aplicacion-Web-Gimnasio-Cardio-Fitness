

class Session():

    def __init__(self, Session_ID = None, Indications = None, Exercises = None, Routine_ID  = None, Name = None) -> None:
        self.Session_ID = Session_ID
        self.Indications = Indications
        self.Exercises = Exercises
        self.Routine_ID = Routine_ID
        self.Name = Name

    def to_dict(self):
        return {
            "Session_ID": self.Session_ID,
            "Indications": self.Indications,
            "Exercises": self.Exercises,
            "Routine_ID": self.Routine_ID,
            "Name": self.Name
        }