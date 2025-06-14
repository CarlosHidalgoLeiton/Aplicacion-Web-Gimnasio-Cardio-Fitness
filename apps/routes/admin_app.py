# Importaciones
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from flask_login import login_required
from apps.db.conection import Conection
from apps.db.repositories.UserRepository import UserRepository
from apps.db.repositories.ClientRepository import ClientRepository

from apps.db.models.User import User
from apps.routes.permissions import admin_permission
import json  
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from io import BytesIO
from flask import send_file
from apps.controllers.user_controller import userController
from apps.controllers.client_controller import clientController
from apps.controllers.trainer_controller import trainerController
from apps.controllers.statistics_controller import statisticsController
from apps.controllers.inventory_controller import productController
from apps.controllers.notification_controller import notificationController
from apps.controllers.bill_controller import billController
from apps.controllers.cancelledBill_controller import cancelledBillController
from apps.controllers.routine_controller import routineController
from apps.controllers.session_controller import sessionController
from apps.controllers.membership_controller import membershipController
from collections import defaultdict
# from apps.controllers.report_controller import reportController

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
                flash('Registro creado exitosamente', 'success')
                return redirect(url_for("admin_app.clients"))
        else:
            return render_template("admin/clients.html", clients=clients, client = None )
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("admin_app.clients"))    
    
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

@admin_app.route("/clientes/disable", methods = ['POST'])
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
    
@admin_app.route("/clientes/able", methods = ['POST'])
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
    try:
        statistics = statisticsController.getStatisticsByClientId(documentId)
        return render_template("admin/statistics.html", statistics=statistics,documentId = documentId)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.clients'))

@admin_app.route("/viewStatistics/<documentId>/<clientId>", methods = ['GET'])
@login_required
def viewStatistics(documentId,clientId):
    try:
        statistics = statisticsController.getStatisticById(documentId)
        return render_template("admin/viewStatistics.html", statistics=statistics)
    
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.statisticsClient'))


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
        return render_template("admin/viewRoutine.html", routine=routine, sessions=sessions, client=client,DocumentId=DocumentId)

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
        ID_Routine = request.args.get("routine_id")
        DocumentId = request.args.get("DocumentId")
        session = sessionController.findOneById(Session_ID)
        session.Exercises = json.loads(session.Exercises)

        return render_template("admin/viewSession.html", session=session, routine=session.routine)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.routinesClient', ID_Routine = ID_Routine, DocumentId = DocumentId))

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
            flash('Registro creado exitosamente', 'success')
            return redirect(url_for('admin_app.trainers'))
        else:
            return render_template("admin/trainers.html", trainers=trainers, trainer = None)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.trainers'))
 

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

