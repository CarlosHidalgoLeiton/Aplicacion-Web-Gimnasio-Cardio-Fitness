from flask import Flask
from apps.admin_app import admin_app
from apps.client_app import client_app
from apps.trainer_app import trainer_app
from apps.login_app import login_app

app = Flask(__name__)

#Registro de los blueprint
app.register_blueprint(admin_app, url_prefix='/admin')
app.register_blueprint(client_app, url_prefix='/client')
app.register_blueprint(trainer_app, url_prefix='/trainer')
app.register_blueprint(login_app)


if __name__ == '__main__':
    app.run(debug=True)