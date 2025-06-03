# Importaciones
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, Response, flash
from flask_login import login_required, current_user
from apps.db.conection import Conection
from apps.db.repositories.UserRepository import UserRepository
from apps.db.repositories.ClientRepository import ClientRepository
from apps.db.repositories.ProductRepository import ProductRepository
from apps.db.repositories.RoutineRepository import RoutineRepository
from apps.db.repositories.SessionRepository import SessionRepository


from apps.db.models.User import User
from apps.routes.permissions import admin_permission
import json  
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file
from apps.controllers.client_controller import clientController
from apps.controllers.trainer_controller import trainerController
from apps.controllers.statistics_controller import statisticsController
from apps.controllers.inventory_controller import productController
from apps.controllers.notification_controller import notificationController
from apps.controllers.bill_controller import billController
from apps.controllers.membership_controller import membershipController
from apps.controllers.cancelledBill_controller import cancelledBillController
from apps.controllers.routine_controller import routineController
from apps.controllers.session_controller import sessionController



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
    return render_template("admin/index.html")

#-------------Rutas de Clientes-------------#
@admin_app.route("/clients", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def clients():
    try:
        clients = clientController.get_all()
        if request.method == 'POST':
            client = clientController.getDataClient(request)
            clientValidated = clientController.clientValidated(client)
            if not type(clientValidated) == bool:
                return render_template("admin/clients.html", clients=clients, error=clientValidated, client = client)
            else:
                clientController.create(client)
                clients = clientController.get_all()
                flash('Registro creado exitosamente', 'success')
                return render_template("admin/clients.html", clients=clients, client = None)
        else:
            return render_template("admin/clients.html", clients=clients, client = None )
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("admin/clients.html", clients=clients, client = None)
    
@admin_app.route("/client/update/<documentId>", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def UpdateClient(documentId):

    try:
        client = clientController.get_one(documentId)
        if request.method == 'POST':
            clientupdated = clientController.getDataClient(request)
            clientValidated = clientController.clientValidatedUpdate(client.DocumentId,clientupdated)
            if not type(clientValidated) == bool:
                return render_template("admin/updateClient.html", error=clientValidated, client = client)
            clientController.updateClient(client.DocumentId,clientupdated)
            flash('Registro actualizado exitosamente', 'success')
            return redirect(url_for('admin_app.clients'))
        else:
                return render_template("admin/updateClient.html", client=client)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("admin_app.clients"))
 

    
@admin_app.route("/clientes/ver/<documentId>", methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewClient(documentId):
    try:
        client = clientController.getClientById(documentId)
        return render_template("admin/viewClient.html", client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.clients'))

@admin_app.route("/clientes/deshabilitar", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableClient():
    try:
        data = request.get_json()
        clientId = data.get('clientId')
    
        disable = clientController.disable_client(clientId)

        if disable:
            return jsonify({"message": "Hecho"})
        else:
            # Manejar el caso en que no se encuentre el cliente
            return jsonify({"error": "No se pudo deshabilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.clients'))
    
@admin_app.route("/clientes/habilitar", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableClient():
    try:
        data = request.get_json()
        clientId = data.get('clientId')
        able = clientController.able_Client(clientId)
        if able:
            return jsonify({"message": "Hecho"})
        else:
            # Manejar el caso en que no se encuentre el cliente
            return jsonify({"error": "No se pudo habilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.clients'))


@admin_app.route("/client/statisticsClient/<documentId>", methods=['GET'])
@login_required
def statisticsClient(documentId):
    conection = Conection.conectar()

    # Obtener las estadísticas del cliente por su ID
    #statistics = ModelStatistics.getStatisticsByClientId(conection, documentId)
    #client = ModelStatistics.getClientById(conection, documentId)

    statistics = statisticsController.getStatisticsByClientId(documentId)
    #client = clientController.getClientById(documentId)
    # if client is None:
    #     return redirect(url_for('admin_app.clients', error="Cliente no encontrado"))
    
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    
    return render_template("admin/statistics.html", statistics=statistics, done=doneMessage, error=errorMessage, documentId = documentId)


@admin_app.route("/viewStatistics/<documentId>/<clientId>", methods = ['GET'])
@login_required
def viewStatistics(documentId,clientId):
    try:
        statistics = statisticsController.getStatisticById(documentId)
        return render_template("admin/viewStatistics.html", statistics=statistics)
    
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("admin/viewStatistics.html", statistics = None)


## VER RUTINAS
@admin_app.route("/clients/routinesClient/<ID_Cliente>", methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def routinesClient(ID_Cliente):
    try:
            client = clientController.finOneByDocumentId(ID_Cliente)

            routines = routineController.getRoutineClient(ID_Cliente)

            return render_template("admin/routinesClient.html", routines=routines, client=client)

    except Exception as ex:
            flash(ex.args[0], 'danger')
            return redirect(url_for('admin_app.clients'))



@admin_app.route("/viewRoutine/<routineId>/<DocumentId>", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewRoutine(routineId, DocumentId):
    try:
        client = clientController.finOneByDocumentId(DocumentId)
        routine = routineController.findOneRoutine(routineId)
        sessions = sessionController.findAllByIdRoutine(routineId)
        return render_template("admin/viewRoutine.html", routine=routine, sessions=sessions, client=client)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.routinesClient', ID_Cliente = DocumentId))

@admin_app.route("/getSession/<ID_Routine>", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def getSessions(ID_Routine):
    try:
        sessions = sessionController.findAllByIdRoutine(ID_Routine)

        return jsonify(sessions)
    except:
        return jsonify({'error': 'No se encontraron las sesiones.'})
    

@admin_app.route("/viewRoutine/viewSession/<Session_ID>", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewSession(Session_ID):
    try:
        session = sessionController.findOneById(Session_ID)
        session.Exercises = json.loads(session.Exercises)

        return render_template("admin/viewSession.html", session=session, routine=session.routine)

    except Exception as ex:
        flash(ex.args[0], 'danger')

#-------------Rutas de Entrenadores-------------#

#Aquí he cambiadooo
@admin_app.route("/trainers", methods = ['POST', 'GET'])
@login_required
def trainers():
    try:
        trainers = trainerController.get_all()
        if request.method == 'POST':
            trainer = trainerController.getData(request)
            trainerValidated = trainerController.validateDataForm(trainer)
            if not type(trainerValidated) == bool:
                return render_template("admin/trainers.html", trainers=trainers, error=trainerValidated, trainer = trainer)
            trainerController.create(trainer)
            trainers = trainerController.get_all()
            flash('Registro creado exitosamente', 'success')
            return render_template("admin/trainers.html", trainers=trainers, trainer = None)
        else:
            return render_template("admin/trainers.html", trainers=trainers, trainer = None)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("admin/trainers.html", trainers=trainers, trainer = None)
 

@admin_app.route("/trainer/update/<documentId>", methods = ['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateTrainer(documentId):

    try:
        trainer = trainerController.get_one(documentId)

        if request.method == 'POST':
            trainerUpdated = trainerController.getData(request)
            trainerValidated = trainerController.TrainertValidatedUpdate(trainer.DocumentId,trainerUpdated)

            if not type(trainerValidated) == bool:
                return render_template("admin/updateTrainer.html", error=trainerValidated, trainer = trainer)
                
            trainerController.updateTrainer(trainer.DocumentId,trainerUpdated)
            flash('Registro actualizado exitosamente', 'success')
            return redirect(url_for('admin_app.trainers'))
                
        return render_template("admin/updateTrainer.html", trainer = trainer)
    
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("admin_app.trainers"))
 


@admin_app.route("/trainers/view/<documentId>", methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewTrainer(documentId):
    try:
        trainer = trainerController.get_one(documentId)
        return render_template("admin/viewTrainer.html", trainer=trainer)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.trainers'))
    

@admin_app.route("/trainer/disable", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableTrainer():
    try:
        data = request.get_json()
        DocumentId = data.get('clientID')

        disable = trainerController.disable_trainer(DocumentId)

        if disable:
            return jsonify({"message": "Hecho"})
        else:
            
            return jsonify({"error": "No se pudo deshabilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.trainers'))

    
@admin_app.route("/trainer/able", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableTrainer():
    try:
        data = request.get_json()
        DocumentId = data.get('clientID')
        able = trainerController.able_trainer(DocumentId)

        if able:
            return jsonify({"message": "Hecho"})
        else:
            return jsonify({"error": "No se pudo habilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.trainers'))
    

#-------------Rutas de user-------------#
@admin_app.route("/users", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def users():
    conection = Conection.conectar()
    users = UserRepository.get_Users(conection)
    clients = UserRepository.get_Clients(conection) 
    trainers = UserRepository.get_Trainers(conection) 
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        user = UserRepository.validateDataForm(request)
        if type(user) != User:
            return render_template("admin/users.html", users=users, clients=clients, trainers=trainers,  error=user)
        conection = Conection.conectar()
        if conection == None:
            return render_template("admin/users.html", users=users, clients=clients, trainers=trainers,  error= "Error en la conexión.")
        insert = UserRepository.insertUser(conection, user)
        if insert:
            users = UserRepository.get_Users(conection)
            Conection.desconectar()
            return redirect(url_for("admin_app.users", done = "Usuario creado correctamente."))
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
        user = UserRepository.get_User(conection, DocumentId)  
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
    user = UserRepository.get_UserU(conection, DocumentId)
    Conection.desconectar()
    if user:
        if request.method == 'POST':
            validatedUser = UserRepository.validateDataFormUpdate(request, user)
            if type(validatedUser) == str:  
                return render_template("/admin/updateUser.html", user=user, error=validatedUser)
            conection = Conection.conectar()
            if conection == None:
                return render_template("/admin/updateUser.html", user=user, error="Error en la conexión.")
            update_result = UserRepository.update_User(conection, validatedUser, user.id)
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
    disable = UserRepository.disableUser(conexion, DocumentId)
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
    conection = Conection.conectar()
    able = UserRepository.ableUser(conection, DocumentId)
    Conection.desconectar()

    if able:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo habilitar"})


#-------------Rutas de facturas-------------#
@admin_app.route("/bills", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def bills():
    try:
        bills = billController.get_allAble()
        clients = clientController.get_allAble()
        trainers = trainerController.get_allAble()
        memberships = membershipController.get_allAble()
        products = productController.get_allAble()

        if request.method == 'POST':
            if request.form['typeEntity'] == 'Trainer':
                bill = billController.getDataTrainerBill(request)
                validatedBill = billController.validateDataFormTrainer(bill)
                if not type(validatedBill) == bool:
                    flash(validatedBill, 'danger')
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, trainerValidated = bill, generalValidated = None, productValidated = None, membershipValidated = None  ) 
                
                billController.create( bill)
                bills = billController.get_all()
                flash('Registro creado exitosamente', 'success')
                return redirect(url_for("admin_app.bills"))
            
            elif request.form['typeEntity'] == 'General':
                bill = billController.getDataGeneralBill(request)
                validatedBill = billController.validateDataFormGeneral(bill)
                if not type(validatedBill) == bool:
                    flash(validatedBill, 'danger')
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, generalValidated = bill, trainerValidated = None,productValidated = None, membershipValidated = None ) 

                insert = billController.create(bill)
                bills = billController.get_all()
                flash('Registro creado exitosamente', 'success')
                return redirect(url_for("admin_app.bills"))

        
            if request.form['typeEntity'] == 'Product':
                bill = billController.getDataProductBill(request)
                validatedBill = billController.validateDataFormProduct(bill)
                if not type(validatedBill) == bool:
                    flash(validatedBill, 'danger')
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None  ) 

                stock = productController.get_stock(bill.ID_Entity)

                if not stock:
                    flash('No se pudo realizar el pago.', 'danger')
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None ) 

                lotEnough = billController.validateStock(stock ,bill.Lot)
                if lotEnough:
                    bill.Lot = stock - int(bill.Lot)
                    billController.create(bill)
                    flash('Registro creado exitosamente', 'success')
                    return redirect(url_for('admin_app.bills'))
                else:
                    flash('La cantidad ingresada excede la cantidad en el stock.', 'danger')
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None ) 

            if request.form['typeEntity'] == 'Membership':
                bill = billController.getDataMembershipBill(request)
                validatedBill = billController.validateDataFormMembership(bill)
                if not type(validatedBill) == bool:
                    flash(validatedBill, 'danger')
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, membershipValidated = bill, generalValidated = None, trainerValidated = None, productValidated = None) 

                billController.create(bill)

                if request.form['typeEntity']=='Membership':
                        # Obtener los datos del cliente y membresía
                    days = billController.getDataMembership(request)

                    # days = billController.getDataMembershipDay(idMembership)

                    client = billController.getDataMembershipClient(request,days)

                    # Validar los datos obtenidos del formulario
                    validation_result = billController.validateDataFormMembershipClient(client)
                
                    if validation_result == True:
                        # Intentar actualizar la membresía del cliente
                        billController.updateClientMembership(client)
                        flash('Registro creado exitosamente', 'success')
                        return redirect(url_for('admin_app.bills'))
                    else:
                        flash(validation_result, 'danger')
                        return render_template("admin/bill.html", bills=bills, clients=clients, memberships=memberships, membershipValidated=bill, generalValidated=None, trainerValidated=None, productValidated=None)
        else:
            return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, trainerValidated = None, generalValidated = None, productValidated = None, membershipValidated = None)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.bills'))
    

@admin_app.route("/bills/view/<ID_Bill>")
@login_required
@admin_permission.require(http_exception=403)
def viewBill(ID_Bill):
    try:
        bill = billController.get_one(ID_Bill)  
        return render_template("/admin/viewBill.html", bill=bill)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.bills'))



@admin_app.route("/bills/cancel/<ID_Bill>", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def cancelBill(ID_Bill):
    try:
        if request.method == 'POST':
            cancelBill = cancelledBillController.getDataCanceledBill(request)
            validatedCancel = cancelledBillController.validateDataForm(cancelBill)

            if not type(validatedCancel) == bool:
                flash('Registro creado exitosamente', 'success')
                return render_template('admin/cancelBill.html', error = validatedCancel, cancelBill = cancelBill, ID_Bill = ID_Bill)
            
            cancelledBillController.create(cancelBill)
            billController.disable_bill(ID_Bill)
            flash('Registro creado exitosamente', 'success')
            return redirect(url_for('admin_app.bills'))

        return render_template("admin/cancelBill.html", ID_Bill = ID_Bill, cancelBill = None)
      
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.bills'))
    
@admin_app.route("/bills/viewCancelBill/<ID_Bill>", methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewcancelBill(ID_Bill):
    
    if ID_Bill != None:
        bill = billController.get_one(ID_Bill)
        cancelBill = cancelledBillController.getCancelBill(ID_Bill)
        if not bill or not cancelBill:
            return redirect(url_for('admin_app.bills', error = "No se pudo obtener la información de la factura anulada."))

        if bill.EntityType == 'Entrenador':
            trainer = trainerController.getTrainerBill( bill.ID_Entity)
            
            return render_template('admin/viewCancel.html', trainer = trainer, ID_Bill = ID_Bill, bill = bill, cancelBill = cancelBill)
                
        elif bill.EntityType == 'Cliente': 
            client = ClientRepository.getClientBill( bill.ID_Entity)
            
            return render_template('admin/viewCancel.html', client = client, ID_Bill = ID_Bill, bill = bill, cancelBill = cancelBill)
        
        else:
            return render_template('admin/viewCancel.html', ID_Bill = ID_Bill, bill = bill, cancelBill = cancelBill)

    
    return redirect(url_for('admin_app.bills', error = "No se pudo obtener la información de la factura anulada."))


@admin_app.route('/getClients', methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def getClientsPay():
    conection = Conection.conectar()
    clients = ClientRepository.get_all(conection)
    Conection.desconectar()

    if clients != None:
        return jsonify({'message': 'Hecho','clients': clients})
    else:
        return jsonify({'error': 'No se pudieron cargar los clientes.'})



#-------------Rutas de Inventario - Producto -------------#
@admin_app.route("/inventory", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def inventory():
    try:
        products = productController.get_all()
        if request.method == 'POST':

            product = productController.getDataProduct(request, None)
            productValidated = productController.productValidated(product)
            if not type(productValidated) == bool:
                return render_template("admin/inventory.html", products=products, error=productValidated, product = product)
            else:
                productController.create(product)
                products = productController.get_all()
                flash('Producto creado exitosamente', 'success')
                return render_template("admin/inventory.html", products=products, product = None)
        else:
            return render_template("admin/inventory.html", products=products, product = None )
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("admin/inventory.html", products=products, product = None)
    

@admin_app.route("/inventory/selectProduct/", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def select_Product():
    action = request.args.get('action')
    productId = request.args.get('IdProduct')  # Obtener el IdProduct desde los parámetros de la URL
    if not productId:
        return redirect(url_for('admin_app.inventory', error="No product selected."))
    # Almacenar productId en la sesión
    session['IdProduct'] = productId
    if action == 'view':
        return redirect(url_for('admin_app.viewProduct'))
    elif action == 'update':
        return redirect(url_for('admin_app.updateProduct'))
    else:
        return redirect(url_for('admin_app.inventory', error="Invalid action."))


@admin_app.route("/inventory/updateProduct", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateProduct():
    try:
        productId = session.get('IdProduct') 
        product = productController.get_one(productId)
        if request.method == 'POST':
            productUpdated = productController.getDataUpdateProduct(request, product.Image)
            productValidated = productController.productValidatedUpdate(product.Name, productUpdated)

            if not type(productValidated) == bool:
                    return render_template("admin/updateProduct.html", error=productUpdated, product = product)
        
            productController.updateProduct(product.ID_Product, productUpdated)
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('admin_app.inventory'))    
    
        else:
            return render_template("admin/updateProduct.html", product=product)
        
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("admin_app.inventory"))

@admin_app.route("/inventory/view", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewProduct():
    try:
        productId = session.get('IdProduct') 
        product = productController.getProductById(productId)
        return render_template("admin/viewProduct.html", product=product)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.inventory'))


@admin_app.route("/inventory/view/disable", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableProduct():
    productId = session.get('IdProduct') 
   
    disable = productController.disable_product(productId)

    if disable:
        return jsonify({"message": "Hecho"})
    else:
        # Manejar el caso en que no se encuentre el producto
        return jsonify({"error": "No se pudo deshabilitar"})
    
@admin_app.route("/inventory/view/able", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableProduct():
    productId = session.get('IdProduct') 
    
    able = productController.able_Product(productId)
    if able:
        return jsonify({"message": "Hecho"})
    else:
        # Manejar el caso en que no se encuentre el cliente
        return jsonify({"error": "No se pudo habilitar"})

# @admin_app.route("/inventory", methods = ['GET', 'POST'])
# @login_required
# @admin_permission.require(http_exception=403)
# def inventory():
#     products = productController.getProducts()
#     doneMessage = request.args.get('done')
#     errorMessage = request.args.get('error')
#     if request.method == 'POST':
#         product = ProductRepository.getDataProduct(request, None)
#         productValidated = ProductRepository.validateDataForm(product)
#         if not type(productValidated) == bool:
#             return render_template("admin/inventory.html", products=products, error=productValidated, product = product)
#         conection = Conection.conectar()
#         if conection == None:
#             return render_template("admin/inventory.html", products=products, error= "Error en la conexión.", product = product)
#         insert = ProductRepository.insertProduct(conection, product)
#         if insert and type(insert) == bool:
#             products = ProductRepository.get_all(conection)
#             Conection.desconectar()
#             # return render_template("admin/inventory.html", products=products, done = "Producto creado correctamente.", product = None)
#             return redirect(url_for('admin_app.inventory', done = "Producto creado correctamente."))
#         elif insert == "Unique":
#             Conection.desconectar()
#             return render_template("admin/inventory.html", products=products, error= "El nombre del producto ingresado ya esta registrado.", product = product)
#         elif insert == "DataBase":
#             return render_template("admin/inventory.html", products=products, error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", product = product)
#         else:
#             Conection.desconectar()
#             return render_template("admin/inventory.html", products=products, error= "No se pudo ingresar el producto, por favor inténtalo más tarde.", product = product)
#     else:
#         return render_template("admin/inventory.html", products=products, product = None, done = doneMessage, error = errorMessage)
    




# @admin_app.route("/inventory/view", methods=['GET'])
# @login_required
# @admin_permission.require(http_exception=403)
# def viewProduct():
#     productId = session.get('IdProduct') 
#     if not productId:
#         return redirect(url_for('admin_app.inventory', error="No product selected."))

#     product = productController.getProductId( productId)  # Asegurarse de que se usa productId

#     if product:
#         return render_template("admin/viewProduct.html", product=product)
#     else:
#         return redirect(url_for('admin_app.inventory', error="Producto no encontrado"))

# @admin_app.route("/inventory/updateProduct", methods=['POST', 'GET'])
# @login_required
# @admin_permission.require(http_exception=403)
# def updateProduct():
#     productId = session.get('IdProduct') 
#     product = productController.getProductId(productId)

#     if product:
#         if request.method == 'POST':
#             productUpdated = ProductRepository.getDataProduct(request, product.Image)
#             productValidated = ProductRepository.validateDataForm(productUpdated)
#             if not type(productValidated) == bool:
#                 return render_template("admin/updateProduct.html", error=productValidated, product = product)
#             conection = Conection.conectar()
#             if conection == None:
#                 return render_template("admin/updateProduct.html", error= "Error en la conexión.", product = product)
#             update = ProductRepository.updateProduct(conection, productUpdated, product.ID_Product)
#             Conection.desconectar()
#             if update and type(update) == bool:
#                 return redirect(url_for('admin_app.inventory', done = "Producto actualizado correctamente."))
#             elif update == "DataBase":
#                 return render_template("admin/updateProduct.html", error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", product = product)
#             else:
#                 return render_template("admin/updateProduct.html", error= "No se pudo actualizar el Producto.", product = product)
#         else:
#             return render_template("admin/updateProduct.html", product=product)
#     else:
#         return redirect(url_for("admin_app.inventory", error = "Producto no encontrado"))

# @admin_app.route("/inventory/view/disable", methods = ['POST'])
# @login_required
# @admin_permission.require(http_exception=403)
# def disableProduct():
#     data = request.get_json()
#     ID_Product = data.get('ProductId')
#     conexion = Conection.conectar()
#     disable = ProductRepository.disableProduct(conexion, ID_Product)
#     Conection.desconectar()
#     if disable:
#         return jsonify({"message": "Hecho"})
#     else:
#         return jsonify({"error": "No se pudo deshabilitar"})
    
# @admin_app.route("/inventory/view/able", methods = ['POST'])
# @login_required
# @admin_permission.require(http_exception=403)
# def ableProduct():
#     data = request.get_json()
#     ID_Product = data.get('ProductId')
#     conexion = Conection.conectar()
#     able = ProductRepository.ableProduct(conexion, ID_Product)
#     Conection.desconectar()
#     if able:
#         return jsonify({"message": "Hecho"})
#     else:
#         return jsonify({"error": "No se pudo habilitar"})


#-------------Rutas de Notificaciones-------------#
@admin_app.route("/notifications", methods = ['GET', 'POST'])
@login_required
def notifications():
    try:
        notifications = notificationController.get_all()
        if request.method == 'POST':
            notificationController.CreateData(request)
            notifications = notificationController.get_all()
            flash('Registro creado exitosamente', 'success')
            return render_template("admin/notifications.html", notifications=notifications, notification = None)
        else:
            return render_template("admin/notifications.html", notifications=notifications, notification = None)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("admin_app.notifications"))

@admin_app.route("/notifications/view/<ID_Notication>")
@login_required
@admin_permission.require(http_exception=403)
def viewNotification(ID_Notication):
    notification = None
    try:
        notification = notificationController.get_one(ID_Notication)
        return render_template("admin/viewNotification.html", notification=notification)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.notifications'))


@admin_app.route("/notifications/disable", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableNotification():
    try:
        data = request.get_json()
        ID_Notification = data.get('DocumentId')
        disable = notificationController.disableNotification(ID_Notification)

        if disable:
            return jsonify({"message": "Hecho"})
        else:
            return jsonify({"error": "No se pudo deshabilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.notifications'))

    
@admin_app.route("/notifications/able", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableNotification():
    try: 
        data = request.get_json()
        ID_Product = data.get('DocumentId')
        able = notificationController.ableNotification(ID_Product)

        if able:
            return jsonify({"message": "Hecho"})
        else:
            return jsonify({"error": "No se pudo habilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.notifications'))









@admin_app.route("/notifications/delete")
@login_required
def notificationsDesable(id):
    return render_template("admin/verNotificacion.html")

#-------------Reportes------------#
@admin_app.route("/billsReports", methods=['GET', 'POST'])
@login_required
def billsReports():
    connection = Conection.conectar()
    if request.method == 'POST':
        data = request.get_json()
        invoice_type = data.get('invoiceType')

        try:
            if invoice_type in ['diaria', 'semanal', 'mensual']:
                reports = ModelBill.get_reports(connection, invoice_type)
                if reports is None:
                    return jsonify({"error": "Error al obtener los reportes"}), 500
                return jsonify(reports)
            else:
                return jsonify({"error": "Tipo de reporte no válido"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template("admin/billsReports.html")


@admin_app.route("/generate_report_bill", methods=['GET'])
@login_required
def generate_reportBills_pdf():
    period = request.args.get('month')
    invoice_type = request.args.get('invoice_type')
    connection = Conection.conectar()
    reports = ModelBill.get_reports(connection, invoice_type)
    if not reports:
        return jsonify({"error": "No se encontraron reportes"}), 404

    filtered_reports = {}
    for group, group_reports in reports.items():
        if invoice_type == 'semanal':
            if str(group) == period:
                filtered_reports[group] = group_reports
        elif invoice_type in ['mensual', 'diaria']:
            if group == period:
                filtered_reports[group] = group_reports
    if not filtered_reports:
        return jsonify({"error": "No se encontraron reportes para el período seleccionado"}), 404
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    logo_path = "static/images/icono.jpg"
    try:
        c.drawImage(logo_path, 450, 750, width=1.5 * inch, height=0.8 * inch, preserveAspectRatio=True)
    except Exception as ex:
        print(f"Error al cargar el logo: {ex}")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor("#c0392b"))
    c.drawString(50, 750, f"Reporte de Facturas - {invoice_type.capitalize()} ({period})")
    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#7f8c8d"))
    c.drawString(50, 730, f"Detalles de facturación para el período de {period}")
    c.setFont("Helvetica", 10)
    for group, group_reports in filtered_reports.items():
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 700, f"Fecha: {group}")
        y_position = 680

        entity_groups = {}
        for report in group_reports:
            entity_type = report.get('TipoEntidad', 'General')
            if entity_type not in entity_groups:
                entity_groups[entity_type] = []
            entity_groups[entity_type].append(report)

        for entity_type, reports_in_entity in entity_groups.items():
            entity_title = {
                'Entrenador': 'Pago Entrenador',
                'Cliente': 'Membresía Cliente',
                'Producto': 'Venta de Producto',
                'General': 'General'
            }.get(entity_type, 'General')

            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y_position, f"{entity_title}")
            y_position -= 20
            y_position -= 10
            data = []
            if entity_type == 'Producto':
                data = [["Producto", "Monto", "Fecha"]]
                for report in reports_in_entity:
                    data.append([report.get('Producto', 'N/A'), report['Monto'], report.get('Fecha', 'N/A')])
            elif entity_type in ['Cliente', 'Entrenador']:
                data = [["Nombre", "Cédula", "Monto", "Fecha"]]
                for report in reports_in_entity:
                    data.append([report.get('Nombre', 'N/A'), report.get('Cedula', 'N/A'), report['Monto'], report.get('Fecha', 'N/A')])
            else:
                data = [["Descripción", "Monto", "Fecha"]]
                for report in reports_in_entity:
                    data.append([report['Descripcion'], report['Monto'], report.get('Fecha', 'N/A')])

            table = Table(data, colWidths=[70, 150, 90, 90, 90])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor("#e74c3c")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ]))
            table.wrapOn(c, 50, y_position - 20)
            table.drawOn(c, 50, y_position - 40)

            y_position -= len(reports_in_entity) * 20 + 40  
    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"reporte_facturas_{period}.pdf", mimetype="application/pdf")

@admin_app.route("/inventoryReports", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def inventoryReports():
    conection = Conection.conectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    reports = ModelBill.get_ProductBills(conection)  
    Conection.desconectar()
    return render_template("admin/inventoryReports.html", reports=reports, done=doneMessage, error=errorMessage)


@admin_app.route("/generate_report_pdf", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def generate_report_pdf():
    month = request.args.get('month')
    conection = Conection.conectar()

    reports = ModelBill.get_ProductBills(conection).get(month, [])
    Conection.desconectar()

    if not reports:
        return "No hay facturas para este mes", 404

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    logo_path = "static/images/icono.jpg"
    try:
        c.drawImage(logo_path, 450, 700, width=1.5 * inch, height=0.8 * inch, preserveAspectRatio=True)
    except Exception as ex:
        print(f"Error al cargar el logo: {ex}")

    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(HexColor("#c0392b"))  
    c.drawString(50, 750, f"Reporte de Inventario - {month}")

    c.setFont("Helvetica", 12)
    c.setFillColor(HexColor("#7f8c8d"))
    c.drawString(50, 730, f"Reporte de ventas de productos para el mes de {month}")

    c.setFont("Helvetica", 10)

    data = [["Código", "Producto", "Precio", "Cantidad Vendida", "Total Vendido"]]
    for report in reports:
        row = [
            str(report['ProductCode']),
            report['ProductName'],
            f"{report['Price']:.2f}",
            str(report['QuantitySold']),
            f"{report['TotalSold']:.2f}"
        ]
        data.append(row)

    table = Table(data, colWidths=[70, 150, 90, 90, 90])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#e74c3c")),  
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey), 
        ('LINEABOVE', (0, 0), (-1, 0), 1, HexColor("#c0392b")), 
        ('LINEBELOW', (0, -1), (-1, -1), 1, HexColor("#c0392b")),  
        ('LINEBEFORE', (0, 0), (0, -1), 1, HexColor("#c0392b")),  
        ('LINEAFTER', (-1, 0), (-1, -1), 1, HexColor("#c0392b")),  
    ]))

    table.wrapOn(c, 50, 600)
    table.drawOn(c, 50, 500)  

    c.setStrokeColor(HexColor("#c0392b"))
    c.setLineWidth(1)
    c.line(50, 490, 550, 490)  

    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name=f"reporte_inventario_{month}.pdf", mimetype="application/pdf")


    #-------------Perfil------------#
@admin_app.route("/profile")
@login_required
def profile():
    return render_template("admin/profile.html")

#-------------Rutas de Membresias-------------#
@admin_app.route("/memberships", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def memberships():
    conection = Conection.conectar()
    memberships = ModelMembership.get_all(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        membership = ModelMembership.getDataMembership(request)
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
            return redirect(url_for('admin_app.memberships', done = "Membresía creada correctamente."))
        elif insert == "Unique":
            return render_template("admin/membership.html", memberships=memberships, error= "Ya existe una membresía con el nombre ingresado.", membership = membership)
        elif insert == "DataBase":
            return render_template("admin/membership.html", memberships=memberships, error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", membership = membership)
        else:
            Conection.desconectar()
            return render_template("admin/membership.html", memberships=memberships, error= "No se pudo ingresar la membresía, por favor inténtalo más tarde.", membership = membership)
    else:
        return render_template("admin/membership.html", memberships=memberships, membership = None, done = doneMessage, error = errorMessage)

@admin_app.route("/membership/updateMembership/<id>", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateMembership(id):
    conexion = Conection.conectar()
    membership = ModelMembership.getMembership(conexion, id)
    Conection.desconectar()
    if membership:
        if request.method == 'POST':
            membershipUpdate = ModelMembership.getDataMembership(request)
            membershipValidated = ModelMembership.validateDataForm(membershipUpdate)
            if not type(membershipValidated) == bool:
                return render_template("admin/updateMembership.html", error=membershipValidated, membership = membership)
            conection = Conection.conectar()
            if conection == None:
                return render_template("admin/updateMembership.html", error= "Error en la conexión.", membership = membership)
            update = ModelMembership.updateMembership(conection, membershipUpdate, id)
            Conection.desconectar()
            if update and type(update) == bool:
                return redirect(url_for('admin_app.memberships', done = "Membresia actualizada correctamente."))
            elif update == "DataBase":
                return render_template("admin/updateMembership.html", error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", membership = membership)
            else:
                return render_template("admin/updateMembership.html", error= "No se pudo actualizar la membresia.", membership = membership)
        else:
            return render_template("admin/updateMembership.html", membership = membership)
    else:
        return redirect(url_for("admin_app.memberships", error = "Membresia no encontrada."))

@admin_app.route("/membership/view/<id>")
@login_required
def viewMembership(id):
    conection = Conection.conectar()
    membership = ModelMembership.getMembership(conection, id)
    Conection.desconectar()
    if membership:
        return render_template("admin/viewMembership.html", membership=membership)
    else:
        return redirect(url_for("admin_app.memberships", error = "Membresia no encontrada."))
    

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