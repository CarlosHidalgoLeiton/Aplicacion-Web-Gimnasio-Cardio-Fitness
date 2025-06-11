from flask import Blueprint, render_template, request, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, login_required, current_user
from apps.db.conection import Conection
from apps.db.repositories.RoutineRepository import RoutineRepository
from apps.db.repositories.SessionRepository import SessionRepository
from apps.routes.permissions import trainer_permission
import json  
from apps.controllers.client_controller import clientController
from apps.controllers.trainer_controller import trainerController
from apps.controllers.routine_controller import routineController
from apps.controllers.session_controller import sessionController
from apps.controllers.statistics_controller import statisticsController
from apps.utils.utils import getDataRoutine, validateDataRoutine, validateDataStatistics, getDataStatistics

trainer_app = Blueprint('trainer_app', __name__)

@trainer_app.route("/")
@login_required
@trainer_permission.require(http_exception=403)
def inicio():
    return redirect(url_for("trainer_app.clients"))

#-------------Rutas de Perfil -------------#
@trainer_app.route("/profile")
@login_required
@trainer_permission.require(http_exception=403)
def profile():
    try:
        trainer = trainerController.getTrainer(current_user.DocumentId)

        return render_template("trainer/profile.html", trainer=trainer)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("trainer/profile.html", trainer = None) 

#-------------Rutas de Clientes-------------#
@trainer_app.route("/clients", methods = ['GET'] )
@login_required
@trainer_permission.require(http_exception=403)
def clients():
    try:
        clients = clientController.get_all()

        return render_template("trainer/clients.html", clients=clients)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("trainer/clients.html", clients=[])

@trainer_app.route("/statisticsClient/<documentId>", methods=['GET', 'POST'])
@login_required
def statisticsClient(documentId):
    try:
        client = clientController.finOneByDocumentId(documentId)
        statistics = statisticsController.getStatisticsByClientId(documentId)

        if request.method == 'POST':
            statistics_data = getDataStatistics(request)
            statisticsValidated = validateDataStatistics(statistics_data)

            if not isinstance(statisticsValidated, bool):
                return render_template("trainer/statisticsClient.html", statistics=statistics, error=statisticsValidated, statistics_data=statistics_data, documentId=documentId,client=client)

            statisticsController.create(statistics_data)
            
            flash('Estadística creada correctamente', 'success')

            return redirect(url_for("trainer_app.statisticsClient", documentId = documentId))

        return render_template("trainer/statisticsClient.html", client = client, statistics=statistics, statistics_data=None, documentId = documentId)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.clients'))

@trainer_app.route("/statisticsUpdate/<statisticsId>/<documentId>", methods=["POST", 'GET'])
@login_required
@trainer_permission.require(http_exception=403)
def updateStatistics(statisticsId, documentId):
    try:
        statistics = statisticsController.getStatisticById(statisticsId)
        
        if request.method == 'POST':
            statistics_data = getDataStatistics(request)
            statisticsValidated = validateDataStatistics(statistics_data, True)

            if not isinstance(statisticsValidated, bool):
                flash(statisticsValidated, 'danger')
                return render_template("trainer/updateStatistics.html", statistics=statistics, statistics_data=statistics_data, statisticsId=statisticsId,documentId=documentId)

            updatedStatistics = statisticsController.update_statistics(statisticsId, statistics_data)
            
            flash('Estadística actualizada correctamente', 'success')

            return redirect(url_for("trainer_app.statisticsClient", documentId = documentId))

        return render_template('trainer/updateStatistics.html', statistics = statistics,statisticsId = statisticsId,documentId=documentId)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("trainer_app.statisticsClient", documentId=documentId))

@trainer_app.route("/viewStatistics/<statisticsId>/<documentId>", methods = ['GET'])
@login_required
def viewStatistics(statisticsId,documentId):
    try:
        statistics = statisticsController.getStatisticById(statisticsId)
        client = clientController.finOneByDocumentId(documentId)

        return render_template("trainer/viewStatistics.html", statistics=statistics, clientId = documentId,client=client)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("trainer_app.statisticsClient", documentId=documentId))

