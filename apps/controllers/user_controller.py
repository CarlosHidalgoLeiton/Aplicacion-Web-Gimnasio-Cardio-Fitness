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

        user = cls.userRepository.findOne(filters={'Cedula': id})

        if user:
            if User.verifyPassword(user.Contrasena, password):
                return user
            else:
                raise Exception('Usuario o contraseña incorrectos')

        else:
            raise Exception('Usuario o contraseña incorrectos')

    @classmethod
    def sendEmail(cls, request):
        documentId = request.form['documentId']

        if not documentId:
            raise Exception('La cédula es requerida')
        
        email = cls.userRepository.findAll(column_names=['Correo'], filters={'Cedula': documentId})

        if not email:
            raise Exception('No se ha encontrado ningún correo relacionado con el número de cédula ingresado')

        return email

    # def get_by_id(id):
    #     try:
    #         user = UserRepository.findOne(id)
    #     except Exception as ex:
    #         raise Exception(f'Error en user.controller.py {ex}')