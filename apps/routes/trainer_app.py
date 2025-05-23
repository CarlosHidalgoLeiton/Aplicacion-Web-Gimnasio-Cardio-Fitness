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


trainer_app = Blueprint('trainer_app', __name__)

@trainer_app.route("/")
@login_required
@trainer_permission.require(http_exception=403)
def inicio():
    return render_template("trainer/index.html")

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

@trainer_app.route("/editarEstadistica" )
@login_required
def editarEstadistica():
    return render_template("trainer/editarEstadistica.html")

@trainer_app.route("/editarSesion" )
@login_required
def editarSesion():
    return render_template("trainer/editarSesion.html")

@trainer_app.route("/editarSesionesRutinaCliente" )
@login_required
def editarSesionesRutinaCliente():
    return render_template("trainer/editarSesionesRutinaCliente.html")


@trainer_app.route("/statisticsClient/<documentId>", methods=['GET', 'POST'])
@login_required
def statisticsClient(documentId):
    conection = Conection.conectar()

    # Obtener las estadísticas del cliente por su ID
    statistics = ModelStatistics.getStatisticsByClientId(conection, documentId)
    client = ModelStatistics.getClientById(conection, documentId)
    Conection.desconectar()
    if client is None:
        return redirect(url_for('trainer_app.clients', error="Cliente no encontrado"))
    
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')

    if request.method == 'POST':
        # Obtener y validar datos de estadísticas del formulario
        statistics_data = ModelStatistics.getDataStatistics(request)
        statisticsValidated = ModelStatistics.validateDataForm(statistics_data)

        if not isinstance(statisticsValidated, bool):
            return render_template("trainer/statisticsClient.html", statistics=statistics, error=statisticsValidated, statistics_data=statistics_data, documentId=documentId,client=client)

        conection = Conection.conectar()
        if conection is None:
            return render_template("trainer/statisticsClient.html", statistics=statistics, error="Error en la conexión.", statistics_data=statistics_data,client=client)

        # Intentar insertar las estadísticas
        statistics_data.Client_ID = documentId  # Asegurar que el Client_ID esté presente en los datos
        insert = ModelStatistics.insertStatistics(conection, statistics_data)

        if insert and isinstance(insert, bool):
            # Obtener las estadísticas nuevamente para actualizar la vista
            statistics = ModelStatistics.getStatisticsByClientId(conection, documentId)
            Conection.desconectar()
            return redirect(url_for("trainer_app.statisticsClient", documentId = documentId, done = "Estadística creada correctamente"))
        elif insert == "Primary":
            Conection.desconectar()
            return render_template("trainer/statisticsClient.html", statistics=statistics, error="El registro de estadísticas ya existe.", statistics_data=statistics_data,documentId=documentId,client=client)
        elif insert == "DataBase":
            return render_template("trainer/statisticsClient.html", statistics=statistics, error="No se puede conectar a la base de datos, por favor inténtalo más tarde o comuníquese con el desarrollador.", statistics_data=statistics_data,documentId=documentId,client=client)
        else:
            Conection.desconectar()
            return render_template("trainer/statisticsClient.html", statistics=statistics, error="No se pudo ingresar las estadísticas, por favor inténtalo más tarde.", statistics_data=statistics_data,documentId=documentId,client=client)
    else:
        return render_template("trainer/statisticsClient.html", client = client, statistics=statistics, statistics_data=None, done=doneMessage, error=errorMessage, documentId = documentId)





@trainer_app.route("/statisticsUpdate/<statisticsId>/<documentId>", methods=["POST", 'GET'])
@login_required
@trainer_permission.require(http_exception=403)
def updateStatistics(statisticsId,documentId):
    conection = Conection.conectar()
    statistics = ModelStatistics.getStatisticsId(conection, statisticsId)
    Conection.desconectar()
    if statistics:
        if request.method == 'POST':
            statistics_data = ModelStatistics.getDataStatisticsUpdate(request)
            statisticsValidated = ModelStatistics.validateDataFormUpdate(statistics_data)

            if not isinstance(statisticsValidated, bool):
                return render_template("trainer/updateStatistics.html", statistics=statistics, error=statisticsValidated, statistics_data=statistics_data, statisticsId=statisticsId,documentId=documentId)
            conection = Conection.conectar()
            if conection == None:
                return render_template("trainer/updateStatistics.html", statistics=statistics, error="Error en la conexión.", statistics_data=statistics_data)
            update_result = ModelStatistics.updateStatistics(conection, statistics_data,statisticsId)
            Conection.desconectar()
            if update_result is True:
                return redirect(url_for('trainer_app.statisticsClient', documentId=documentId, done="Estadística actualizada correctamente"))
            else:
                return render_template("/trainer/updateStatistics.html", statistics=statistics, error="No se pudo actualizar la estadística.", statistics_data=statistics_data,statisticsId = statisticsId,documentId=documentId)

        else:
            return render_template('trainer/updateStatistics.html', statistics = statistics,statisticsId = statisticsId,documentId=documentId)
    else:
        return redirect(url_for("trainer_app.statisticsClient", error = "Estadística no encontrado",documentId=documentId))