## VER RUTINAS
@trainer_app.route("/client/routinesClient/<ID_Cliente>", methods=['GET'])
@login_required
@trainer_permission.require(http_exception=403)
def routinesClient(ID_Cliente):
    try:
        client = clientController.finOneByDocumentId(ID_Cliente)

        routines = routineController.getRoutineClient(ID_Cliente)

        return render_template("trainer/routinesClient.html", routines=routines, client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.clients'))

@trainer_app.route("/viewRoutine/<routineId>/<DocumentId>", methods=['GET'])
@login_required
def viewRoutine(routineId, DocumentId):
    try:
        client = clientController.finOneByDocumentId(DocumentId)
        routine = routineController.findOneRoutine(routineId)
        sessions = sessionController.findAllByIdRoutine(routineId)
        return render_template("trainer/viewRoutine.html", routine=routine, sessions=sessions, client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.routinesClient', ID_Cliente = DocumentId))

@trainer_app.route("/UpdateRoutine/<ID_Cliente>/<routineId>", methods=['GET', 'POST'])
@login_required
@trainer_permission.require(http_exception=403)
def UpdateRoutine(ID_Cliente, routineId):
    try:
        client = clientController.finOneByDocumentId(ID_Cliente)
        routine = routineController.findOneRoutine(routineId)
        
        if request.method == 'POST':
            updated_routine =  getDataRoutine(request)
            routineValidated = validateDataRoutine(updated_routine)

            if not isinstance(routineValidated, bool):
                flash(routineValidated, 'danger')
                return render_template("trainer/updateRoutineClient.html", client=client, routine=updated_routine)
            
            routineController.updateRoutine(request, routineId)

            flash('Se ha actualizado la rutina correctamente', 'success')
            return redirect(url_for('trainer_app.routinesClient', ID_Cliente=ID_Cliente))
        
        return render_template("trainer/updateRoutineClient.html", routine=routine, client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.UpdateRoutine', ID_Cliente = ID_Cliente, routineId=routineId))


@trainer_app.route("/getSession/<ID_Routine>", methods=['GET'])
@login_required
@trainer_permission.require(http_exception=403)
def getSessions(ID_Routine):
    try:
        sessions = sessionController.findAllByIdRoutine(ID_Routine)

        return jsonify(sessions)
    except:
        return jsonify({'error': 'No se encontraron las sesiones.'})

@trainer_app.route("/client/routineClient/<ID_Cliente>", methods=['GET', 'POST'])
@login_required
def routineClient(ID_Cliente):
    try:
        client = clientController.getClientById(ID_Cliente)
        clear_local_storage = request.args.get('clear_local_storage')

        if request.method == 'POST':
            routineController.createRoutine(request)

            flash('Se ha creado la rutina correctamente', 'success')
            return redirect(url_for('trainer_app.routinesClient', ID_Cliente=ID_Cliente, clear_local_storage=True))

        return render_template("trainer/routineClient.html", routine=None, client=client, clear_local_storage=clear_local_storage)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.routineClient', ID_Cliente = ID_Cliente))


@trainer_app.route("/client/routineClient/disable", methods = ['POST'])
@login_required
@trainer_permission.require(http_exception=403)
def disableRoutine():
    try:
        routineController.disableRoutine(request)
        return jsonify({"message": "Hecho"})
    except Exception as ex:
        return jsonify({"error": "No se pudo deshabilitar"})
    
@trainer_app.route("/client/routineClient/able", methods = ['POST'])
@login_required
@trainer_permission.require(http_exception=403)
def ableRoutine():
    try:
        routineController.ableRoutine(request)
        return jsonify({"message": "Hecho"})
    except Exception as ex:
        return jsonify({"error": "No se pudo deshabilitar"})

@trainer_app.route("/statisticsClient/disable", methods = ['POST'])
@login_required
@trainer_permission.require(http_exception=403)
def disableStatistics():
    try:
        statisticsController.disableStatistic(request)
        return jsonify({"message": "Hecho"})
    except Exception as ex:
        return jsonify({"error": "No se pudo deshabilitar"})
    
@trainer_app.route("/statisticsClient/able", methods = ['POST'])
@login_required
@trainer_permission.require(http_exception=403)
def ableStatistics():
    try:
        statisticsController.ableStatistic(request)
        return jsonify({"message": "Hecho"})
    except Exception as ex:
        return jsonify({"error": "No se pudo deshabilitar"})
        
## Sesiones
@trainer_app.route("client/newSession/<ID_Cliente>", methods=['GET', 'POST'])
@login_required
def newSession(ID_Cliente):
    try:
        client = clientController.getClientById(ID_Cliente)
        return render_template("trainer/newSession.html", client=client)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.routineClient', ID_Cliente = ID_Cliente))

@trainer_app.route("newSessionUpdate/<ID_Cliente>/<ID_Rutina>", methods=['GET', 'POST'])
@login_required
def newSessionUpdate(ID_Cliente, ID_Rutina):
    try:
        client = clientController.getClientById(ID_Cliente)
        routine = routineController.findOneRoutine(ID_Rutina)
        return render_template("trainer/newSessionUpdate.html", client=client, routine=routine)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.UpdateRoutine', ID_Cliente = ID_Cliente, routineId = ID_Rutina))

@trainer_app.route("/viewUpdateSession/<sessionId>/<clientId>", methods=['GET'])
@login_required
def viewSessionUpdate(sessionId, clientId):
    routineId = request.args.get('routineId')
    if sessionId and clientId and routineId:
        return render_template('trainer/viewUpdateSession.html', sessionId = sessionId, clientId = clientId, routineId = routineId)
    else:
        flash(ex.args[0], 'No se encontró la sesión')
        return redirect(url_for('trainer_app.routineClient'))

@trainer_app.route("/viewClient/<documentId>")
@login_required
@trainer_permission.require(http_exception=403)
def viewClient(documentId):
    try:
        client = clientController.getClientById(documentId)
        return render_template("trainer/viewClient.html", client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('trainer_app.clients'))
    
@trainer_app.route("/viewRoutine/viewSession/<Session_ID>", methods=['GET'])
@login_required
def viewSession(Session_ID):
    try:
        session = sessionController.findOneById(Session_ID)
        session.Exercises = json.loads(session.Exercises)

        return render_template("trainer/viewSession.html", session=session, routine=session.routine)

    except Exception as ex:
        flash(ex.args[0], 'danger')

@trainer_app.route("/viewNewSession/<sessionId>/<clientId>", methods=['GET'])
@login_required
def viewSessionInsert(sessionId, clientId):
    if sessionId and clientId:
        return render_template('trainer/viewNewSession.html', sessionId = sessionId, clientId = clientId)
    else:
        return redirect(url_for('trainer_app.routineClient', error="Sesión no encontrada"))