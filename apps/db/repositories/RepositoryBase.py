from apps.db.db import db

class RepositoryBase:

    def __init__(self, model):
        self.model = model
    
    def get_one(self, id):
        try: 
            return self.model.query.get(id)
        except Exception as ex:
            raise Exception(f'Error en get_one para {self.model}: {ex}')

    def findAll(self, filters=None):
        try:
            query = db.session.query(self.model) 

            if filters:
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        raise Exception(f"Columna '{key}' no existe en {self.model}")
                    query = query.filter(column == value)

            return query.all() 
        except Exception as ex:
            raise Exception(f'Error en findAll para {self.model}: {ex}')

    def findAllFiltered(self, column_names, filters=None):
        try:
            columns = [getattr(self.model, name) for name in column_names]

            query = db.session.query(*columns)

            if filters:
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        raise Exception(f"Columna '{key}' no existe en {self.model}")
                    query = query.filter(column == value)

            return query.all()

        except Exception as ex:
            raise Exception(f'Error en findAllFiltered para {self.model}: {ex}')
    
    def findOne(self, filters=None):
        try:
            query = db.session.query(self.model)

            if filters:
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        raise Exception(f"Columna '{key}' no existe en {self.model}")
                    query = query.filter(column == value)

            return query.first()
        except Exception as ex:
            raise Exception(f'Error en findOne para {self.model}: {ex}')
    
    def findOneFiltered(self, column_names, filters=None):
        try:
            columns = [getattr(self.model, name) for name in column_names]

            query = db.session.query(*columns)

            if filters:
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        raise Exception(f"Columna '{key}' no existe en {self.model}")
                    query = query.filter(column == value)

            result = query.first()
            return dict(zip(column_names, result)) if result else None
        except Exception as ex:
            raise Exception(f'Error en findOneFiltered para {self.model}: {ex}')

    def create(self, **kwargs):
        try:
            instance = self.model(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
        except Exception as ex:
            db.session.rollback()
            raise Exception(f'Error en create para {self.model}: {ex}')
        
    def update(self, id, **kwargs):
        try:
            instance = self.get_one(id)
            if not instance:
                raise Exception(f'{self.model} con id {id} no encontrado')

            for key, value in kwargs.items():
                if hasattr(instance, key):
                    setattr(instance, key, value)

            db.session.commit()
            return instance
        except Exception as ex:
            db.session.rollback()
            raise Exception(f'Error en update para {self.model}: {ex}')

    def delete(self, id):
        try:
            instance = self.get_one(id)
            if instance:
                db.session.delete(instance)
                db.session.commit()
        except Exception as ex:
            raise Exception(f'Error en delete para {self.model}: {ex}')