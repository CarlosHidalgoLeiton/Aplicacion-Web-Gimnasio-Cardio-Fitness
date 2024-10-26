from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from flask_login import login_user, logout_user, login_required, current_user
from db.conection import Conection
from db.models.ModelClient import ModelClient
from db.models.ModelTrainer import ModelTrainer
from db.models.ModelRoutine import ModelRoutine
from db.models.ModelStatistics import ModelStatistics
from db.models.ModelSesion import ModelSession
from apps.permissions import trainer_permission
import json  


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
        conexion = Conection.conectar()
        trainer = ModelTrainer.getTrainer(conexion, current_user.DocumentId)
        print(trainer)
    except Exception as ex:
        print(f"Error al obtener el perfil del entrenador: {ex}")
        trainer = None
    finally:
        Conection.desconectar()
    
    return render_template("trainer/profile.html", trainer=trainer)


#-------------Rutas de Clientes-------------#
@trainer_app.route("/clients", methods = ['GET'] )
@login_required
@trainer_permission.require(http_exception=403)
def clients():
    conexion = Conection.conectar()
    clients = ModelClient.get_all(conexion)
    errorMessage = request.args.get('error')
    Conection.desconectar()
    return render_template("trainer/clients.html", clients=clients, error = errorMessage)

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


## VER RUTINAS
@trainer_app.route("/client/routinesClient/<ID_Cliente>", methods=['GET', 'POST'])
@login_required
@trainer_permission.require(http_exception=403)
def routinesClient(ID_Cliente):
    conection = Conection.conectar()
    client = ModelClient.getClient(conection,ID_Cliente)
    routines = ModelRoutine.get_all(conection, ID_Cliente)  
    errorMessage = request.args.get('error')
    Conection.desconectar()
    return render_template("trainer/routinesClient.html", routines=routines, client=client, error=errorMessage)


@trainer_app.route("/viewRoutine/<routineId>/<DocumentId>", methods=['GET'])
@login_required
def viewRoutine(routineId, DocumentId):
    conexion = Conection.conectar()
    routine = ModelRoutine.get_routine(conexion, routineId)
    sessions = ModelSession.get_sesssion_by_Routine(conexion, routineId)
    client = ModelClient.getClient(conexion, DocumentId)
    Conection.desconectar()

    if routine:
        return render_template("trainer/viewRoutine.html", routine=routine, sessions=sessions, client=client)
    else:
        return redirect(url_for('trainer_app.clients', error="Rutina no encontrada"))


    
@trainer_app.route("/UpdateRoutine/<ID_Cliente>/<routineId>", methods=['GET', 'POST'])
@login_required
def UpdateRoutine(ID_Cliente, routineId):
    conection = Conection.conectar()
    client = ModelClient.getClient(conection, ID_Cliente)
    routine = ModelRoutine.get_routine(conection, routineId)
    sessions = ModelSession.get_sesssion_by_Routine(conection, routineId)

    Conection.desconectar()

    if request.method == 'POST':
        updated_routine = ModelRoutine.getDataRoutine(request)
        routineValidated = ModelRoutine.validateDataForm(updated_routine)

        if not isinstance(routineValidated, bool):
            return render_template("trainer/updateRoutineClient.html", client=client, error=routineValidated, routine=updated_routine, sessions=sessions)

        conection = Conection.conectar()
        if conection is None:
            return render_template("trainer/updateRoutineClient.html", client=client, error="Error en la conexión.", routine=updated_routine, sessions=sessions)

        try:
            conection.begin()
            success = ModelRoutine.updateRoutine(conection, routineId, updated_routine)
            if not success:
                raise Exception("Error al actualizar la rutina.")

            sessions_data = request.form.get('sessions')
            if sessions_data:
                ModelSession.deleteSessionsByRoutineID(conection, routineId)  # Borrar sesiones existentes
                sessions_data = json.loads(sessions_data)

                for session in sessions_data:
                    session['Routine_ID'] = routineId
                    session_result = ModelSession.insertSession(conection, session)
                    if session_result != True:
                        raise Exception(f"Error al insertar la sesión: {session['Name']}")

            conection.commit()
            Conection.desconectar()

            return redirect(url_for('trainer_app.routinesClient', ID_Cliente=ID_Cliente, done="Rutina actualizada correctamente."))

        except Exception as e:
            conection.rollback()
            print(f"Error durante la actualización de la rutina y sesiones: {e}")
            Conection.desconectar()
            return render_template("trainer/updateRoutineClient.html", client=client, error="Error al actualizar la rutina o sesiones.", routine=updated_routine, sessions=sessions)

    return render_template("trainer/updateRoutineClient.html", routine=routine, sessions=sessions, client=client)



