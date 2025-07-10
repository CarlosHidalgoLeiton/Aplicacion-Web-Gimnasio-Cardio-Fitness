from flask import Flask, current_app
from flask_login import LoginManager, current_user
from flask_principal import Principal, Identity, RoleNeed, identity_changed
from apps.db.db import db
from apps.routes.login_app import login_app
from apps.routes.admin_app import admin_app
from apps.routes.client_app import client_app
from apps.routes.landingPage_app import landingPage_app
from apps.routes.trainer_app import trainer_app
from apps.routes.porton_app import porton_app
from apps.db.repositories.UserRepository import UserRepository
from apps.db.models.User import User

# --- Inicialización ---
app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = 'your_secret_key'

# --- Extensiones ---
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

principal = Principal()
principal.init_app(app)

# --- Blueprints ---
app.register_blueprint(landingPage_app)
app.register_blueprint(login_app)
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(client_app, url_prefix='/client')
app.register_blueprint(trainer_app, url_prefix='/trainer')
app.register_blueprint(porton_app)


# --- User Loader ---
user_cache = {}

@login_manager.user_loader
def load_user(user_id):
    userRepository = UserRepository()
    if user_id in user_cache:
        return user_cache[user_id]
    
    user = userRepository.get_one(user_id)
    if user:
        user_cache[user_id] = user
    return user

@principal.identity_loader
def load_identity():
    try:
        # No tocar current_user si no hay sesión activa
        if not hasattr(current_user, 'is_authenticated') or not current_user.is_authenticated:
            return None

        # Si está autenticado, cargamos su identidad desde la base de datos (seguro)
     
        user = db.session.get(User, current_user.id)

        if user:
            identity = Identity(user.id)
            identity.provides.add(RoleNeed(user.role))
            identity_changed.send(current_app._get_current_object(), identity=identity)
            print(f"Identidad cargada: {identity}")
            return identity

    except Exception as e:
        print(f"Error en load_identity: {e}")
        return None


# --- Ejecutar ---
if __name__ == '__main__':
    app.run(debug=True)