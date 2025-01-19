from flask import Flask, current_app
from apps.db.db import db
from apps.routes.login_app import login_app
from apps.routes.admin_app import admin_app
from apps.routes.client_app import client_app
from apps.routes.trainer_app import trainer_app

def create_app():
    app = Flask(__name__)

    # Configuración de la base de datos
    app.config.from_object('config.Config')
    app.secret_key = 'your_secret_key'

    # Inicializa la instancia de SQLAlchemy con la app
    db.init_app(app)

    # Registra los blueprints
    app.register_blueprint(login_app)
    app.register_blueprint(admin_app, url_prefix='/admin')
    app.register_blueprint(client_app, url_prefix='/client')
    app.register_blueprint(trainer_app, url_prefix='/trainer')

    return app