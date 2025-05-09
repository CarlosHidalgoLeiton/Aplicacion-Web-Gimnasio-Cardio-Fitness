class Config:
    # Connection to db
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/gimnasio'
    # SQLALCHEMY_DATABASE_URI = 'mysql://admin:CardioFit2025#@168.231.68.243/gimnasio'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # User logged
    SECRET_KEY = 'your_secret_key'