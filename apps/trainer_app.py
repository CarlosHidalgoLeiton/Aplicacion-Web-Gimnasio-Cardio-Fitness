from flask import Blueprint, render_template, jsonify

trainer_app = Blueprint('trainer_app', __name__)

@trainer_app.route("/")
def inicio():
    return render_template("trainer/index.html")

#-------------Rutas de Clientes-------------#
@trainer_app.route("/clientes" )
def clientes():
    return render_template("trainer/clientes.html")

@trainer_app.route("/editarEstadistica" )
def editarEstadistica():
    return render_template("trainer/editarEstadistica.html")

@trainer_app.route("/editarSesion" )
def editarSesion():
    return render_template("trainer/editarSesion.html")

@trainer_app.route("/editarSesionesRutinaCliente" )
def editarSesionesRutinaCliente():
    return render_template("trainer/editarSesionesRutinaCliente.html")

@trainer_app.route("/estadisticasCliente" )
def estadisticasCliente():
    return render_template("trainer/estadisticasCliente.html")

@trainer_app.route("/nuevaRutina" )
def nuevaRutina():
    return render_template("trainer/nuevaRutina.html")

@trainer_app.route("/rutinaCliente" )
def rutinaCliente():
    return render_template("trainer/rutinaCliente.html")

@trainer_app.route("/rutinas" )
def rutinas():
    return render_template("trainer/rutinas.html")

@trainer_app.route("/sesionesRutinaCliente" )
def sesionesRutinaCliente():
    return render_template("trainer/sesionesRutinaCliente.html")

@trainer_app.route("/verCliente" )
def verCliente():
    return render_template("trainer/verCliente.html")

@trainer_app.route("/verEstadistica" )
def verEstadistica():
    return render_template("trainer/verEstadistica.html")

@trainer_app.route("/verSesion" )
def verSesion():
    return render_template("trainer/verSesion.html")

@trainer_app.route("/verSesionesRutinaCliente" )
def verSesionesRutinaCliente():
    return render_template("trainer/verSesionesRutinaCliente.html")
