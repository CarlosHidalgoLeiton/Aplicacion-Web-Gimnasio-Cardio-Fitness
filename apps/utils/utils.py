import secrets

def generateToken():
    token = secrets.token_urlsafe(32)

    return token