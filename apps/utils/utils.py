import secrets
import re
from werkzeug.security import check_password_hash, generate_password_hash
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