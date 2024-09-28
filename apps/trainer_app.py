from flask import Blueprint, render_template, jsonify
from flask_login import login_user, logout_user, login_required
from db.conection import Conection
from db.models.ModelClient import ModelCliente


trainer_app = Blueprint('trainer_app', __name__)

@trainer_app.route("/")
@login_required
def inicio():
    return render_template("trainer/index.html")

#-------------Rutas de Clientes-------------#
@trainer_app.route("/clientes" )
@login_required
def clientes():
    conexion = Conection.conectar()
    clientes = ModelCliente.get_all(conexion)
    Conection.desconectar()
    return render_template("trainer/clientes.html", clientes=clientes)

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

@trainer_app.route("/verCliente/<cedula>" )
@login_required
def verCliente(cedula):
    conexion = Conection.conectar()
    cliente = ModelCliente.get_cliente_by_cedula(conexion, cedula)
    Conection.desconectar()
    if cliente:
        return render_template("trainer/verCliente.html", cliente=cliente)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return "Cliente no encontrado"

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
