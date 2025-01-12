from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class RepositoryBase:
    def __init__(self, model):
        self.model = model

    def get_all(self):
        try:
            return self.model.query.all()
        except:
            raise Exception(f'Error get_all para {self.model}')

    def get_one(self, id):
        try: 
            return self.model.query.get(id)
        except:
            raise Exception(f'Error get_one para {self.model}')


    def create(self, **kwargs):
        try:
            instance = self.model(**kwargs)
            db.session.add(instance)
            db.session.commit()
        except:
            db.session.rollback()
            raise Exception(f'Error create para {self.model}')
        

    def update(self, id, **kwargs):
        try:
            instance = self.model.get(id)
            if instance:
                for key, value in kwargs.items():
                    setattr(instance, key, value)
                db.session.commit()
            return instance
        except:
            raise Exception(f'Error update para {self.model}')

    def delete(self, id):
        try:
            instance = self.model.query.get(id)
            if instance:
                db.session.delete(instance)
                db.session.commit()
        except:
            raise Exception(f'Error delete para {self.model}')