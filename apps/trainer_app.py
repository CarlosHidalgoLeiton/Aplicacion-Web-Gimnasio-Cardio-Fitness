from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from db.conection import Conection
from db.models.ModelClient import ModelClient
from db.models.ModelTrainer import ModelTrainer
from db.models.ModelStatistics import ModelStatistics
from apps.permissions import trainer_permission


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
        # print(trainer)
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


@trainer_app.route("/estadisticasCliente/<documentId>", methods=['GET', 'POST'])
@login_required
def estadisticasCliente(documentId):
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
            return render_template("trainer/estadisticasCliente.html", statistics=statistics, error=statisticsValidated, statistics_data=statistics_data, documentId=documentId,client=client)

        conection = Conection.conectar()
        if conection is None:
            return render_template("trainer/estadisticasCliente.html", statistics=statistics, error="Error en la conexión.", statistics_data=statistics_data,client=client)

        # Intentar insertar las estadísticas
        statistics_data.Client_ID = documentId  # Asegurar que el Client_ID esté presente en los datos
        insert = ModelStatistics.insertStatistics(conection, statistics_data)

        if insert and isinstance(insert, bool):
            # Obtener las estadísticas nuevamente para actualizar la vista
            statistics = ModelStatistics.getStatisticsByClientId(conection, documentId)
            Conection.desconectar()
            return render_template("trainer/estadisticasCliente.html", statistics=statistics, done="Estadísticas creadas correctamente.", statistics_data=None,documentId=documentId,client=client)
        elif insert == "Primary":
            Conection.desconectar()
            return render_template("trainer/estadisticasCliente.html", statistics=statistics, error="El registro de estadísticas ya existe.", statistics_data=statistics_data,documentId=documentId,client=client)
        elif insert == "DataBase":
            return render_template("trainer/estadisticasCliente.html", statistics=statistics, error="No se puede conectar a la base de datos, por favor inténtalo más tarde o comuníquese con el desarrollador.", statistics_data=statistics_data,documentId=documentId,client=client)
        else:
            Conection.desconectar()
            return render_template("trainer/estadisticasCliente.html", statistics=statistics, error="No se pudo ingresar las estadísticas, por favor inténtalo más tarde.", statistics_data=statistics_data,documentId=documentId,client=client)
    else:
        return render_template("trainer/estadisticasCliente.html", client = client, statistics=statistics, statistics_data=None, done=doneMessage, error=errorMessage, documentId = documentId)


@trainer_app.route("/nuevaRutina" )
@login_required
def nuevaRutina():
    return render_template("trainer/nuevaRutina.html")

@trainer_app.route("/rutinaCliente" )
@login_required
def rutinaCliente():
    return render_template("trainer/rutinaCliente.html")

@trainer_app.route("/rutinas" )
@login_required
def rutinas():
    return render_template("trainer/rutinas.html")

@trainer_app.route("/sesionesRutinaCliente" )
@login_required
def sesionesRutinaCliente():
    return render_template("trainer/sesionesRutinaCliente.html")

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

@trainer_app.route("/verSesionesRutinaCliente" )
@login_required
def verSesionesRutinaCliente():
    return render_template("trainer/verSesionesRutinaCliente.html")
