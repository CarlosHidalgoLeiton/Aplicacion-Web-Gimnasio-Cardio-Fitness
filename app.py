from flask import Flask
from apps.admin_app import admin_app
from apps.client_app import client_app
from apps.trainer_app import trainer_app
from apps.login_app import login_app
from db.conection import Conection
from flask_login import LoginManager
from db.models.ModelUser import ModelUser

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Establece una clave secreta para la gestión de sesiones

# Inicializa el gestor de inicio de sesión
login_manager_app = LoginManager(app)
login_manager_app.init_app(app)



# Revisar si esto es necesario
# Crea una conexión a la base de datos dentro del contexto de la aplicación
# with app.app_context():
#     db = Conection()
#     app.conexion = db.conectar()  # Establecer la conexión aquí

@login_manager_app.user_loader
def load_user(user_id):
    return ModelUser.get_by_id(Conection.conectar(), user_id)

# Registra los blueprints
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(client_app, url_prefix='/client')
app.register_blueprint(trainer_app, url_prefix='/trainer')
app.register_blueprint(login_app)

if __name__ == '__main__':
    app.run(debug=True)