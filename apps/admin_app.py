#Importaciones
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.ModelTrainer import ModelTrainer
from db.models.ModelClient import ModelClient
from db.models.entities.User import User
from db.models.entities.Client import Client
from apps.permissions import admin_permission
import datetime

#Creación de los blueprint para usar en app.py
admin_app = Blueprint('admin_app', __name__)

#Routes redirectioned
@admin_app.errorhandler(403)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))

@admin_app.errorhandler(401)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))


@admin_app.route('/notAutorized')
def notAutorized():
    return "No tienes permisos para ingresar"


#Configuración de rutas y solicitudes
@admin_app.route("/")
@login_required
@admin_permission.require()
def inicio():
    print(current_user.role)
    return render_template("admin/index.html")

#-------------Rutas de Clientes-------------#
@admin_app.route("/clients")
@login_required
@admin_permission.require()
def clients():
    conexion = Conection.conectar()
    clients = ModelClient.get_all(conexion)
    Conection.desconectar()
    return render_template("admin/clients.html", clients=clients)

@admin_app.route("/insertClient", methods = ['POST'])
@login_required
def insertClient():
    client = ModelClient.validateDataForm(request)
    if type(client) != Client:
        return redirect(url_for('admin_app.clients', error = client))
    conection = Conection.conectar()
    if conection == None:
        return redirect(url_for('admin_app.clients', error = "Error en la conexion"))
    insert = ModelClient.insertClient(conection, client)
    if insert:
        print('Insertado conrrectamente')
        return redirect(url_for('admin_app.clients', done = "Cliente creado correctamente."))
    else:
        print('Algo paso')
        return redirect(url_for('admin_app.clients', error = "No se pudo ingresar el cliente."))

@admin_app.route("/clientes/actualizar/<documentId>", methods=['GET'])
@login_required
@admin_permission.require()
def viewUpdateClient(documentId):
    conexion = Conection.conectar()
    client = ModelClient.get_cliente_by_cedula(conexion, documentId)
    Conection.desconectar()
    if client:
        return render_template("admin/updateClient.html", client=client)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return "Cliente no encontrado"
    
@admin_app.route("/client/update/", methods=['POST'])
@login_required
@admin_permission.require()
def updateClient():
    client = ModelClient.validateDataForm(request)
    if type(client) != Client:
        return redirect(url_for('admin_app.clients', error = client))
    id = request.form['id']
    conection = Conection.conectar()
    if conection == None:
        return redirect(url_for('admin_app.clients', error = "Error en la conexion"))
    update = ModelClient.updateClient(conection, client, id)
    if update:
        print('Actualizado conrrectamente')
        return redirect(url_for('admin_app.clients', done = "Cliente actualizado correctamente."))
    else:
        print('Algo paso')
        return redirect(url_for('admin_app.clients', error = "No se pudo actualizar el cliente."))




@admin_app.route("/clientes/ver/<cedula>")
def verCliente(cedula):
    conexion = Conection.conectar()
    client = ModelClient.get_cliente_by_cedula(conexion, cedula)
    Conection.desconectar()

    if client:
        return render_template("admin/viewClient.html", client=client)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return "Cliente no encontrado"






@admin_app.route("/clientes/estadísticas")
@login_required
def estadisticas():
    return render_template("admin/estadisticas.html")

@admin_app.route("/cliente/estadistica/ver")
@login_required
def verEstadistica():
    return render_template("admin/verEstadistica.html")

@admin_app.route("/clientes/rutinas")
@login_required
def rutinasCliente():
    return render_template("admin/rutinaCliente.html")

@admin_app.route("/clientes/rutinas/sesiones")
@login_required
def sesionesCliente():
    return render_template("admin/verSesionesRutinaCliente.html")

@admin_app.route("/cliente/sesiones/ver")
@login_required
def verSesionCliente():
    return render_template("admin/verSesion.html")


    #-------------Rutas de Productos-------------#
@admin_app.route("/productos")
@login_required
def productos():
    return render_template("admin/inventario.html")

@admin_app.route("/productos/ver")
@login_required
def verProducto():
    return render_template("admin/verProducto.html")

