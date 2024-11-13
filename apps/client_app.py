#Importaciones
from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from flask_login import login_required, current_user
from apps.permissions import client_permission
from db.conection import Conection
from db.models.ModelClient import ModelClient
from db.models.ModelProduct import ModelProduct
from db.models.ModelSesion import ModelSession
from db.models.ModelRoutine import ModelRoutine
import json  
from apps.chatbot import get_response 


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

@client_app.route("/get_bot", methods=["POST"])
@login_required
@client_permission.require(http_exception=403)
def get_bot_response():
    """
    Ruta que recibe el mensaje del usuario y devuelve la respuesta del chatbot
    junto con las opciones a seguir.
    """
    data = request.get_json()  # Obtener los datos del cuerpo de la solicitud JSON
    userText = data.get('msg')  # Obtener el mensaje del usuario

    if userText:
        # Generar la respuesta del bot (basado en el texto del usuario)
        bot_response = get_response(userText)

        # Las opciones siempre serán las mismas, sin importar la entrada del usuario
        options = [
            {"text": "Ver horarios", "value": "horarios"},
            {"text": "Ver precios", "value": "precios"},
            {"text": "Ver ubicación", "value": "ubicación"},
            {"text": "Ver contacto", "value": "contacto"}
        ]

        return jsonify({"response": bot_response, "options": options})
    
    return jsonify({"response": "Lo siento, no pude entender tu pregunta."})

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
@client_app.route("/profile")
@login_required
@client_permission.require(http_exception=403)
def profile():
    try:
        conexion = Conection.conectar()
        client = ModelClient.getClient(conexion, current_user.DocumentId)
        print(client)
    except Exception as ex:
        print(f"Error al obtener el perfil del cliente: {ex}")
        client = None
    finally:
        Conection.desconectar()
    
    return render_template("client/profile.html", client=client)


#-------------Rutas de inventario-------------#
@client_app.route("/inventory", methods = ['GET', 'POST'])
@login_required
@client_permission.require(http_exception=403)
def inventory():
    conection = Conection.conectar()
    products = ModelProduct.get_allAble(conection)
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

## VER RUTINAS
@client_app.route("/routinesClient", methods=['GET', 'POST'])
@login_required
@client_permission.require(http_exception=403)
def routinesClient():
    conection = Conection.conectar()
    routines = ModelRoutine.get_all(conection, current_user.DocumentId)  
    errorMessage = request.args.get('error')
    Conection.desconectar()
    return render_template("client/routinesClient.html", routines=routines, error=errorMessage)

@client_app.route("/viewRoutine/<routineId>", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def viewRoutine(routineId):
    conexion = Conection.conectar()
    routine = ModelRoutine.get_routine(conexion, routineId)
    sessions = ModelSession.get_session_by_Routine(conexion, routineId)
    Conection.desconectar()

    if routine:
        return render_template("client/viewRoutine.html", routine=routine, sessions=sessions)
    else:
        return redirect(url_for('client_app.clients', error="Rutina no encontrada"))

@client_app.route("/getSession/<ID_Routine>", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def getSessions(ID_Routine):
    conection = Conection.conectar()
    getSessions = ModelSession.get_session_by_Routine(conection, ID_Routine)
    Conection.desconectar()
    sessions = [session.to_dict() for session in getSessions]

    if sessions:
        return jsonify(sessions)
    else:
        return jsonify({'error': 'No se encontraron las sesiones.'})
    

@client_app.route("/viewRoutine/viewSession/<Session_ID>", methods=['GET'])
@login_required
@client_permission.require(http_exception=403)
def viewSession(Session_ID):
    conexion = Conection.conectar()
    session = ModelSession.get_sesssion_by_id(conexion, Session_ID)
    routine = ModelRoutine.get_routine(conexion, session.Routine_ID)
    Conection.desconectar()
    
    if session:
        # Deserializa el JSON a un objeto Python
        session.Exercises = json.loads(session.Exercises)
        return render_template("client/viewSession.html", session=session, routine=routine)
    else:
        return redirect(url_for('client_app.viewRoutine', routineId=routine.RoutineId, DocumentId=routine.ClientId, error="Sesión no encontrada"))



#-------------Rutas de estadisticas-------------#
@client_app.route("/estadisticas")
def estadisticas():
    return render_template("client/Estadisticas.html")

@client_app.route("/verEstadisticas")
def verEstadisticas():
    return render_template("client/verEstadistica.html")

#-------------Rutas de notificaciones-------------#
