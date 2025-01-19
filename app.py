from apps import create_app
from flask_principal import Principal
from flask_login import LoginManager, current_user
from apps.db.repositories.UserRepository import UserRepository
from flask_principal import Principal, Identity, RoleNeed, identity_changed
from flask import current_app

app = create_app()

# Configuración de roles
principal = Principal(app)

# Inicializa el gestor de inicio de sesión
login_manager_app = LoginManager(app)
login_manager_app.init_app(app)


user_cache = {}

@login_manager_app.user_loader
def load_user(user_id):
    userRepository = UserRepository()
    if user_id in user_cache:
        return user_cache[user_id]
    
    user = userRepository.get_one(user_id)
    if user:
        user_cache[user_id] = user  # Almacenar en caché
    return user

@principal.identity_loader
def load_identity():
    if current_user.is_authenticated:
        identity = Identity(current_user.ID_Usuario)
        identity.provides.add(RoleNeed(current_user.Rol))
        print(f"Identidad cargada: {identity}")
        identity_changed.send(current_app._get_current_object(), identity=identity)
        return identity

if __name__ == '__main__':
    app.run(debug=True)