@admin_app.route("/productos/actualizar")
@login_required
def actualizarProducto():
    return render_template("admin/actualizarProducto.html")




#-------------Rutas de Entrenadores-------------#
@admin_app.route("/entrenadores")
@login_required
def entrenadores():
    return render_template("admin/entrenadores.html")

@admin_app.route("/entrenadores/ver")
@login_required
def verEntrenador():
    return render_template("admin/verEntrenador.html")

@admin_app.route("/entrenadores/actualizar")
@login_required
def actualizarEntrenador():
    return render_template("admin/actualizarEntrenador")


#-------------Rutas de user-------------#
@admin_app.route("/users", methods = ['GET', 'POST'])
@login_required
@admin_permission.require()
def users():
    conection = Conection.conectar()
    users = ModelUser.get_Users(conection)
    clients = ModelUser.get_Clients(conection) 
    trainers = ModelUser.get_Trainers(conection) 
    Conection.desconectar()
    if request.method == 'POST':
        user = ModelUser.validateDataForm(request)
        if type(user) != User:
            return render_template("admin/users.html", users=users, clients=clients, trainers=trainers,  error=user)
        conection = Conection.conectar()
        if conection == None:
            return render_template("admin/users.html", users=users, clients=clients, trainers=trainers,  error= "Error en la conexión.")
        insert = ModelUser.insertUser(conection, user)
        if insert:
            users = ModelUser.get_Users(conection)
            Conection.desconectar()
            return render_template("admin/users.html", users=users,  clients=clients, trainers=trainers, done = "Cliente creado correctamente.")
        else:
            Conection.desconectar()
            return render_template("admin/users.html", users=users,  clients=clients, trainers=trainers, error= "No se pudo ingresar el cliente.")
    else:
        return render_template("admin/users.html", users=users, clients=clients, trainers=trainers)
    

@admin_app.route("/users/view/<DocumentId>")
def viewUser(DocumentId):
    try:
        conection = Conection.conectar()
        user = ModelUser.get_User(conection, DocumentId)  
    except Exception as e:
        print(f"Error al obtener el usuario: {e}")
        user = None
    finally:
        Conection().desconectar()

    return render_template("/admin/viewUser.html", user=user)

    
@admin_app.route("/usuarios/actualizar")
@login_required
def actualizarUsuario():
    return render_template("/admin/actualizarUsuario.html")



#-------------Rutas de facturas-------------#
@admin_app.route("/facturas")
@login_required
def facturas():
    return render_template("admin/factura.html")

@admin_app.route("/facturas/ver")
@login_required
def verFactura():
    return render_template("admin/verFactura.html")

@admin_app.route("/facturas/anular")
@login_required
def anular():
    return render_template("admin/anular.html")  


#-------------Rutas de Inventario-------------#
@admin_app.route("/inventario")
@login_required
def inventario():
    return render_template("admin/inventario.html")

#-------------Rutas de Notificaciones-------------#
@admin_app.route("/notificaciones")
@login_required
def notificaciones():
    return render_template("admin/notificaciones.html")

@admin_app.route("/notificaciones/ver")
@login_required
def verNotificacion():
    return render_template("admin/verNotificacion.html")



    #-------------Reportes------------#
@admin_app.route("/reportesFacturacion")
@login_required
def reportesFacturacion():
    return render_template("admin/reportesFacturacion.html")

@admin_app.route("/reportesInventario")
@login_required
def reportesInventario():
    return render_template("admin/reporteInventario.html")


    #-------------Perfil------------#
@admin_app.route("/perfil")
@login_required
def perfil():
    return render_template("admin/perfil.html")

#-------------Rutas de Membresias-------------#
@admin_app.route("/menbresias")
@login_required
def membresias():
    return render_template("admin/membresias.html")

@admin_app.route("/menbresias/ver")
@login_required
def verMembresia():
    return render_template("admin/verMembresia.html")

@admin_app.route("/menbresias/actualizar")
@login_required
def actualizarMembresia():
    return render_template("admin/actualizarMembresia.html")

