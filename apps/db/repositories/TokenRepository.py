from apps.db.models.TokenUser import TokenUser

from apps.db.repositories.RepositoryBase import RepositoryBase

class TokenRepository(RepositoryBase):

    def __init__(self):
        super().__init__(TokenUser)