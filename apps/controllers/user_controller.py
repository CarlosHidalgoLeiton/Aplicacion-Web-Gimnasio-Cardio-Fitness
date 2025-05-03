from apps.db.repositories.UserRepository import UserRepository
from apps.db.models.User import User

class userController:

    userRepository = UserRepository()

    @classmethod
    def login(cls, request):

        id = request.form['DocumentId']
        password = request.form['Password']

        if not id:
            raise Exception('El número de cédula es requerido')

        if not password: 
            raise Exception('La contraseña es requerida')

        user = cls.userRepository.get_one_by_parameter('Cedula', id)

        if user:
            if User.verifyPassword(user.Contrasena, password):
                return user
            else:
                raise Exception('Usuario o contraseña incorrectos')

        else:
            raise Exception('Usuario o contraseña incorrectos')

    def get_by_id(id):
        try:
            user = UserRepository.get_one(id)
        except Exception as ex:
            raise Exception(f'Error en user.controller.py {ex}')