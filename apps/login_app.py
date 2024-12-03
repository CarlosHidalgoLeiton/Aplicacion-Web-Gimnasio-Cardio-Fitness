from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_user, logout_user,current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.ModelClient import ModelClient
from db.models.entities.User import User
from db.models.entities.Client import Client


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


@login_app.route("/entryInstallation", methods=["GET", "POST"])
def entryInstallation():
    if request.method == "POST":
        user_document_id = request.form['DocumentId']
        try:
            conexion = Conection.conectar()
            client = ModelClient.getClient(conexion, user_document_id)
            if client is not None:
                if client.is_member_active():
                    success_message = f"Acceso Permitido. Bienvenido {client.Name}. Su membresía finaliza el {client.ExpirationMembership}."
                    return render_template("login/entryInstallationStatus.html", success_message=success_message)
                else:
                    error_message = "Acceso Denegado. Su membresía ha expirado."
                    return render_template("login/entryInstallationStatus.html", error=error_message)
            else:
                error_message = "Cliente no encontrado."
                return render_template("login/entryInstallationStatus.html", error=error_message)
        
        except Exception as e:
            print(e)
            error_message = "Hubo un error en el sistema. Inténtelo más tarde."
            return render_template("login/entryInstallationStatus.html", error=error_message)
        finally:
            Conection().desconectar()

    return render_template("login/entryInstallation.html")

@login_app.route("/entryInstallationStatus")
def entryInstallationStatus():
    return render_template("login/entryInstallationStatus.html")

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
                        if logged_user != "DataBase":
                            if type(logged_user) == User:
                                login_user(logged_user)
                                if logged_user.role == "Admin":
                                    return redirect(url_for('admin_app.inicio'))
                                elif logged_user.role == "Client":
                                    return redirect(url_for('client_app.inicio'))
                                elif logged_user.role == 'Trainer':
                                    return redirect(url_for('trainer_app.inicio'))
                                else:
                                    return render_template("login/login.html")
                            else:
                                return render_template("login/login.html", error="Ha ocurrido un error. Intentelo más tarde.")
                        else:
                            return render_template("login/login.html", error="No se pudo obtener la información. Contáctese con el desarrollador.")
                    else:
                        return render_template("login/login.html", error="Contraseña no válida.")
                else:
                    return render_template("login/login.html", error="Su usuario esta inactivo. Inténtalo de nuevo más tarde o comuniquese con el administrador")
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