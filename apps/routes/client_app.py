#Importaciones
from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.routes.permissions import client_permission
from apps.db.conection import Conection
from apps.controllers.client_controller import clientController
from apps.controllers.session_controller import sessionController
from apps.controllers.routine_controller import routineController
from apps.controllers.statistics_controller import statisticsController
import json  
from apps.controllers.inventory_controller import productController

from apps.routes.chatbot import generate_bot_response 

#Creación de los blueprint para usar en app.py
client_app = Blueprint('client_app', __name__)

#Configuración de rutas y solicitudes
@client_app.route("/")
@login_required
@client_permission.require(http_exception=403)
#-------------Rutas de notificaciones-------------#
def inicio():
    try:
        notifications = clientController.getNotifications()
        return render_template("client/index.html" , notifications=notifications)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("client/index.html")
    
@client_app.errorhandler(403)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))

@client_app.errorhandler(401)
def forbidden(error):
    return redirect(url_for('client_app.notAutorized'))


@client_app.route("/get_bot", methods=["POST"])
@login_required
@client_permission.require(http_exception=403)
def get_bot_response():
    data = request.get_json()
    userText = data.get('msg')

    if userText:
        bot_response = generate_bot_response(userText)  # uso correcto

        options = [
            {"text": "Ver horarios", "value": "horarios"},
            {"text": "Ver precios", "value": "precios"},
            {"text": "Ver ubicación", "value": "ubicación"},
            {"text": "Ver contacto", "value": "contacto"}
        ]

        return jsonify({"response": bot_response, "options": options})

    return jsonify({"response": "Lo siento, no pude entender tu pregunta."})


@client_app.route('/notAutorized')
def notAutorized():
    return "No tienes permisos para ingresar"


    #-------------Rutas de Perfil -------------#
@client_app.route("/profile")
@login_required
@client_permission.require(http_exception=403)
def profile():
    try:
        client = clientController.finOneByDocumentId(current_user.DocumentId)

        return render_template("client/profile.html", client=client)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("client/profile.html", client = None)

#-------------Rutas de inventario-------------#
@client_app.route("/inventory", methods = ['GET', 'POST'])
@login_required
@client_permission.require(http_exception=403)
def inventory():
    try:
        products = productController.get_all()
        if request.method == 'POST':

            product = productController.getDataProduct(request, None)
            productValidated = productController.productValidated(product)
            if not type(productValidated) == bool:
                return render_template("client/inventory.html", products=products, error=productValidated, product = product)
            else:
                productController.create(product)
                products = productController.get_all()
                flash('Producto creado exitosamente', 'success')
                return render_template("client/inventory.html", products=products, product = None)
        else:
            return render_template("client/inventory.html", products=products, product = None )
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("client/inventory.html", products=products, product = None)

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

#------------- VER PRODUCTO -------------#
@client_app.route("/inventory/view", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def viewProduct():
    try:
        productId = session.get('IdProduct') 
        product = productController.getProductById(productId)
        return render_template("client/viewProduct.html", product=product)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('client_app.inventory'))
    
#-------------Rutas de rutinas-------------#

## VER RUTINAS
@client_app.route("/routinesClient", methods=['GET', 'POST'])
@login_required
@client_permission.require(http_exception=403)
def routinesClient():
    try:
        ID_Cliente = current_user.DocumentId
        client = clientController.finOneByDocumentId(ID_Cliente)

        routines = routineController.getRoutineClient(ID_Cliente)

        return render_template("client/routinesClient.html", routines=routines, client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('client_app.inicio'))

@client_app.route("/viewRoutine/<routineId>", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def viewRoutine(routineId):
    try:
        DocumentId = current_user.DocumentId
        client = clientController.finOneByDocumentId(DocumentId)
        routine = routineController.findOneRoutine(routineId)
        sessions = sessionController.findAllByIdRoutine(routineId)
        return render_template("client/viewRoutine.html", routine=routine, sessions=sessions, client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('client_app.routinesClient', ID_Cliente = DocumentId))

@client_app.route("/getSession/<ID_Routine>", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def getSessions(ID_Routine):
    try:
        sessions = sessionController.findAllByIdRoutine(ID_Routine)

        return jsonify(sessions)
    except:
        return jsonify({'error': 'No se encontraron las sesiones.'})
    
@client_app.route("/viewRoutine/viewSession/<Session_ID>", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def viewSession(Session_ID):
    try:
        ID_Routine = request.args.get("routine_id")

        session = sessionController.findOneById(Session_ID)
        session.Exercises = json.loads(session.Exercises)

        return render_template("client/viewSession.html", session=session, routine=session.routine)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('client_app.viewRoutine', ID_Routine = ID_Routine))


#-------------Rutas de estadisticas-------------#
@client_app.route("/statisticsClient", methods=['GET'])
@login_required
def statisticsClient():
    try:
        documentId = current_user.DocumentId
        client = clientController.finOneByDocumentId(documentId)
        statistics = statisticsController.getStatisticsByClientId(documentId)

        return render_template("client/statisticsClient.html", client = client, statistics=statistics, documentId = documentId)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('client_app.inicio'))
    
@client_app.route("/viewStatistics/<statisticsId>/<documentId>", methods = ['GET'])
@login_required
def viewStatistics(statisticsId, documentId):
    try:
        statistics = statisticsController.getStatisticById(statisticsId)
        client = clientController.finOneByDocumentId(documentId)

        return render_template("client/viewStatistics.html", statistics=statistics, clientId = documentId,client=client)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("client_app.statisticsClient", documentId=documentId))

@client_app.route("/viewMemberships", methods = ['GET'])
@login_required
def viewMemberships():
    errorMessage = request.args.get('error')

    conection = Conection.conectar()

    memberships = ModelMembership.get_allAble(conection)

    return render_template("client/membershipClient.html", memberships = memberships, error = errorMessage)

@client_app.route("/viewMemberships/<membershipId>", methods = ['GET'])
@login_required
def viewMembership(membershipId):

    conection = Conection.conectar()

    membership = ModelMembership.getMembership(conection, membershipId)

    if(membership):
        return render_template("client/viewMembership.html", membership = membership)
    else:
        return redirect(url_for("client_app.viewMemberships", error = "No se pudo encontrar la membresia."))