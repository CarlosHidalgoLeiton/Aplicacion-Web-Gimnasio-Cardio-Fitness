import secrets
import re
from werkzeug.security import check_password_hash, generate_password_hash
from apps.db.models.Product import Product
import base64
from datetime import datetime
from apps.db.models.Routine import Routine
from apps.db.models.Statistics import Statistics
from apps.db.models.User import User

def generateToken():
    token = secrets.token_urlsafe(32)

    return token

def validateBothPasswords(pwd1, pwd2):
    if pwd1 != pwd2:
        return "Las contraseñas no coinciden"

    if len(pwd1) < 8:
        return "La contraseña debe tener al menos 8 caracteres"

    if not re.search(r"[A-Z]", pwd1):
        return "La contraseña debe contener al menos una letra mayúscula"

    if not re.search(r"[a-z]", pwd1):
        return "La contraseña debe contener al menos una letra minúscula"

    if not re.search(r"[0-9]", pwd1):
        return "La contraseña debe contener al menos un número."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", pwd1):
        return "La contraseña debe contener al menos un carácter especial"
    
    return True

def hashPassword(password):
    return generate_password_hash(password, method='pbkdf2:sha256')



def getDataProductInsert( request, image):
    name = request.form['Name']
    detail = request.form['Detail']
    price = request.form['Price']
    stock = request.form['Stock']
    image_file = request.files['Image']
    image_blob = None
    if image:
        if not image_file or image_file.content_length == 0:
            # image es ya un blob, úsalo directamente
            image_blob = image
        else:
            image_blob = image_file.read()
    
    else:
        if image_file:
            image_blob = image_file.read()


    return Product(
        Name = name,
        Detail = detail,
        Price = price,
        Stock = stock,
        Image = image_blob,
        State = True
    )

def getDataUpdateProductUpdate(request, previous_image_blob):
    ID_Product = request.form['ID_Product']
    name = request.form['Name']
    detail = request.form['Detail']
    price = request.form['Price']
    stock = request.form['Stock']
    image_file = request.files['Image'] # Usa get para evitar errores si no está

    # Prioriza la nueva imagen si fue cargada
    if image_file and image_file.filename != '':
        image_blob = image_file.read()
    else:
        image_blob = previous_image_blob  # Usa la imagen anterior

    return Product(
        ID_Product=ID_Product,
        Name=name,
        Detail=detail,
        Price=price,
        Stock=stock,
        Image=image_blob,
        State=True
    )
   

def validateDataProduct( product):
    # Validar que la imagen no sea None o esté vacía
    if not product.Image:
        print("La imagen del producto es requerida.")
        return False
    
    if product.Price is not None:
        if any(p.isalpha() for p in str(product.Price)):
            return "El precio no debe contener letras."
        elif any(p in "-$" for p in str(product.Price)):  # Verifica si contiene caracteres no permitidos
            return "El precio no debe contener caracteres especiales como '-'."
    else:
        return "Debe ingresar el precio en número."
    
    return True

def getDataRoutine(request):
    ClientId = request.form['ClientId']
    TrainerId = request.form['TrainerId']
    Indications = request.form['Indications']
    Date = datetime.now()

    return Routine(ClientId = ClientId, TrainerId=TrainerId, Indications=Indications, Date=Date)

def validateDataRoutine(routine):

    #Validation for Client
    if routine.ClientId == None:
        return "Debe contener ID cliente"
    
    #Validation for Trainer
    if routine.TrainerId == None:
        return "Debe contener ID de entrenador"
    
    #Validation for Indications
    if routine.Indications == None:
        return "Debe ingresar las indicaciones."

    return True

