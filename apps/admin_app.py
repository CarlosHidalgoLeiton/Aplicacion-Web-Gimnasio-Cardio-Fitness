#Importaciones
from flask import Blueprint, render_template
from flask_login import login_required
from db.conection import Conection
from db.models.ModelClient import ModelCliente
from db.conection import Conection

#Creación de los blueprint para usar en app.py
admin_app = Blueprint('admin_app', __name__)


#Configuración de rutas y solicitudes
@admin_app.route("/")
@login_required
def inicio():
    return render_template("admin/index.html")

#-------------Rutas de Clientes-------------#
@admin_app.route("/clientes")
def clientes():
    conexion = Conection.conectar()
    clientes = ModelCliente.get_all(conexion)
    Conection.desconectar()
    return render_template("admin/clientes.html", clientes=clientes)


@admin_app.route("/clientes/ver/<cedula>")
def verCliente(cedula):
    conexion = Conection.conectar()
    cliente = ModelCliente.get_cliente_by_cedula(conexion, cedula)
    Conection.desconectar()

    if cliente:
        return render_template("admin/verCliente.html", cliente=cliente)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return "Cliente no encontrado"

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



    #-------------Rutas de Productos-------------#
@admin_app.route("/productos")
def productos():
    return render_template("admin/inventario.html")

@admin_app.route("/productos/ver")
def verProducto():
    return render_template("admin/verProducto.html")

@admin_app.route("/productos/actualizar")
def actualizarProducto():
    return render_template("admin/actualizarProducto.html")





#-------------Rutas de Entrenadores-------------#
@admin_app.route("/entrenadores")
def entrenadores():
    return render_template("admin/entrenadores.html")

@admin_app.route("/entrenadores/ver")
def verEntrenador():
    return render_template("admin/verEntrenador.html")

@admin_app.route("/entrenadores/actualizar")
def actualizarEntrenador():
    return render_template("admin/actualizarEntrenador")








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

@admin_app.route("/facturas/ver")
def verFactura():
    return render_template("admin/verFactura.html")

@admin_app.route("/facturas/anular")
def anular():
    return render_template("admin/anular.html")  


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


    #-------------Perfil------------#
@admin_app.route("/perfil")
def perfil():
    return render_template("admin/perfil.html")

#-------------Rutas de Membresias-------------#
@admin_app.route("/menbresias")
def membresias():
    return render_template("admin/membresias.html")

@admin_app.route("/menbresias/ver")
def verMembresia():
    return render_template("admin/verMembresia.html")

@admin_app.route("/menbresias/actualizar")
def actualizarMembresia():
    return render_template("admin/actualizarMembresia.html")

