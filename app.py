from flask import Flask, current_app
from apps.admin_app import admin_app
from apps.client_app import client_app
from apps.trainer_app import trainer_app
from apps.login_app import login_app
from db.conection import Conection
from flask_login import LoginManager, current_user
from flask_principal import Principal, Identity, RoleNeed, identity_changed
from db.models.ModelUser import ModelUser

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Establece una clave secreta para la gestión de sesiones


#Configuración para los roles
principal = Principal(app)


# Inicializa el gestor de inicio de sesión
login_manager_app = LoginManager(app)
login_manager_app.init_app(app)


user_cache = {}

@login_manager_app.user_loader
def load_user(user_id):
    if user_id in user_cache:
        return user_cache[user_id]
    
    user = ModelUser.get_by_id(Conection.conectar(), user_id)
    if user:
        user_cache[user_id] = user  # Almacenar en caché
    return user

@principal.identity_loader
def load_identity():
    if current_user.is_authenticated:
        identity = Identity(current_user.id)
        identity.provides.add(RoleNeed(current_user.role))
        print(f"Identidad cargada: {identity}")
        identity_changed.send(current_app._get_current_object(), identity=identity)
        return identity

# Registra los blueprints
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(client_app, url_prefix='/client')
app.register_blueprint(trainer_app, url_prefix='/trainer')
app.register_blueprint(login_app)

if __name__ == '__main__':
    app.run(debug=True)