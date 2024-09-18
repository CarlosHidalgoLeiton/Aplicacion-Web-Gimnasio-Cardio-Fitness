#Importaciones
from flask import Blueprint, render_template, jsonify

#Creación de los blueprint para usar en app.py
admin_app = Blueprint('admin_app', __name__)


#Configuración de rutas y solicitudes
@admin_app.route("/")
def inicio():
    return render_template("admin/index.html")

#-------------Rutas de Clientes-------------#
@admin_app.route("/clientes")
def clientes():
    return render_template("admin/clientes.html")


@admin_app.route("/clientes/ver")
def verCliente():
    return render_template("admin/verCliente.html")

@admin_app.route("/clientes/ver/estadísticas")
def estadisticas():
    return render_template("admin/estadisticas.html")


#-------------Rutas de Entrenadores-------------#
@admin_app.route("/entrenadores")
def entrenadores():
    return render_template("admin/entrenadores.html")


#-------------Rutas de Usuarios-------------#
@admin_app.route("/usuarios")
def usuarios():
    return render_template("admin/usuarios.html")



#-------------Rutas de facturas-------------#
@admin_app.route("/facturas")
def facturas():
    return render_template("admin/factura.html")


#-------------Rutas de Inventario-------------#
@admin_app.route("/inventario")
def inventario():
    return render_template("admin/inventario.html")

#-------------Rutas de Notificaciones-------------#
@admin_app.route("/notificaciones")
def notificaciones():
    return render_template("admin/notificaciones.html")



