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

@admin_app.route("/clientes/estadísticas")
def estadisticas():
    return render_template("admin/estadisticas.html")

@admin_app.route("/cliente/estadistica/ver")
def verEstadistica():
    return render_template("admin/verEstadistica.html")

@admin_app.route("/clientes/actualizar")
def actualizarCliente():
    return render_template("admin/actualizarCliente.html")

@admin_app.route("/clientes/rutinas")
def rutinasCliente():
    return render_template("admin/rutinaCliente.html")

@admin_app.route("/clientes/rutinas/sesiones")
def sesionesCliente():
    return render_template("admin/verSesionesRutinaCliente.html")

@admin_app.route("/cliente/sesiones/ver")
def verSesionCliente():
    return render_template("admin/verSesion.html")







#-------------Rutas de Entrenadores-------------#
@admin_app.route("/entrenadores")
def entrenadores():
    return render_template("admin/entrenadores.html")










#-------------Rutas de Usuarios-------------#
@admin_app.route("/usuarios")
def usuarios():
    return render_template("admin/usuarios.html")

@admin_app.route("/usuarios/ver")
def verUsuario():
    return render_template("/admin/verUsuario.html")

@admin_app.route("/usuarios/actualizar")
def actualizarUsuario():
    return render_template("/admin/actualizarUsuario.html")




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

@admin_app.route("/notificaciones/ver")
def verNotificacion():
    return render_template("admin/verNotificacion.html")



    #-------------Reportes------------#
@admin_app.route("/reportesFacturacion")
def reportesFacturacion():
    return render_template("admin/reportesFacturacion.html")

@admin_app.route("/reportesInventario")
def reportesInventario():
    return render_template("admin/reporteInventario.html")
