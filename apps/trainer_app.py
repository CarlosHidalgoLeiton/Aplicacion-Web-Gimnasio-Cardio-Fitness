from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from db.conection import Conection
from db.models.ModelClient import ModelClient
from db.models.ModelTrainer import ModelTrainer
from apps.permissions import trainer_permission


trainer_app = Blueprint('trainer_app', __name__)

@trainer_app.route("/")
@login_required
@trainer_permission.require(http_exception=403)
def inicio():
    return render_template("trainer/index.html")

#-------------Rutas de Perfil -------------#
@trainer_app.route("/perfil")
@login_required
@trainer_permission.require(http_exception=403)
def perfil():
    try:
        conexion = Conection.conectar()
        trainer = ModelTrainer.getTrainer(conexion, current_user.DocumentId)
        print(trainer)
    except Exception as ex:
        print(f"Error al obtener el perfil del entrenador: {ex}")
        trainer = None
    finally:
        Conection.desconectar()
    
    return render_template("trainer/perfil.html", trainer=trainer)


#-------------Rutas de Clientes-------------#
@trainer_app.route("/clients", methods = ['GET'] )
@login_required
@trainer_permission.require(http_exception=403)
def clients():
    conexion = Conection.conectar()
    clients = ModelClient.get_all(conexion)
    errorMessage = request.args.get('error')
    Conection.desconectar()
    return render_template("trainer/clients.html", clients=clients, error = errorMessage)

@trainer_app.route("/editarEstadistica" )
@login_required
def editarEstadistica():
    return render_template("trainer/editarEstadistica.html")

@trainer_app.route("/editarSesion" )
@login_required
def editarSesion():
    return render_template("trainer/editarSesion.html")

@trainer_app.route("/editarSesionesRutinaCliente" )
@login_required
def editarSesionesRutinaCliente():
    return render_template("trainer/editarSesionesRutinaCliente.html")

@trainer_app.route("/estadisticasCliente" )
@login_required
def estadisticasCliente():
    return render_template("trainer/estadisticasCliente.html")

@trainer_app.route("/nuevaRutina" )
@login_required
def nuevaRutina():
    return render_template("trainer/nuevaRutina.html")

@trainer_app.route("/rutinaCliente" )
@login_required
def rutinaCliente():
    return render_template("trainer/rutinaCliente.html")

@trainer_app.route("/rutinas" )
@login_required
def rutinas():
    return render_template("trainer/rutinas.html")

@trainer_app.route("/sesionesRutinaCliente" )
@login_required
def sesionesRutinaCliente():
    return render_template("trainer/sesionesRutinaCliente.html")

@trainer_app.route("/viewClient/<documentId>")
@login_required
@trainer_permission.require(http_exception=403)
def viewClient(documentId):
    conexion = Conection.conectar()
    client = ModelClient.get_cliente_by_cedula(conexion, documentId)
    Conection.desconectar()
    if client:
        return render_template("trainer/viewClient.html", client=client)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return redirect(url_for('trainer_app.clients', error="Cliente no encontrado"))

@trainer_app.route("/verEstadistica" )
@login_required
def verEstadistica():
    return render_template("trainer/verEstadistica.html")

@trainer_app.route("/verSesion" )
@login_required
def verSesion():
    return render_template("trainer/verSesion.html")

@trainer_app.route("/verSesionesRutinaCliente" )
@login_required
def verSesionesRutinaCliente():
    return render_template("trainer/verSesionesRutinaCliente.html")
