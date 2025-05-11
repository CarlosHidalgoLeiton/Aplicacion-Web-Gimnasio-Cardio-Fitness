import secrets
import re
from werkzeug.security import check_password_hash, generate_password_hash

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