@trainer_app.route("/client/routineClient/<ID_Cliente>", methods=['GET', 'POST'])
@login_required
def routineClient(ID_Cliente):
    conection = Conection.conectar()
    client = ModelClient.getClient(conection, ID_Cliente)  
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    clear_local_storage = request.args.get('clear_local_storage') 
    Conection.desconectar()

    if request.method == 'POST':
        routine = ModelRoutine.getDataRoutine(request)
        routineValidated = ModelRoutine.validateDataForm(routine)

        if not isinstance(routineValidated, bool):
            return render_template("trainer/routineClient.html", client=client, error=routineValidated, routine=routine)

        conection = Conection.conectar()
        if conection is None:
            return render_template("trainer/routineClient.html", client=client, error="Error en la conexión.", routine=routine)

        try:
            sessions = request.form.get('sessions')
            if sessions == '[]':
                return render_template("trainer/routineClient.html", client=client, error="Debe ingresar al menos una sesión.", routine=routine) 

            conection.begin()

            insert, success = ModelRoutine.insertRoutine(conection, routine)

            if not success:
                raise Exception("Error al insertar la rutina.")

            Routine_ID = insert.RoutineId  # Obtener el ID de la rutina creada
            
            sessions_data = json.loads(sessions)

            for session in sessions_data:
                session['Routine_ID'] = Routine_ID
                session_result = ModelSession.insertSession(conection, session)
                if session_result != True:
                    raise Exception(f"Error al insertar la sesión: {session['Name']}")

            conection.commit()
            Conection.desconectar()

            return redirect(url_for('trainer_app.routinesClient', ID_Cliente=ID_Cliente, done="Rutina creada correctamente.", clear_local_storage=True))

        except Exception as e:
            conection.rollback()
            print(f"Error durante la creación de la rutina y sesiones: {e}")
            if 'Routine_ID' in locals():
                ModelRoutine.deleteRoutine(conection, Routine_ID)
                print(f"Rutina {Routine_ID} eliminada debido a un fallo en las sesiones.")
            
            Conection.desconectar()
            return render_template("trainer/routineClient.html", client=client, error="Error al crear la rutina o sesiones.", routine=routine)

    else:
        return render_template("trainer/routineClient.html", routine=None, client=client, done=doneMessage, error=errorMessage, clear_local_storage=clear_local_storage)

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
    conection = Conection.conectar()
    client = ModelClient.getClient(conection, ID_Cliente)  
    Conection.desconectar()
    return render_template("trainer/newSession.html", client=client)


@trainer_app.route("newSessionUpdate/<ID_Cliente>/<ID_Rutina>", methods=['GET', 'POST'])
@login_required
def newSessionUpdate(ID_Cliente, ID_Rutina):
    conection = Conection.conectar()
    client = ModelClient.getClient(conection, ID_Cliente) 
    routine = ModelRoutine.get_routine(conection, ID_Rutina) 
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

@trainer_app.route("/verEstadistica" )
@login_required
def verEstadistica():
    return render_template("trainer/verEstadistica.html")

@trainer_app.route("/verSesion" )
@login_required
def verSesion():
    return render_template("trainer/verSesion.html")


@trainer_app.route("/viewRoutine/viewSession/<Session_ID>", methods=['GET'])
@login_required
def viewSession(Session_ID):
    conexion = Conection.conectar()
    session = ModelSession.get_sesssion_by_id(conexion, Session_ID)
    routine = ModelRoutine.get_routine(conexion, session.Routine_ID)
    Conection.desconectar()
    
    if session:
        # Deserializa el JSON a un objeto Python
        session.Exercises = json.loads(session.Exercises)
        return render_template("trainer/viewSession.html", session=session, routine=routine)
    else:
        return redirect(url_for('trainer_app.viewRoutine', routineId=routine.RoutineId, DocumentId=routine.ClientId, error="Sesión no encontrada"))

@trainer_app.route("/viewSession/<sessionId>/<clientId>", methods=['GET'])
@login_required
def viewSessionInsert(sessionId, clientId):
    if sessionId and clientId:
        return render_template('trainer/viewNewSession.html', sessionId = sessionId, clientId = clientId)
    else:
        return redirect(url_for('trainer_app.routineClient', error="Sesión no encontrada"))


