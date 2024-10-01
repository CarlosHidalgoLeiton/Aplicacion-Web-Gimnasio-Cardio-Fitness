#Importaciones
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from apps.permissions import client_permission

#Creación de los blueprint para usar en app.py
client_app = Blueprint('client_app', __name__)

#Configuración de rutas y solicitudes
@client_app.route("/")
@login_required
@client_permission.require(http_exception=403)
def inicio():
    return render_template("client/index.html")


@client_app.errorhandler(403)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))

@client_app.errorhandler(401)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))


@client_app.route('/notAutorized')
def notAutorized():
    return "No tienes permisos para ingresar"

#-------------Rutas de inventario-------------#
@client_app.route("/inventario")
def inventario():
    return render_template("client/inventario.html")

@client_app.route("/verProducto")
def verProducto():
    return render_template("client/verProducto.html")
#-------------Rutas de rutinas-------------#
@client_app.route("/rutinaCliente")
def rutina():
    return render_template("client/rutinaCliente.html")


@client_app.route("/verRutina")
def verRutina():
    return render_template("client/verRutinaCliente.html")

@client_app.route("/verSesion")
def verSesion():
    return render_template("client/verSesionClient.html")

#-------------Rutas de estadisticas-------------#
@client_app.route("/estadisticas")
def estadisticas():
    return render_template("client/Estadisticas.html")

@client_app.route("/verEstadisticas")
def verEstadisticas():
    return render_template("client/verEstadistica.html")

#-------------Rutas de perfil-------------#
@client_app.route("/perfil")
def perfil():
    return render_template("client/perfil.html")