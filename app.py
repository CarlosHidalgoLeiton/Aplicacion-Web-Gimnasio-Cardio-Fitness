from flask import Flask
from apps.admin_app import admin_app
from apps.client_app import client_app
from apps.trainer_app import trainer_app
from apps.login_app import login_app
from db.conection import config
from flask_mysqldb import MySQL
from flask_login import LoginManager
from db.models.ModelUser import ModelUser

app = Flask(__name__)

# Inicialización de MySQL
db = MySQL(app)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db,id)

#Registro de los blueprint
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(client_app, url_prefix='/client')
app.register_blueprint(trainer_app, url_prefix='/trainer')
app.register_blueprint(login_app)


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
    
    