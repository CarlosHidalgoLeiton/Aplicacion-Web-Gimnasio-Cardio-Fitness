class Baserepository:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        return self.model.query.all()
    
    