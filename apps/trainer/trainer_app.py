from flask import Blueprint, render_template, jsonify

trainer_app = Blueprint('trainer_app', __name__)

@trainer_app.route("/")
def inicio():
    return render_template("trainer/index.html")

#-------------Rutas de Clientes-------------#
@trainer_app.route("/clientes" )
def clientes():
    return render_template("trainer/clientes.html")




#-------------Rutas de Rutinas-------------#
@trainer_app.route("/rutinas")
def rutinas():
    return render_template("trainer/rutinas.html")


#-------------Rutas de Rutinas-------------#
@trainer_app.route("/sesiones")
def sesiones():
    return render_template("trainer/rutinas.html")