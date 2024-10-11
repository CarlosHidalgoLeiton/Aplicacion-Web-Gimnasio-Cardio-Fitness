#Importaciones
from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from flask_login import login_required, current_user
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.ModelTrainer import ModelTrainer
from db.models.ModelClient import ModelClient
from db.models.ModelMembership import ModelMembership
from db.models.entities.User import User
from apps.permissions import admin_permission

#Creación de los blueprint para usar en app.py
admin_app = Blueprint('admin_app', __name__)

#Routes redirectioned
@admin_app.errorhandler(403)
def forbidden(error):
    return redirect(url_for('admin_app.notAutorized'))

@admin_app.errorhandler(401)
def forbidden(error):
    return redirect(url_for('admin_app.notAutorized'))

@admin_app.route('/notAutorized')
def notAutorized():
    return "No tienes permisos para ingresar"

#Configuración de rutas y solicitudes
@admin_app.route("/")
@login_required
@admin_permission.require(http_exception=403)
def inicio():
    print(current_user.role)
    return render_template("admin/index.html")

#-------------Rutas de Clientes-------------#
@admin_app.route("/clients", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def clients():
    conection = Conection.conectar()
    clients = ModelClient.get_all(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        client = ModelClient.getDataClient(request)
        clientValidated = ModelClient.validateDataForm(client)
        if not type(clientValidated) == bool:
            return render_template("admin/clients.html", clients=clients, error=clientValidated, client = client)
        conection = Conection.conectar()
        if conection == None:
            return render_template("admin/clients.html", clients=clients, error= "Error en la conexión.", client = client)
        insert = ModelClient.insertClient(conection, client)
        if insert and type(insert) == bool:
            clients = ModelClient.get_all(conection)
            Conection.desconectar()
            return render_template("admin/clients.html", clients=clients, done = "Cliente creado correctamente.", client = None)
        elif insert == "Primary":
            Conection.desconectar()
            return render_template("admin/clients.html", clients=clients, error= "El número de cédula ingresado ya esta registrado con otro cliente.", client = client)
        elif insert == "DataBase":
            return render_template("admin/clients.html", clients=clients, error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", client = client)
        else:
            Conection.desconectar()
            return render_template("admin/clients.html", clients=clients, error= "No se pudo ingresar el cliente, por favor inténtalo más tarde.", client = client)
    else:
        return render_template("admin/clients.html", clients=clients, client = None, done = doneMessage, error = errorMessage)

    
@admin_app.route("/client/update/<documentId>", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def UpdateClient(documentId):
    conexion = Conection.conectar()
    client = ModelClient.get_cliente_by_cedula(conexion, documentId)
    Conection.desconectar()
    if client:
        if request.method == 'POST':
            clientupdated = ModelClient.getDataClient(request)
            clientValidated = ModelClient.validateDataForm(clientupdated)
            if not type(clientValidated) == bool:
                return render_template("admin/updateClient.html", error=clientValidated, client = client)
            conection = Conection.conectar()
            if conection == None:
                return render_template("admin/updateClient.html", error= "Error en la conexión.", client = client)
            update = ModelClient.updateClient(conection, clientupdated, client.DocumentId)
            Conection.desconectar()
            if update and type(update) == bool:
                return redirect(url_for('admin_app.clients', done = "Cliente actualizado correctamente."))
            elif update == "Primary":
                return render_template("admin/updateClient.html", error= "El número de cédula ingresado ya esta registrado con otro cliente.", client = client)
            elif update == "DataBase":
                return render_template("admin/updateClient.html", error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", client = client)
            else:
                return render_template("admin/updateClient.html", error= "No se pudo actualizar el cliente.", client = client)
        else:
            return render_template("admin/updateClient.html", client=client)
    else:
        return redirect(url_for("admin_app.clients", error = "Cliente no encontrado"))
    
@admin_app.route("/clientes/ver/<documentId>", methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewClient(documentId):
    conexion = Conection.conectar()
    client = ModelClient.get_cliente_by_cedula(conexion, documentId)
    Conection.desconectar()

    if client:
        return render_template("admin/viewClient.html", client=client)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return redirect(url_for('admin_app.clients', error="Cliente no encontrado"))

@admin_app.route("/clientes/deshabilitar", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableClient():
    data = request.get_json()
    clientId = data.get('clientId')
    conection = Conection.conectar()
    if conection == None:
        return redirect(url_for('admin_app.client', error = "No se pudo conectar con la base de datos"))
    disable = ModelClient.disableClient(conection, clientId)
    Conection.desconectar()

    if disable:
        return jsonify({"message": "Hecho"})
    else:
        # Manejar el caso en que no se encuentre el cliente
        return jsonify({"error": "No se pudo deshabilitar"})
    
@admin_app.route("/clientes/habilitar", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableClient():
    data = request.get_json()
    clientId = data.get('clientId')
    conection = Conection.conectar()
    if conection == None:
        return redirect(url_for('admin_app.client', error = "No se pudo conectar con la base de datos"))
    able = ModelClient.ableClient(conection, clientId)
    Conection.desconectar()

    if able:
        return jsonify({"message": "Hecho"})
    else:
        # Manejar el caso en que no se encuentre el cliente
        return jsonify({"error": "No se pudo habilitar"})




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
@admin_permission.require(http_exception=403)
def users():
    conection = Conection.conectar()
    users = ModelUser.get_Users(conection)
    clients = ModelUser.get_Clients(conection) 
    trainers = ModelUser.get_Trainers(conection) 
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
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
        return render_template("admin/users.html", users=users, clients=clients, trainers=trainers, done = doneMessage, errorMessage = errorMessage)
    

@admin_app.route("/users/view/<DocumentId>")
@login_required
@admin_permission.require(http_exception=403)
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

@admin_app.route("/users/update/<DocumentId>", methods=["POST", 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateUser(DocumentId):
    conection = Conection.conectar()
    user = ModelUser.get_UserU(conection, DocumentId)
    Conection.desconectar()
    if user:
        if request.method == 'POST':
            validatedUser = ModelUser.validateDataFormUpdate(request, user)
            if type(validatedUser) == str:  
                return render_template("/admin/updateUser.html", user=user, error=validatedUser)
            conection = Conection.conectar()
            if conection == None:
                return render_template("/admin/updateUser.html", user=user, error="Error en la conexión.")
            update_result = ModelUser.update_User(conection, validatedUser, user.id)
            Conection.desconectar()
            if update_result:
                return redirect(url_for('admin_app.users', done = "Usuario actualizado correctamente"))
            else:
                return render_template("/admin/updateUser.html", user=user, error="No se pudo actualizar el usuario.")
        else:
            return render_template('admin/updateUser.html', user = user)
    else:
        return redirect(url_for("admin_app.users", error = "Usuario no encontrado"))




@admin_app.route("/users/disable", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableUser():
    data = request.get_json()
    DocumentId = data.get('DocumentId')
    conexion = Conection.conectar()
    disable = ModelUser.disableUser(conexion, DocumentId)
    Conection.desconectar()

    if disable:
        return jsonify({"message": "Hecho"})
    else:
        
        return jsonify({"error": "No se pudo deshabilitar"})
    
@admin_app.route("/users/able", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableUser():
    data = request.get_json()
    DocumentId = data.get('DocumentId')
    conexion = Conection.conectar()
    able = ModelUser.ableUser(conexion, DocumentId)
    Conection.desconectar()

    if able:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo habilitar"})


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
@admin_app.route("/membresias", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def memberships():
    conection = Conection.conectar()
    memberships = ModelMembership.get_all(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        membership = ModelMembership.getDataClient(request)
        membershipValidated = ModelMembership.validateDataForm(membership)
        if not type(membershipValidated) == bool:
            return render_template("admin/membership.html", memberships=memberships, error=membershipValidated, membership = membership)
        conection = Conection.conectar()
        if conection == None:
            return render_template("admin/membership.html", memberships=memberships, error= "Error en la conexión.", membership = membership)
        insert = ModelMembership.insertMembership(conection, membership)
        if insert and type(insert) == bool:
            memberships = ModelMembership.get_all(conection)
            Conection.desconectar()
            return render_template("admin/membership.html", memberships=memberships, done = "Membresía creada correctamente.", membership = None)
        elif insert == "DataBase":
            return render_template("admin/membership.html", memberships=memberships, error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", membership = membership)
        else:
            Conection.desconectar()
            return render_template("admin/membership.html", memberships=memberships, error= "No se pudo ingresar la membresía, por favor inténtalo más tarde.", membership = membership)
    else:
        return render_template("admin/membership.html", memberships=memberships, membership = None, done = doneMessage, error = errorMessage)



@admin_app.route("/menbresias/ver")
@login_required
def viewMembership():
    return render_template("admin/verMembresia.html")

@admin_app.route("/menbresias/actualizar")
@login_required
def updateMembership():
    return render_template("admin/actualizarMembresia.html")

@admin_app.route("/membresias/deshabilitar", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableMembership():
    data = request.get_json()
    membershipId = data.get('membershipId')
    conection = Conection.conectar()
    if conection == None:
        return redirect(url_for('admin_app.memberships', error = "No se pudo conectar con la base de datos."))
    disable = ModelMembership.disableMembership(conection, membershipId)
    Conection.desconectar()

    if disable:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo deshabilitar"})
    
@admin_app.route("/membresias/habilitar", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableMembership():
    data = request.get_json()
    membershipId = data.get('membershipId')
    conection = Conection.conectar()
    if conection == None:
        return redirect(url_for('admin_app.memberships', error = "No se pudo conectar con la base de datos"))
    able = ModelMembership.ableMembership(conection, membershipId)
    Conection.desconectar()

    if able:
        return jsonify({"message": "Hecho"})
    else:
        # Manejar el caso en que no se encuentre el cliente
        return jsonify({"error": "No se pudo habilitar"})