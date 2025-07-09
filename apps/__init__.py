from flask import Flask, current_app
from flask_login import LoginManager, current_user
from flask_principal import Principal, Identity, RoleNeed, identity_changed
from apps.db.db import db
from apps.routes.login_app import login_app
from apps.routes.admin_app import admin_app
from apps.routes.client_app import client_app
from apps.routes.trainer_app import trainer_app
from apps.routes.porton_app import porton_app
from apps.db.repositories.UserRepository import UserRepository

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

# --- Identity Loader ---
@principal.identity_loader
def load_identity():
    if current_user.is_authenticated:
        identity = Identity(current_user.id)
        identity.provides.add(RoleNeed(current_user.role))
        print(f"Identidad cargada: {identity}")
        identity_changed.send(current_app._get_current_object(), identity=identity)
        return identity

# --- Ejecutar ---
if __name__ == '__main__':
    app.run(debug=True)