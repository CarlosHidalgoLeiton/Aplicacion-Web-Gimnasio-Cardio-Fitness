from apps.db.repositories.UserRepository import UserRepository
from apps.db.repositories.TokenRepository import TokenRepository
from apps.db.models.User import User
from apps.utils.utils import generateToken
from datetime import datetime, timedelta
from notifications.emailTest import manageEmail
from apps.utils.utils import validateBothPasswords, generate_password_hash

class userController:

    userRepository = UserRepository()
    tokenRepository = TokenRepository()

    @classmethod
    def login(cls, request):

        id = request.form['DocumentId']
        password = request.form['Password']

        if not id:
            raise Exception('El número de cédula es requerido')

        if not password: 
            raise Exception('La contraseña es requerida')

        user = cls.userRepository.findOne(filters={'DocumentId': id})

        if user:
            if User.verifyPassword(user.Password, password):
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

        email = cls.userRepository.findOneFiltered(column_names=['Email'], filters={'DocumentId': documentId})

        if not email:
            raise Exception('No se ha encontrado ningún correo relacionado con el número de cédula ingresado')

        existToken = cls.tokenRepository.findOne(filters = {'CedulaUser': documentId})
        token = generateToken()

        currentTime = datetime.now()

        expiration = currentTime + timedelta(minutes=30)
        manageEmail.sendEmail(documentId, email['Email'], token)

        if existToken:
            save = cls.tokenRepository.update(existToken.IdToken, Token = token, Expiration = expiration)
        else:
            save = cls.tokenRepository.create(CedulaUser = documentId, Token = token, Expiration = expiration)

        return save

    @classmethod               
    def changePassword(cls, request, documentId, token):
        newPassword = request.form['password1']
        confirmPassword = request.form['password2']
        
        if not documentId:
            raise Exception('No se pudo recuperar la información del usuario. Por favor, inténtelo de nuevo más tarde')

        user = cls.userRepository.findOne(filters={'DocumentId': documentId})

        if not user:
            raise Exception('El usuario no ha sido encontrado')

        if not newPassword:
            raise Exception('La nueva contraseña es requerida')
        
        if not confirmPassword:
            raise Exception('Debe confirmar la contraseña')
        
        if not token:
            raise Exception('No se pudo recuperar la información del usuario. Por favor, inténtelo de nuevo más tarde')
        
        existToken = cls.tokenRepository.findOne(filters = {'CedulaUser': documentId})

        if token != existToken.Token:
            raise Exception('No se pudo obtener la información del usuario. Por favor, intente nuevamente')
        
        if existToken.Expiration < datetime.now():
            raise Exception('Debe reenviar el correo para poder cambiar la contraseña')

        validatePassword = validateBothPasswords(newPassword, confirmPassword)

        if validatePassword is not True:
            raise Exception(validatePassword)

        hashedPassword = generate_password_hash(newPassword)

        update = cls.userRepository.update(user.id, Password = hashedPassword)

        return update
        

    # def get_by_id(id):
    #     try:
    #         user = UserRepository.findOne(id)
    #     except Exception as ex:
    #         raise Exception(f'Error en user.controller.py {ex}')