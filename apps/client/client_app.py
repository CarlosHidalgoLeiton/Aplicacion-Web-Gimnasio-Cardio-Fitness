#Importaciones
from flask import Blueprint, render_template, jsonify

#Creación de los blueprint para usar en app.py
client_app = Blueprint('client_app', __name__)

#Configuración de rutas y solicitudes
@client_app.route("/")
def inicio():
    return render_template("client/index.html")



#-------------Rutas de Rutinas-------------#
@client_app.route("/rutinas")
def rutina():
    return render_template("client/rutinaCliente.html")


@client_app.route("/rutinas/ver")
def verRutina():
    return render_template("client/verRutinaCliente.html")

#-------------Rutas de Productos-------------#

@client_app.route("/verProducto")
def producto():
    return render_template("/verProducto.html")