#Importaciones
from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from apps.permissions import client_permission
from db.conection import Conection
from db.models.ModelClient import ModelClient
from db.models.ModelProduct import ModelProduct
#Creación de los blueprint para usar en app.py
client_app = Blueprint('client_app', __name__)

#Configuración de rutas y solicitudes
@client_app.route("/")
@login_required
@client_permission.require(http_exception=403)
#-------------Rutas de notificaciones-------------#
def inicio():
    conection = Conection.conectar()
    notifications = ModelClient.get_Notifications(conection)
    return render_template("client/index.html" , notifications=notifications)


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
@client_app.route("/inventory", methods = ['GET', 'POST'])
@login_required
@client_permission.require(http_exception=403)
def inventory():
    conection = Conection.conectar()
    products = ModelProduct.get_all(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    return render_template("client/inventory.html", products=products, product = None, done = doneMessage, error = errorMessage)

@client_app.route("/inventory/selectProduct/", methods=['POST', 'GET'])
@login_required
@client_permission.require(http_exception=403)
def select_Product():
    action = request.args.get('action')
    productId = request.args.get('IdProduct')  # Obtener el IdProduct desde los parámetros de la URL
    if not productId:
        return redirect(url_for('client_app.inventory', error="No product selected."))
    session['IdProduct'] = productId
    if action == 'view':
        return redirect(url_for('client_app.viewProduct'))
    else:
        return redirect(url_for('client_app.inventory', error="Invalid action."))

@client_app.route("/inventory/view", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def viewProduct():
    productId = session.get('IdProduct') 
    if not productId:
        return redirect(url_for('client_app.inventory', error="No product selected."))
    conexion = Conection.conectar()
    product = ModelProduct.get_product_by_id(conexion, productId)  # Asegurarse de que se usa productId
    Conection.desconectar()

    if product:
        return render_template("client/viewProduct.html", product=product)
    else:
        return redirect(url_for('client_app.inventory', error="Producto no encontrado"))
    
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

#-------------Rutas de notificaciones-------------#
