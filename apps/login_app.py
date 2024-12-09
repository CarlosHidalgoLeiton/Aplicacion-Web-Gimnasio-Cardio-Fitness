from flask import Blueprint, render_template, request, redirect, url_for, current_app
from flask_login import login_user, logout_user,current_user
from flask_principal import identity_changed, Identity, AnonymousIdentity
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.ModelClient import ModelClient
from db.models.entities.User import User
from emailTest import manageEmail
from db.models.entities.Client import Client
import serial


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
    doneMessage = request.args.get('done')
    return render_template("login/login.html",done = doneMessage)




ALLOWED_IP = " 172.16.1.127"  # Reemplaza con la IP de la laptop con el USB

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
        # Verificar si la solicitud proviene de la computadora autorizada
        client_ip = request.remote_addr
        if client_ip != ALLOWED_IP:
            error_message = "Acceso denegado. Esta operación solo puede realizarse desde el dispositivo autorizado."
            return render_template("login/entryInstallationStatus.html", error=error_message)

        user_document_id = request.form['DocumentId']
        conexion = None
        try:
            conexion = Conection.conectar()
            client = ModelClient.getClient(conexion, user_document_id)

            if client is not None:
                if client.is_member_active():
                    # Lógica para abrir el portón
                    if abrir_porton():
                        success_message = f"Acceso Permitido. Bienvenido {client.Name}. Su membresía finaliza el {client.ExpirationMembership}."
                    else:
                        success_message = "Acceso Permitido, pero hubo un problema al abrir el portón."
                    
                    Conection().desconectar()  # Desconectar antes de retornar
                    return render_template("login/entryInstallationStatus.html", success_message=success_message)
                else:
                    error_message = "Acceso Denegado. Su membresía no se encuentra activa."
                    Conection().desconectar()  # Desconectar antes de retornar
                    return render_template("login/entryInstallationStatus.html", error=error_message)
            else:
                error_message = "Cliente no encontrado."
                return render_template("login/entryInstallationStatus.html", error=error_message)

        except Exception as e:
            print(e)
            error_message = "Hubo un error en el sistema. Inténtelo más tarde."
            return render_template("login/entryInstallationStatus.html", error=error_message)

        finally:
            if conexion:
                Conection().desconectar()
    return render_template("login/entryInstallation.html")

@login_app.route("/entryInstallationStatus")
def entryInstallationStatus():
    return render_template("login/entryInstallationStatus.html")

@login_app.route("/restartPassword")
def restartPassword():
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    return render_template("login/restartPassword.html", error = errorMessage, done = doneMessage)

@login_app.route("/sendEmail", methods = ['POST'])
def sendEmail():
    conection = Conection.conectar()
    documentId = request.form['documentId']
    if documentId:
        email = ModelUser.getEmail(conection, documentId)
        token = ModelUser.generateToken()
        exist = ModelUser.tokenExist(conection, documentId)

        if exist:
            save = ModelUser.saveToken(conection, documentId, token, action="update")
        else:
            save = ModelUser.saveToken(conection, documentId, token, action="save")
        
        if save:
            if email:
                if(manageEmail.sendEmail(documentId, email, token)):
                    return redirect( url_for("login_app.restartPassword", done="Correo enviado correctamente.") )
                else:
                    return redirect( url_for("login_app.restartPassword", error="No se pudo enviar el correo.") )
            else:
                return redirect( url_for("login_app.restartPassword", error="El usuario no esta registrado.") )
        else:
            return redirect( url_for("login_app.restartPassword", error="No se puedo enviar el correo.") )
    else:
        return redirect( url_for("login_app.restartPassword", error="Debe de ingresar el correo.") )

@login_app.route("/changePassword/<documentId>/<token>", methods=["GET","POST"])
def changePassword(documentId, token):
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == "POST":
        conection = Conection.conectar()
        data = ModelUser.getDataPasswords(request)
        Validator = ModelUser.changePassword(conection,documentId, token,data)
        if (Validator != "El cambio de contraseña fue exitosa"):
            return redirect(url_for("login_app.changePassword",documentId = documentId,token = token, error=Validator))
        
        else: return redirect(url_for("login_app.inicio", done = Validator))
    else:
        return render_template("login/changePassword.html",documentId = documentId, token = token,error = errorMessage, done = doneMessage)

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