#Aquí he cambiadooo
@admin_app.route("/users", methods = ['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def users():
    try:
        users = userController.get_all()
        clients = userController.get_Clients() 
        trainers = userController.get_Trainers() 
        if request.method == 'POST':
            user = userController.getData(request)
            userValidated = userController.validateDataForm(user)
            if not type(userValidated) == bool:
                return render_template("admin/users.html", users=users,  clients=clients, trainers=trainers,  error=userValidated, user = user)
            userController.create(user)
            flash('Registro creado exitosamente', 'success')
            return redirect(url_for('admin_app.users'))
        else:
            return render_template("admin/users.html", users=users, clients=clients, trainers=trainers, user = None)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("admin/users.html", users=users, clients=clients, trainers=trainers, user = None)
    
    
@admin_app.route("/users/view/<DocumentId>", methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewUser(DocumentId):
    try:
        user = userController.getUser(DocumentId)
        return render_template("admin/viewUser.html", user=user)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.users'))
    

@admin_app.route("/users/update/<DocumentId>", methods = ['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateUser(DocumentId):

    try:
        user = userController.getUser(DocumentId)

        if request.method == 'POST':
           
            userUpdated = userController.getDataUpdate(request)
            userValidated = userController.validateDataFormUpdate(userUpdated,DocumentId)

            if not type(userValidated) == bool:
                return render_template("admin/updateUser.html", error=userValidated, user = user)
            
            if not userUpdated.Password:
                userUpdated.Password = user.Password

            userController.updateUser(user.id ,userUpdated )
            flash('Registro actualizado exitosamente', 'success')
            return redirect(url_for('admin_app.users'))
                
        return render_template("admin/updateUser.html", user = user)
    
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("admin_app.users"))



@admin_app.route("/users/able", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableUser():
    try:
        data = request.get_json()
        DocumentId = data.get('DocumentId')
        able = userController.able_user(DocumentId)
        if able:
            return jsonify({"message": "Hecho"})
        else:
            # Manejar el caso en que no se encuentre el cliente
            return jsonify({"error": "No se pudo habilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.users'))
    

@admin_app.route("/users/disable", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableUser():
    try:
        data = request.get_json()
        DocumentId = data.get('DocumentId')
    
        disable = userController.disable_user(DocumentId)

        if disable:
            return jsonify({"message": "Hecho"})
        else:
            # Manejar el caso en que no se encuentre el cliente
            return jsonify({"error": "No se pudo deshabilitar"})
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.users'))
    


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

                lotEnough = billController.validateStock(stock ,bill.Quantity)
                if lotEnough:
                    Quantity = stock - int(bill.Quantity)
                    billController.updateQuantityProduct(Quantity, bill.ID_Entity)
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
                flash('Producto creado exitosamente', 'success')
                return redirect(url_for('admin_app.inventory'))
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


#-------------Rutas de Notificaciones-------------#
@admin_app.route("/notifications", methods = ['GET', 'POST'])
@login_required
def notifications():
    try:
        notifications = notificationController.get_all()
        if request.method == 'POST':
            notificationController.CreateData(request)
            flash('Registro creado exitosamente', 'success')
            return redirect(url_for("admin_app.notifications"))
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
        ID_Notification = data.get('DocumentId')
        able = notificationController.ableNotification(ID_Notification)

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


#------------- Reportes (Facturas) ------------#

@admin_app.route("/billsReports", methods=['GET', 'POST'])
@login_required
def billsReports():
    if request.method == 'POST':
        data = request.get_json()
        invoice_type = data.get('invoiceType')
        try:
            if invoice_type in ['diaria', 'semanal', 'mensual']:
                reports = billController.get_reports(invoice_type)
                if reports is None:
                    return jsonify({"error": "Error al obtener los reportes"}), 500
                return jsonify(reports['data'])
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

    if not period or not invoice_type:
        return jsonify({"error": "Parámetros requeridos: month e invoice_type"}), 400

    reports = billController.get_reports_bills(invoice_type)
    if not reports:
        return jsonify({"error": "No se encontraron reportes"}), 404

    # Filtrar por el período solicitado
    filtered_reports = {
        group: items for group, items in reports.items()
        if str(group) == str(period)
    }

    if not filtered_reports:
        return jsonify({"error": "No se encontraron reportes para el período seleccionado"}), 404

    # Comenzar la generación del PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Título y logo
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
    y_position = 700

    # Contenido de facturas
    for group, group_reports in filtered_reports.items():
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(50, y_position, f"Fecha: {group}")
        y_position -= 20

        entity_groups = defaultdict(list)
        for report in group_reports:
            entity_type = report.get('TipoEntidad', 'General')
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

            # Armar la tabla
            if entity_type == 'Producto':
                data = [["Producto", "Cantidad", "Monto", "Fecha"]]
                for r in reports_in_entity:
                    data.append([r.get('Producto', 'N/A'), str(r['Cantidad']),str(r['Monto']), str(r.get('Fecha', 'N/A'))])
            elif entity_type in ['Cliente', 'Entrenador']:
                data = [["Nombre", "Cédula", "Monto", "Fecha"]]
                for r in reports_in_entity:
                    data.append([
                        r.get('Nombre', 'N/A'),
                        r.get('Cedula', 'N/A'),
                        str(r['Monto']),
                        str(r.get('Fecha', 'N/A'))
                    ])
            else:
                data = [["Descripción", "Monto", "Fecha"]]
                for r in reports_in_entity:
                    data.append([r.get('Descripcion', 'N/A'), str(r['Monto']), str(r.get('Fecha', 'N/A'))])

            col_count = len(data[0])
            col_width = 500 / col_count
            table = Table(data, colWidths=[col_width] * col_count)
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

            table_height = 20 * len(data)
            if y_position - table_height < 100:  # Salto de página si no hay espacio
                c.showPage()
                y_position = 750
                c.setFont("Helvetica-Bold", 12)
                c.drawString(50, y_position, f"{entity_title}")
                y_position -= 20

            table.wrapOn(c, 50, y_position)
            table.drawOn(c, 50, y_position - table_height)
            y_position -= table_height + 30  # Espacio después de la tabla

    c.showPage()
    c.save()
    buffer.seek(0)

    return send_file(
        buffer,
        as_attachment=True,
        download_name=f"reporte_facturas_{period}.pdf",
        mimetype="application/pdf"
    )

#------------- Reportes (Inventario Productos) ------------#
@admin_app.route("/inventoryReports", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def inventoryReports():
    try:
        reports = billController.get_product_bills()
        print(reports)
        return render_template("admin/inventoryReports.html",
                           reports=reports)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for('admin_app.inicio'))

@admin_app.route("/generate_report_pdf", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def generate_report_pdf():
    month = request.args.get('month')

    all_reports = billController.get_product_bills()

    if not all_reports or month not in all_reports:
        return "No hay facturas para este mes", 404

    reports = all_reports[month] 

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
            str(report['ID_Producto']),
            report['Nombre_Producto'],
            f"{report['Precio']:.2f}",
            str(report['Cantidad']),
            f"{report['Total_Vendido']:.2f}"
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

#-------------------Membresias------------------- #
@admin_app.route("/memberships", methods=['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def memberships():
    try:
        memberships = membershipController.get_all()

        if request.method == 'POST':
            membership = membershipController.getDataMembershipSent(request)
            membershipValidated = membershipController.membershipValidated(membership)

            if not type(membershipValidated) == bool:
                return render_template("admin/membership.html", memberships=memberships, error=membershipValidated, membership=membership)
            else:
                membershipController.create_membership(membership)
                memberships = membershipController.get_all()
                flash('Membresía creada exitosamente', 'success')
                return render_template("admin/membership.html", memberships=memberships, membership=None)
        else:
            return render_template("admin/membership.html", memberships=memberships, membership=None)

    except Exception as ex:
        flash(ex.args[0], 'danger')
        return render_template("admin/membership.html", memberships=[], membership=None)



@admin_app.route("/membership/updateMembership/<id>", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateMembership(id):
    try:
        if request.method == 'POST':
            membership_data = membershipController.getDataMembershipSent(request)
            membershipValidated = membershipController.membershipValidated(membership_data)

            if not isinstance(membershipValidated, bool):
                membership_data["id"] = id
                return render_template("admin/updateMembership.html", error=membershipValidated, membership=membership_data)

            updated = membershipController.update_membership(id, membership_data)

            if updated:
                flash("Membresía actualizada correctamente.", "success")
                return redirect(url_for("admin_app.memberships"))
            else:
                flash("No se pudo actualizar la membresía.", "danger")
                return redirect(url_for("admin_app.updateMembership", id=id))

        else:
            membership = membershipController.get_by_id(id)
            return render_template("admin/updateMembership.html", membership=membership)

    except Exception as ex:
        flash(ex.args[0], "danger")
        return redirect(url_for("admin_app.memberships"))

@admin_app.route("/membership/view/<id>")
@login_required
def viewMembership(id):
    try:
        membership = membershipController.get_by_id(id)
        return render_template("admin/viewMembership.html", membership=membership)
    except Exception as ex:
        flash(ex.args[0], 'danger')
        return redirect(url_for("admin_app.memberships"))

@admin_app.route("/membresias/deshabilitar", methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableMembership():
    data = request.get_json()
    membershipId = data.get('membershipId')

    try:
        result = membershipController.disable_membership(membershipId)
        if result:
            return jsonify({"message": "Hecho"})
        else:
            return jsonify({"error": "No se pudo deshabilitar la membresía"})
    except Exception as e:
        return jsonify({"error": str(e)})

    


@admin_app.route("/membresias/habilitar", methods=['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableMembership():
    data = request.get_json()
    membershipId = data.get('membershipId')

    try:
        result = membershipController.enable_membership(membershipId)
        if result:
            return jsonify({"message": "Hecho"})
        else:
            return jsonify({"error": "No se pudo habilitar la membresía"})
    except Exception as e:
        return jsonify({"error": str(e)})
