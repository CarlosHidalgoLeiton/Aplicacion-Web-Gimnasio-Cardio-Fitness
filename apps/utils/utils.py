import secrets
import re
from werkzeug.security import check_password_hash, generate_password_hash
from apps.db.models.Product import Product
import base64
from datetime import datetime
from apps.db.models.Routine import Routine

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
    return generate_password_hash(password)



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
    if image_file and image_file.filename != '' and image_file.content_length > 0:
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