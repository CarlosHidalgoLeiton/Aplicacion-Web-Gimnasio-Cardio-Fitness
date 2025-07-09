from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash
from flask_login import login_user, logout_user
from flask_principal import identity_changed, AnonymousIdentity
from apps.db.conection import Conection
from apps.db.repositories.ClientRepository import ClientRepository
import serial
import requests


from apps.controllers.user_controller import userController
from apps.controllers.client_controller import clientController


login_app = Blueprint('login_app', __name__)

SERIAL_PORT = 'COM3'  # Cambia esto al puerto correcto en tu sistema
BAUD_RATE = 9600

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
    logout_user()
    return render_template("login/login.html")


# IP de la laptop autorizada (la que tiene el USB)
def abrir_porton():
    """
    Envía una señal al hardware para abrir el portón.
    """
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            ser.write(b'ABRIR\n')  # Comando que activa el portón
            print("Se envió el comando 'ABRIR' al portón.")
            return True
    except Exception as e:
        print(f"Error al intentar abrir el portón: {e}")
        return False

@login_app.route("/entryInstallation", methods=["GET", "POST"])
def entryInstallation():
    if request.method == "POST":
        user_document_id = request.form['DocumentId']
        try:
            client = clientController.get_one(user_document_id)

            if client is not None:
                if client.is_member_active():
                    try:
                        # Nueva forma: Enviamos orden al propio servidor
                        orden_url = "https://gymcardiofitness.com/ordenar-apertura"

                        response = requests.post(orden_url, timeout=5)

                        if response.status_code == 200:
                            success_message = f"Acceso Permitido. Bienvenido {client.Name}. Su membresía finaliza el {client.ExpirationMembership}."
                        else:
                            success_message = "Acceso Permitido, pero hubo un problema al crear la orden de apertura."
                    
                    except Exception as e:
                        print(f"Error al crear la orden de apertura: {e}")
                        success_message = "Acceso Permitido, pero no se pudo comunicar la orden."

                    return render_template("login/entryInstallationStatus.html", success_message=success_message)
                
                else:
                    error_message = "Acceso Denegado. Su membresía no se encuentra activa."
                    return render_template("login/entryInstallationStatus.html", error=error_message)
            
            else:
                error_message = "Cliente no encontrado."
                return render_template("login/entryInstallationStatus.html", error=error_message)

        except Exception as e:
            print(e)
            error_message = "Hubo un error en el sistema. Inténtelo más tarde."
            return render_template("login/entryInstallationStatus.html", error=error_message)

    return render_template("login/entryInstallation.html")


@login_app.route("/entryInstallationStatus")
def entryInstallationStatus():
    return render_template("login/entryInstallationStatus.html")

@login_app.route("/restartPassword")
def restartPassword():
    return render_template("login/restartPassword.html")

@login_app.route("/sendEmail", methods = ['POST'])
def sendEmail():
    try:
        userController.sendEmail(request)

        flash('Se ha enviado el correo correctamente', 'success')
        return redirect( url_for("login_app.restartPassword") )
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('login_app.restartPassword'))

@login_app.route("/changePassword/<documentId>/<token>", methods=["GET","POST"])
def changePassword(documentId, token):
    if request.method == "POST":
        try:
            userController.changePassword(request, documentId, token)

            flash('Se ha realizado el cambio de contraseña correctamente', 'success')
            
            return redirect(url_for("login_app.inicio"))
        except Exception as ex:
            flash(ex.args[0], 'danger')
            return redirect(url_for("login_app.changePassword",documentId = documentId,token = token))

    return render_template("login/changePassword.html",documentId = documentId, token = token)

@login_app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            logged_user = userController.login(request)

            login_user(logged_user)

            if logged_user.role == "Admin":
                return redirect(url_for('admin_app.inicio'))
            elif logged_user.role == "Client":
                return redirect(url_for('client_app.inicio'))
            elif logged_user.role == 'Trainer':
                return redirect(url_for('trainer_app.inicio'))
            else:
                return render_template("login/login.html")
        except Exception as ex:
            flash(ex.args[0], 'danger')
            return redirect(url_for('login_app.login'))

    return render_template("login/login.html")

@login_app.route("/logout")
def logout():
    logout_user()

    identity_changed.send(current_app._get_current_object(),
    identity=AnonymousIdentity())
    return redirect(url_for('login_app.login'))
