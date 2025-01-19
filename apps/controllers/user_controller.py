from apps.db.repositories.UserRepository import UserRepository
from apps.db.models.User import User

class userController:

    def __init__(self):
        self.userRepository = UserRepository()

    @classmethod
    def login(self, request):

        try:

            # TODO: Validar que vengan los datos y ver como hacemos las exepciones
            id = request.form['DocumentId']
            password = request.form['Password']

            user = self.userRepository.get_one_by_parameter('Cedula', id)

            if user:
                if User.verifyPassword(user.Contrasena, password):
                    return user
                else:
                    return "Password"
        except Exception as ex:
            return None


    def get_by_id(id):
        try:
            user = UserRepository.get_one(id)
        except Exception as ex:
            raise Exception(f'Error en user.controller.py {ex}')