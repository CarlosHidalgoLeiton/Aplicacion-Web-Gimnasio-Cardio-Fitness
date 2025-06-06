from apps.db.repositories.UserRepository import UserRepository
from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.TrainerRepository import TrainerRepository
from apps.db.repositories.TokenRepository import TokenRepository
from apps.db.models.User import User
from apps.utils.utils import generateToken
from datetime import datetime, timedelta
from notifications.emailTest import manageEmail
from apps.utils.utils import validateBothPasswords, generate_password_hash, validateDataUserForm, validateDataUserFormUpdate


class userController:

    userRepository = UserRepository()
    clientRepository = ClientRepository()
    trainerRepository = TrainerRepository()
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
        

    @classmethod
    def get_all(cls):
        users = cls.userRepository.findAll()
        if not users:
            raise Exception('No se encontraron usuarios')
        return users

    @classmethod
    def get_Clients(cls):
        clients = cls.clientRepository.findAll()
        users = cls.userRepository.findAll()

        if not clients:
            raise Exception('No se encontraron clientes')

        # Obtener todas las cédulas de los usuarios
        user_cedulas = set(user['DocumentId'] for user in users)

        # Filtrar clientes cuya cédula NO esté en usuarios
        filtered_clients = [client for client in clients if client['DocumentId'] not in user_cedulas]

        return filtered_clients

    @classmethod
    def get_Trainers(cls):
        trainers = cls.trainerRepository.findAll()
        users = cls.userRepository.findAll()

        if not trainers:
            raise Exception('No se encontraron clientes')

        # Obtener todas las cédulas de los usuarios
        user_cedulas = set(user['DocumentId'] for user in users)

        # Filtrar clientes cuya cédula NO esté en usuarios
        filtered_trainer = [trainer for trainer in trainers if trainer['DocumentId'] not in user_cedulas]

        return filtered_trainer

    @classmethod
    def getUser(cls, documentId):
        user = cls.userRepository.findOne(filters={'DocumentId': documentId})
        return user
    
    @classmethod
    def get_one(cls,id):
         return cls.userRepository.get_one(id)
    

    @classmethod
    def getData(cls, request):
        return cls.userRepository.getDataUser(request)
    
    @classmethod
    def getDataUpdate(cls, request):
        return cls.userRepository.getDataUserUpdate(request)
    
    @classmethod
    def validateDataForm(cls, request):
        existing_user = cls.userRepository.findOne({'DocumentId': request.DocumentId})
        if existing_user:
            return f"Ya existe un usuario registrado con la cédula '{request.DocumentId}'."
        else:
            return  validateDataUserForm(request)
        
    @classmethod
    def validateDataFormUpdate(cls, request, DocumentId):
        existing_user = cls.userRepository.findOne({'DocumentId': request.DocumentId})
        if existing_user.DocumentId and DocumentId != existing_user.DocumentId:
            raise Exception("No se puede actualizar, debido a que existe el usuario con la cedula " + DocumentId )
        return  validateDataUserFormUpdate(request)

    
    @classmethod
    def create(cls, data):
        dataUser = cls.userRepository.to_dict(data)
        user = cls.userRepository.create(**dataUser)
        return user
    
    @classmethod
    def updateUser(cls,id, data):
        dataUser = cls.userRepository.to_dict(data)
        del dataUser['id']
        user = cls.userRepository.update(id,**dataUser)
        return user
    
    @classmethod
    def disable_user(cls, id):
        user = cls.userRepository.findOne({'DocumentId': id})
        return cls.userRepository.disable_user(user.id)
    
    @classmethod
    def able_user(cls, id):
        user = cls.userRepository.findOne({'DocumentId': id})
        return cls.userRepository.able_user(user.id)
    

    
        
    
    # def get_by_id(id):
    #     try:
    #         user = UserRepository.findOne(id)
    #     except Exception as ex:
    #         raise Exception(f'Error en user.controller.py {ex}')