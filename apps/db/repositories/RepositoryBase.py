from apps.db.db import db
from sqlalchemy.orm import joinedload


class RepositoryBase:

    def __init__(self, model):
        self.model = model

    def _instance_to_dict(self, instance):
        """Convierte una instancia del modelo a diccionario."""
        return {column.name: getattr(instance, column.name) for column in instance.__table__.columns}

    def _load_relations(self, query, relations):
        """
        Carga las relaciones (joins) necesarias si se proporcionan en 'relations'.
        """
        if relations:
            for relation in relations:
                query = query.options(joinedload(relation))
        return query

    def get_one(self, id, relations=None):
        try: 
            instance = self.model.query.get(id)
            return self._instance_to_dict(instance) if instance else None
        except Exception as ex:
            raise Exception(f'Error en get_one para {self.model}: {ex}')


    def findAll(self, filters=None, relations=None):
        try:
            query = db.session.query(self.model)

            # Cargar relaciones si existen
            query = self._load_relations(query, relations)

            if filters:
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        raise Exception(f"Columna '{key}' no existe en {self.model}")
                    query = query.filter(column == value)

            results = query.all()

            # Convertimos todas las instancias a diccionarios
            return [self._instance_to_dict(result) for result in results]

        except Exception as ex:
            raise Exception(f'Error en findAll para {self.model}: {ex}')


    def findAllFiltered(self, column_names, filters=None, relations=None):
        try:
            columns = [getattr(self.model, name) for name in column_names]

            query = db.session.query(*columns)

            # Cargar relaciones si existen
            query = self._load_relations(query, relations)

            if filters:
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        raise Exception(f"Columna '{key}' no existe en {self.model}")
                    query = query.filter(column == value)

            results = query.all()

            # Convertimos cada fila en un diccionario
            json_result = []
            for result in results:
                result_dict = {column.name: value for column, value in zip(columns, result)}
                json_result.append(result_dict)

            return json_result

        except Exception as ex:
            raise Exception(f'Error en findAllFiltered para {self.model}: {ex}')

    
    def findOne(self, filters=None, relations=None):
        try:
            query = db.session.query(self.model)

            # Cargar relaciones si existen
            query = self._load_relations(query, relations)

            if filters:
                for key, value in filters.items():
                    column = getattr(self.model, key, None)
                    if column is None:
                        raise Exception(f"Columna '{key}' no existe en {self.model}")
                    query = query.filter(column == value)

            result = query.first()
            return self._instance_to_dict(result) if result else None

        except Exception as ex:
            raise Exception(f'Error en findOne para {self.model}: {ex}')

    
    def findOneFiltered(self, column_names, filters=None, relations=None):
        try:
            columns = [getattr(self.model, name) for name in column_names]

            query = db.session.query(*columns)

            # Cargar relaciones si existen
            query = self._load_relations(query, relations)

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
