#Importaciones
from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_login import login_required, current_user
from apps.permissions import client_permission
from db.conection import Conection
from db.models.ModelClient import ModelClient
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


    #-------------Rutas de Perfil -------------#
@client_app.route("/perfil")
@login_required
@client_permission.require(http_exception=403)
def perfil():
    try:
        conexion = Conection.conectar()
        client = ModelClient.get_cliente_by_cedula(conexion, current_user.DocumentId)
        print(client)
    except Exception as ex:
        print(f"Error al obtener el perfil del cliente: {ex}")
        client = None
    finally:
        Conection.desconectar()
    
    return render_template("client/perfil.html", client=client)


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