def getDataStatistics(request):
    # Extraer datos del formulario
    Measurement_DateStr = request.form.get('Measurement_Date')
    Measurement_Date = datetime.strptime(Measurement_DateStr, "%Y-%m-%d").date() if Measurement_DateStr else None
    Stature = request.form['Stature']
    Weight = request.form['Weight']
    IMC = request.form['IMC']
    FC_Repose = request.form['FC_Repose']
    FC_MAX = request.form['FC_MAX']
    Blood_pressure = request.form['Blood_pressure']
    BMR = request.form['BMR']
    Body_Fat = request.form['Body_Fat']
    Percent_Water = request.form['Percent_Water']
    Muscle_Mass = request.form['Muscle_Mass']
    Metabolic_Age = request.form['Metabolic_Age']
    Bone_Mass = request.form['Bone_Mass']
    Visceral_Fat = request.form['Visceral_Fat']
    Chest_Circum = request.form['Chest_Circum']
    Right_Arm_Circum = request.form['Right_Arm_Circum']
    Left_Arm_Circum = request.form['Left_Arm_Circum']
    Circum_Waist = request.form['Circum_Waist']
    Circum_Abdomen = request.form['Circum_Abdomen']
    Hip_Circum = request.form['Hip_Circum']
    Circum_Thigh_Right = request.form['Circum_Thigh_Right']
    Circum_Thigh_Left = request.form['Circum_Thigh_Left']
    Circum_Calf_Right = request.form['Circum_Calf_Right']
    Circum_Calf_Left = request.form['Circum_Calf_Left']
    Special_Considerations = request.form['Special_Considerations']
    sportsman = request.form['sportsman']
    Training_Goal = request.form['Training_Goal']
    Emphasis_Training = request.form['Emphasis_Training']
    Disponibilidad = request.form['Disponibilidad']
    State = request.form['State']
    Client_ID = request.form['Client_ID']
    Trainer_ID = request.form['Trainer_ID']

    # Retornar una instancia de Statistics
    return Statistics(
        Measurement_Date=Measurement_Date,
        Stature=Stature,
        Weight=Weight,
        IMC=IMC,
        FC_Repose=FC_Repose,
        FC_MAX=FC_MAX,
        Blood_pressure=Blood_pressure,
        BMR=BMR,
        Body_Fat=Body_Fat,
        Percent_Water=Percent_Water,
        Muscle_Mass=Muscle_Mass,
        Metabolic_Age=Metabolic_Age,
        Bone_Mass=Bone_Mass,
        Visceral_Fat=Visceral_Fat,
        Chest_Circum=Chest_Circum,
        Right_Arm_Circum=Right_Arm_Circum,
        Left_Arm_Circum=Left_Arm_Circum,
        Circum_Waist=Circum_Waist,
        Circum_Abdomen=Circum_Abdomen,
        Hip_Circum=Hip_Circum,
        Circum_Thigh_Right=Circum_Thigh_Right,
        Circum_Thigh_Left=Circum_Thigh_Left,
        Circum_Calf_Right=Circum_Calf_Right,
        Circum_Calf_Left=Circum_Calf_Left,
        Special_Considerations=Special_Considerations,
        sportsman= True if sportsman == 'True' else False,
        Training_Goal=Training_Goal,
        Emphasis_Training=Emphasis_Training,
        Disponibilidad=Disponibilidad,
        State=True if (State == '1' or State == 'True') else False,
        Client_ID=Client_ID,
        Trainer_ID=Trainer_ID
    )

def validateDataStatistics(statistics, isUpdate = False):

    #Validation for Measurement_Date
    if statistics.Measurement_Date is not None:
        # Convertir a datetime si es un string
        if isinstance(statistics.Measurement_Date, str):
            measurement_date = datetime.strptime(statistics.Measurement_Date, '%Y-%m-%d').date()
        else:
            measurement_date = statistics.Measurement_Date

        # Comprobar si la fecha obtenida es diferente de la fecha actual
        if measurement_date != datetime.now().date() and not isUpdate:
            return "La fecha de medición debe ser la fecha actual."
    else:
        return "No se logro obtener la fecha de medición "
                    
    #Validation for documentID 
    if statistics.Client_ID == None:
        return "No se logro enlazar con el cliente, por favor inténtalo más tarde."
    
    if statistics.Trainer_ID == None:
        return "No se logro enlazar con el cliente, por favor inténtalo más tarde."

    return True
    
 
def validateDataUserForm(user):
    
    # Validación para DocumentId
    if user.DocumentId is None:
        return "Debe ingresar el número de cédula."
    
    if user.Password is None or user.ConfirmPassword is None:
        return "Debe ingresar la contraseña y su confirmación."

    if user.Password != user.ConfirmPassword:
        return "Las contraseñas no coinciden."

    if len(user.Password) < 8:
        return "La contraseña debe tener al menos 8 caracteres."

    if not re.search(r"[A-Z]", user.Password):
        return "La contraseña debe contener al menos una letra mayúscula."

    if not re.search(r"[a-z]", user.Password):
        return "La contraseña debe contener al menos una letra minúscula."

    if not re.search(r"[0-9]", user.Password):
        return "La contraseña debe contener al menos un número."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user.Password):
        return "La contraseña debe contener al menos un carácter especial."

    # Validación para correo
    if user.Email is None:
        return "Debe ingresar el correo."
    
    expression = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Validar formato de correo
    if not re.match(expression, user.Email):
        return "El correo ingresado no es válido."

    # Si todas las validaciones pasan, devuelve el objeto User
    return True



def validateDataUserFormUpdate(user):
    

    # Validación para DocumentId
    if user.DocumentId is None:
        return "Debe ingresar el número de cédula."
    
    if user.Password is None or user.ConfirmPassword is None:
        return "Debe ingresar la contraseña y su confirmación."

    if user.Password and user.ConfirmPassword:
        if user.Password != user.ConfirmPassword:
            return "Las contraseñas no coinciden."

        if len(user.Password) < 8:
            return "La contraseña debe tener al menos 8 caracteres."

        if not re.search(r"[A-Z]", user.Password):
            return "La contraseña debe contener al menos una letra mayúscula."

        if not re.search(r"[a-z]", user.Password):
            return "La contraseña debe contener al menos una letra minúscula."

        if not re.search(r"[0-9]", user.Password):
            return "La contraseña debe contener al menos un número."

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user.Password):
            return "La contraseña debe contener al menos un carácter especial."

    # Validación para correo
    if user.Email is None:
        return "Debe ingresar el correo."
    
    expression = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # Validar formato de correo
    if not re.match(expression, user.Email):
        return "El correo ingresado no es válido."

    # Si todas las validaciones pasan, devuelve el objeto User
    return True