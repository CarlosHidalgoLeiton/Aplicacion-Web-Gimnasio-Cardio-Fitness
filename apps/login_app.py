from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_user, logout_user,current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.entities.User import User


login_app = Blueprint('login_app', __name__)


#Routes redirectioned, we have to past this to other unique file, and then we call it as an import
@login_app.errorhandler(403)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))

@login_app.errorhandler(401)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))


@login_app.route('/notAutorized')
def notAutorized():
    return "No tienes permisos para ingresar"


@login_app.route("/")
def inicio():
    return render_template("login/login.html")

@login_app.route("/recuperarContrasena")
def recuperarContrasena():
    return render_template("login/recuperarContrasena.html")

@login_app.route("/cambiarContrasena")
def cambiarContrasena():
    return render_template("login/cambiarContrasena.html")

@login_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User( 0 ,request.form['DocumentId'], request.form['Password'])
        # Establecer una conexión a la base de datos
        try:
            conexion = Conection.conectar()  # Cambiado para crear una instancia
            logged_user = ModelUser.login(user, conexion)
            if logged_user != "Invalid User":
                if logged_user != "Inactive":
                    if logged_user != "Password":
                        if type(logged_user) == User:
                            login_user(logged_user)
                            if logged_user.role == "Admin":
                                return redirect(url_for('admin_app.inicio'))
                            elif logged_user.role == "Cliente":
                                return redirect(url_for('client_app.inicio'))
                            elif logged_user.role == 'Trainer':
                                return redirect(url_for('trainer_app.inicio'))
                            else:
                                return render_template("login/login.html")
                        else:
                            return render_template("login/login.html", error="Ha ocurrido un error. Intentelo más tarde.")
                    else:
                        return render_template("login/login.html", error="Contraseña no válida.")
                else:
                    return render_template("login/login.html", error="Su usuario esta inactivo. Comuniquese con el administrador")
            else:
                return render_template("login/login.html", error="Usuario ingresado no es válido.")
        except Exception as e:
            print(e)
        finally:
            Conection().desconectar()  # Cambiado para crear una nueva instancia

    return render_template("login/login.html")

@login_app.route("/logout")
def logout():
    logout_user()

    identity_changed.send(current_app._get_current_object(),
    identity=AnonymousIdentity())
    return redirect(url_for('login_app.login'))