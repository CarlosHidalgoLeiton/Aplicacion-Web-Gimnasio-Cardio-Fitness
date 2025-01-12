

class Routine():

    def __init__(self, RoutineId= None, ClientId = None, TrainerId = None, Indications = None, Date =  None, State = None) -> None:
        self.RoutineId = RoutineId
        self.ClientId = ClientId
        self.TrainerId = TrainerId
        self.Indications = Indications
        self.Date = Date
        self.State = State  


    def to_dict(self):
        return {
            "RoutineId": self.RoutineId,
            "ClientId": self.ClientId,
            "TrainerId": self.TrainerId,
            "Indications": self.Indications,
            "Date": self.Date,
            "State": self.State,
        }  