@trainer_app.route("/viewStatistics/<documentId>/<clientId>", methods = ['GET'])
@login_required
def viewStatistics(documentId,clientId):
    try:
        conection = Conection.conectar()
        statistics = ModelStatistics.getStatisticsId(conection, documentId)
        client = ModelStatistics.getClientById(conection, clientId)
        Conection.desconectar()
        if client is None:
            return redirect(url_for('trainer_app.statisticsClient', error="Cliente no encontrado"))
    

    except Exception as ex:
        print(f"Error al obtener las estadísticas del cliente: {ex}")
        statistics = None
    finally:
        Conection.desconectar()
    
    return render_template("trainer/viewStatistics.html", statistics=statistics, clientId = clientId,client=client)


## VER RUTINAS
@trainer_app.route("/client/routinesClient/<ID_Cliente>", methods=['GET'])
@login_required
@trainer_permission.require(http_exception=403)
def routinesClient(ID_Cliente):
    try:
        client = clientController.finOneByDocumentId(ID_Cliente)

        if not client:
            raise Exception('No se ha encontrado el cliente')

        routines = trainerController.getRoutineClient(ID_Cliente)

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

    # conexion = Conection.conectar()
    # routine = RoutineRepository.get_routine(conexion, routineId)
    # sessions = SessionRepository.get_session_by_Routine(conexion, routineId)
    # client = ModelClient.getClient(conexion, DocumentId)
    # Conection.desconectar()

    # if routine:
    #     return render_template("trainer/viewRoutine.html", routine=routine, sessions=sessions, client=client)
    # else:
    #     return redirect(url_for('trainer_app.clients', error="Rutina no encontrada"))

@trainer_app.route("/UpdateRoutine/<ID_Cliente>/<routineId>", methods=['GET', 'POST'])
@login_required
@trainer_permission.require(http_exception=403)
def UpdateRoutine(ID_Cliente, routineId):
    conection = Conection.conectar()
    client = ModelClient.getClient(conection, ID_Cliente)
    routine = RoutineRepository.get_routine(conection, routineId)
    Conection.desconectar()

    if request.method == 'POST':
        updated_routine = RoutineRepository.getDataRoutine(request)
        routineValidated = RoutineRepository.validateDataForm(updated_routine)

        if not isinstance(routineValidated, bool):
            return render_template("trainer/updateRoutineClient.html", client=client, error=routineValidated, routine=updated_routine)

        conection = Conection.conectar()
        if conection is None:
            return render_template("trainer/updateRoutineClient.html", client=client, error="Error en la conexión.", routine=updated_routine)

        try:
            conection.begin()

            # Actualizar la rutina principal
            trainer_id = request.form.get('TrainerId')
            indications = request.form.get('Indications')
            RoutineRepository.updateRoutine(conection, indications, routineId)

            # Procesar sesiones
            sessions_data = request.form.get('sessions')
            delete_ids_str = request.form.getlist('delete')  # Lista de IDs para eliminar

            delete_ids = []
            if delete_ids_str:
                # Convertir la cadena JSON en lista de IDs
                delete_ids = json.loads(delete_ids_str[0]) if delete_ids_str else []

            if delete_ids:
                SessionRepository.deleteSessions(conection, routineId, delete_ids)

            if sessions_data:
                sessions_data = json.loads(sessions_data)

                for session in sessions_data:
                    if session.get('insert', False):  
                        session['Routine_ID'] = routineId
                        session_result = SessionRepository.insertSession(conection, session)
                        if not session_result:
                            raise Exception(f"Error al insertar la sesión: {session['Name']}")
                    else:  # Sesión existente, se actualiza
                        session_result = SessionRepository.updateSession(conection, session,routineId )
                        if not session_result:
                            raise Exception(f"Error al actualizar la sesión: {session['Name']}")

            conection.commit()
            Conection.desconectar()

            return redirect(url_for('trainer_app.routinesClient', ID_Cliente=ID_Cliente, done="Rutina actualizada correctamente."))

        except Exception as e:
            conection.rollback()
            print(f"Error durante la actualización de la rutina y sesiones: {e}")
            Conection.desconectar()
            return render_template("trainer/updateRoutineClient.html", client=client, error="Error al actualizar la rutina o sesiones.", routine=updated_routine)

    return render_template("trainer/updateRoutineClient.html", routine=routine, client=client)


@trainer_app.route("/getSession/<ID_Routine>", methods=['GET'])
@login_required
@trainer_permission.require(http_exception=403)
def getSessions(ID_Routine):
    conection = Conection.conectar()
    getSessions = SessionRepository.get_session_by_Routine(conection, ID_Routine)
    Conection.desconectar()
    sessions = [session.to_dict() for session in getSessions]

    if sessions:
        return jsonify(sessions)
    else:
        return jsonify({'error': 'No se encontraron las sesiones.'})
    




@trainer_app.route("/client/routineClient/<ID_Cliente>", methods=['GET', 'POST'])
@login_required
def routineClient(ID_Cliente):
    try:
        client = clientController.getClientById(ID_Cliente)
        clear_local_storage = request.args.get('clear_local_storage')

        if request.method == 'POST':
            trainerController.createRoutine(request)

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
    data = request.get_json()
    DocumentId = data.get('routineID')
    conexion = Conection.conectar()
    disable = RoutineRepository.disableRoutine(conexion, DocumentId)
    Conection.desconectar()

    if disable:
        return jsonify({"message": "Hecho"})
    else:
        
        return jsonify({"error": "No se pudo deshabilitar"})
    
@trainer_app.route("/client/routineClient/able", methods = ['POST'])
@login_required
@trainer_permission.require(http_exception=403)
def ableRoutine():
    data = request.get_json()
    DocumentId = data.get('routineID')
    conection = Conection.conectar()
    able = RoutineRepository.ableRoutine(conection, DocumentId)
    Conection.desconectar()

    if able:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo habilitar"})











@trainer_app.route("/statisticsClient/disable", methods = ['POST'])
@login_required
@trainer_permission.require(http_exception=403)
def disableStatistics():
    data = request.get_json()
    DocumentId = data.get('statisticsID')
    conexion = Conection.conectar()
    disable = ModelStatistics.disableStatistics(conexion, DocumentId)
    Conection.desconectar()

    if disable:
        return jsonify({"message": "Hecho"})
    else:
        
        return jsonify({"error": "No se pudo deshabilitar"})
    
@trainer_app.route("/statisticsClient/able", methods = ['POST'])
@login_required
@trainer_permission.require(http_exception=403)
def ableStatistics():
    data = request.get_json()
    DocumentId = data.get('statisticsID')
    conection = Conection.conectar()
    able = ModelStatistics.ableStatistics(conection, DocumentId)
    Conection.desconectar()

    if able:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo habilitar"})


## Sesiones

@trainer_app.route("client/newSession/<ID_Cliente>", methods=['GET', 'POST'])
@login_required
def newSession(ID_Cliente):
    client = clientController.getClientById(ID_Cliente)
    return render_template("trainer/newSession.html", client=client)


@trainer_app.route("newSessionUpdate/<ID_Cliente>/<ID_Rutina>", methods=['GET', 'POST'])
@login_required
def newSessionUpdate(ID_Cliente, ID_Rutina):
    conection = Conection.conectar()
    client = ModelClient.getClient(conection, ID_Cliente) 
    routine = RoutineRepository.get_routine(conection, ID_Rutina) 
    Conection.desconectar()
    return render_template("trainer/newSessionUpdate.html", client=client, routine=routine)

@trainer_app.route("/viewClient/<documentId>")
@login_required
@trainer_permission.require(http_exception=403)
def viewClient(documentId):
    conexion = Conection.conectar()
    client = ModelClient.get_cliente_by_cedula(conexion, documentId)
    Conection.desconectar()
    if client:
        return render_template("trainer/viewClient.html", client=client)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return redirect(url_for('trainer_app.clients', error="Cliente no encontrado"))

@trainer_app.route("/verSesion" )
@login_required
def verSesion():
    return render_template("trainer/verSesion.html")

@trainer_app.route("/viewRoutine/viewSession/<Session_ID>", methods=['GET'])
@login_required
def viewSession(Session_ID):
    try:
        session = sessionController.findOneById(Session_ID)
        session.Exercises = json.loads(session.Exercises)

        return render_template("trainer/viewSession.html", session=session, routine=session.routine)

    except Exception as ex:
        flash(ex.args[0], 'danger')

    # conexion = Conection.conectar()
    # session = SessionRepository.get_sesssion_by_id(conexion, Session_ID)
    # routine = RoutineRepository.get_routine(conexion, session.Routine_ID)
    # Conection.desconectar()
    
    # if session:
    #     # Deserializa el JSON a un objeto Python
    #     session.Exercises = json.loads(session.Exercises)
    #     return render_template("trainer/viewSession.html", session=session, routine=routine)
    # else:
    #     return redirect(url_for('trainer_app.viewRoutine', routineId=routine.RoutineId, DocumentId=routine.ClientId, error="Sesión no encontrada"))


@trainer_app.route("/viewNewSession/<sessionId>/<clientId>", methods=['GET'])
@login_required
def viewSessionInsert(sessionId, clientId):
    if sessionId and clientId:
        return render_template('trainer/viewNewSession.html', sessionId = sessionId, clientId = clientId)
    else:
        return redirect(url_for('trainer_app.routineClient', error="Sesión no encontrada"))
    

@trainer_app.route("/viewUpdateSession/<sessionId>/<clientId>", methods=['GET'])
@login_required
def viewSessionUpdate(sessionId, clientId):
    routineId = request.args.get('routineId')
    if sessionId and clientId and routineId:
        return render_template('trainer/viewUpdateSession.html', sessionId = sessionId, clientId = clientId, routineId = routineId)
    else:
        return redirect(url_for('trainer_app.routineClient', error="Sesión no encontrada"))


