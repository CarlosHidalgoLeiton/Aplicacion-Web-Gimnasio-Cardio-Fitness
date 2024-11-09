#Importaciones
from flask import Blueprint, render_template, request,session, redirect, url_for, jsonify
from flask_login import login_required, current_user
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.ModelTrainer import ModelTrainer
from db.models.ModelClient import ModelClient
from db.models.ModelProduct import ModelProduct
from db.models.ModelMembership import ModelMembership
from db.models.ModelBill import ModelBill
from db.models.ModelCancelledBill import ModelCancelledBill
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
    client = ModelClient.getClient(conexion, documentId)
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
    client = ModelClient.getClient(conexion, documentId)
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

#-------------Rutas de Entrenadores-------------#

#Aquí he cambiadooo
@admin_app.route("/trainers", methods = ['POST', 'GET'])
@login_required
def trainers():
    conection = Conection.conectar()
    trainers = ModelTrainer.get_all(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        trainer = ModelTrainer.getDataTrainer(request)
        trainerValidated = ModelTrainer.validateDataForm(trainer)
        if not type(trainerValidated) == bool:
            return render_template("admin/trainers.html", trainers=trainers, error=trainerValidated, trainer = trainer)
        conection = Conection.conectar()
        if conection == None:
            return render_template("admin/trainers.html", trainers=trainers, error= "Error en la conexión.", trainer = trainer)
        insert = ModelTrainer.insertTrainer(conection, trainer)
        if insert and type(insert) == bool:
            Conection.desconectar()
            return redirect(url_for("admin_app.trainers", done = "Entrenador creado correctamente."))
        elif insert == "Primary":
            Conection.desconectar()
            return render_template("admin/trainers.html", trainers=trainers, error= "El número de cédula ingresado ya esta registrado con otro entrenador.", trainer = trainer)
        elif insert == "DataBase":
            return render_template("admin/trainers.html", trainers=trainers, error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", trainer = trainer)
        else:
            Conection.desconectar()
            return render_template("admin/trainers.html", trainers=trainers, error= "No se pudo ingresar el entrenador, por favor inténtalo más tarde.", trainer = trainer)
    else:
        return render_template("admin/trainers.html", trainers=trainers, trainer = None, done = doneMessage, error = errorMessage)

@admin_app.route("/trainer/update/<documentId>", methods = ['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateTrainer(documentId):
    conection = Conection.conectar()
    trainer = ModelTrainer.getTrainer(conection, documentId)
    Conection.desconectar()

    if trainer:
        if request.method == 'POST':
            trainerUpdated = ModelTrainer.getDataTrainer(request)
            trainerValidated = ModelTrainer.validateDataForm(trainerUpdated)

            if not type(trainerValidated) == bool:
                return render_template("admin/updateTrainer.html", error=trainerValidated, trainer = trainer)
            conection = Conection.conectar()
            update = ModelTrainer.updateTrainer(conection, trainerUpdated, trainer.DocumentId)
            Conection.desconectar()
            if update and type(update) == bool:
                return redirect(url_for('admin_app.trainers', done = "Entrenador actualizado correctamente."))
            elif update == "Primary":
                return render_template("admin/updateTrainer.html", error= "El número de cédula ingresado ya esta registrado con otro entrenador.", trainer = trainer)
            elif update == "DataBase":
                return render_template("admin/updateTrainer.html", error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", trainer = trainer)
            else:
                return render_template("admin/updateTrainer.html", error= "No se pudo actualizar el entrenador.", trainer = trainer)
    else:
        return redirect(url_for("admin_app.trainer", error = "Entrenador no encontrado."))

    return render_template("admin/updateTrainer.html", trainer = trainer)


@admin_app.route("/entrenadores/ver")
@login_required
def verEntrenador():
    return render_template("admin/verEntrenador.html")

@admin_app.route("/trainer/disable", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableTrainer():
    data = request.get_json()
    DocumentId = data.get('clientID')
    conexion = Conection.conectar()
    disable = ModelTrainer.disableTrainer(conexion, DocumentId)
    Conection.desconectar()

    if disable:
        return jsonify({"message": "Hecho"})
    else:
        
        return jsonify({"error": "No se pudo deshabilitar"})
    
@admin_app.route("/trainer/able", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableTrainer():
    data = request.get_json()
    DocumentId = data.get('clientID')
    conection = Conection.conectar()
    able = ModelTrainer.ableTrainer(conection, DocumentId)
    Conection.desconectar()

    if able:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo habilitar"})
    

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
    conection = Conection.conectar()
    able = ModelUser.ableUser(conection, DocumentId)
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
    conection = Conection.conectar()

    if not conection:
        return render_template("admin/bill.html", error = "No se pudo conectar con la base de datos.", clients = None, trainers = None, memberships = None, products = None)

    bills = ModelBill.get_all(conection)
    clients = ModelClient.get_allAble(conection)
    trainers = ModelTrainer.get_allAble(conection)
    memberships = ModelMembership.get_allAble(conection)
    products = ModelProduct.get_allAble(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        if request.form['typeEntity'] == 'Trainer':
            bill = ModelBill.getDataTrainerBill(request)
            validatedBill = ModelBill.validateDataFormTrainer(bill)
            if not type(validatedBill) == bool:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = validatedBill, trainerValidated = bill, generalValidated = None, productValidated = None, membershipValidated = None  ) 

            conection = Conection.conectar()
            insert = ModelBill.insertTrainerBill(conection, bill)
            Conection.desconectar()
            if insert and type(insert) == bool:
                return redirect(url_for('admin_app.bills', done = "Pago registrado correctamente."))
            elif insert == "DataBase":
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.', trainerValidated = bill, generalValidated = None, productValidated = None, membershipValidated = None ) 
            else:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se pudo realizar el pago.', trainerValidated = bill, generalValidated = None, productValidated = None, membershipValidated = None ) 
    
        if request.form['typeEntity'] == 'General':
            bill = ModelBill.getDataGeneralBill(request)
            validatedBill = ModelBill.validateDataFormGeneral(bill)
            if not type(validatedBill) == bool:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = validatedBill, generalValidated = bill, trainerValidated = None,productValidated = None, membershipValidated = None ) 

            conection = Conection.conectar()
            insert = ModelBill.insertGeneralBill(conection, bill)

            if insert and type(insert) == bool:
                return redirect(url_for('admin_app.bills', done = "Pago registrado correctamente."))
            elif insert == "DataBase":
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.', trainerValidated = None, generalValidated = bill, productValidated = None, membershipValidated = None ) 
            else:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se pudo realizar el pago.', generalValidated = bill, trainerValidated = None, productValidated = None, membershipValidated = None ) 
    
        if request.form['typeEntity'] == 'Product':
            bill = ModelBill.getDataProductBill(request)
            validatedBill = ModelBill.validateDataFormProduct(bill)
            if not type(validatedBill) == bool:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = validatedBill, productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None  ) 

            conection = Conection.conectar()
            stock = ModelBill.getStock(conection, bill.ID_Entity)

            if not stock:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se pudo realizar el pago.', productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None ) 

            lotEnough = ModelBill.validateStock(stock ,bill.Lot)
            if lotEnough:
                insert = ModelBill.insertProductBill(conection, bill, (stock-int(bill.Lot)))
                Conection.desconectar()
                if insert and type(insert) == bool:
                    return redirect(url_for('admin_app.bills', done = "Pago registrado correctamente."))
                elif insert == "DataBase":
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.', productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None ) 
                else:
                    return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se pudo realizar el pago.', productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None ) 
            else:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'La cantidad ingresada excede la cantidad en el stock.', productValidated = bill, generalValidated = None, trainerValidated = None, membershipValidated = None ) 

        if request.form['typeEntity'] == 'Membership':
            bill = ModelBill.getDataMembershipBill(request)
            validatedBill = ModelBill.validateDataFormMembership(bill)
            if not type(validatedBill) == bool:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = validatedBill, membershipValidated = bill, generalValidated = None, trainerValidated = None, productValidated = None) 

            conection = Conection.conectar()
            insert = ModelBill.insertMembershipBill(conection, bill)
            Conection.desconectar()

            if insert and type(insert) == bool:
                if request.form['typeEntity']=='Membership':
                    # Obtener los datos del cliente y membresía
                    conection = Conection.conectar()
                    client = ModelBill.getDataMembershipClient(conection, request)
                    Conection.desconectar()


                    # Validar los datos obtenidos del formulario
                    validation_result = ModelBill.validateDataFormMembershipClient(client)
                
                    if validation_result == True:
                        # Intentar actualizar la membresía del cliente
                        conection = Conection.conectar()
                        update_result = ModelBill.updateClientMembership(conection, client)
                        Conection.desconectar()


                        if update_result == True:
                            return redirect(url_for('admin_app.bills', done="Pago registrado correctamente y cliente actualizado."))
                        else:
                            return render_template("admin/bill.html", bills=bills, clients=clients, memberships=memberships, error="Error actualizando el cliente.", membershipValidated=bill, generalValidated=None, trainerValidated=None, productValidated=None)
                else:
                    # Si la validación falla, mostrar el mensaje de error
                    return render_template("admin/bill.html", bills=bills, clients=clients, memberships=memberships, error=validation_result, membershipValidated=bill, generalValidated=None, trainerValidated=None, productValidated=None)

            elif insert == "DataBase":
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.', membershipValidated = bill, generalValidated = None, trainerValidated = None, productValidated = None ) 
            else:
                return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, error = 'No se pudo realizar el pago.',  membershipValidated = bill, generalValidated = None, trainerValidated = None, productValidated = None  ) 
    
    else:
        return render_template("admin/bill.html", bills = bills, trainers = trainers, clients = clients, memberships = memberships, products = products, trainerValidated = None, generalValidated = None, productValidated = None, membershipValidated = None , done = doneMessage, error = errorMessage)

@admin_app.route("/facturas/ver")
@login_required
def verFactura():
    return render_template("admin/verFactura.html")

@admin_app.route("/bills/cancel/<ID_Bill>", methods = ['GET', 'POST'])
@login_required
@admin_permission.require(http_exception=403)
def cancelBill(ID_Bill):
    if request.method == 'POST':
        cancelBill = ModelCancelledBill.getDataCanceledBill(request)
        validatedCancel = ModelCancelledBill.validateDataForm(cancelBill)

        if not type(validatedCancel) == bool:
            return render_template('admin/cancelBill.html', error = validatedCancel, cancelBill = cancelBill, ID_Bill = ID_Bill)
        
        conection = Conection.conectar()
        insert = ModelCancelledBill.insertCancelledBill(conection ,cancelBill)

        if insert and type(insert) == bool:
            return redirect(url_for('admin_app.bills', done = "Factura anulada correctamente."))
        elif insert == "DataBase":
            return render_template("admin/cancelBill.html", error = "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", ID_Bill = ID_Bill, cancelBill = cancelBill) 
        else:
            return render_template("admin/cancelBill.html", error = "No se pudo realizar la anulación de la factura.", ID_Bill = ID_Bill, cancelBill = cancelBill) 

    return render_template("admin/cancelBill.html", ID_Bill = ID_Bill, cancelBill = None)  

@admin_app.route("/bills/viewCancelBill/<ID_Bill>", methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewcancelBill(ID_Bill):
    
    if ID_Bill != None:
        conection = Conection.conectar()
        bill = ModelBill.getBill(conection, ID_Bill)
        cancelBill = ModelCancelledBill.getCancelBill(conection, ID_Bill)
        if not bill or not cancelBill:
            return redirect(url_for('admin_app.bills', error = "No se pudo obtener la información de la factura anulada."))

        if bill.EntityType == 'Entrenador':
            trainer = ModelTrainer.getTrainerBill(conection, bill.ID_Entity)
            
            return render_template('admin/viewCancel.html', trainer = trainer, ID_Bill = ID_Bill, bill = bill, cancelBill = cancelBill)
                
        elif bill.EntityType == 'Cliente': 
            client = ModelClient.getClientBill(conection, bill.ID_Entity)
            
            return render_template('admin/viewCancel.html', client = client, ID_Bill = ID_Bill, bill = bill, cancelBill = cancelBill)
        
        else:
            return render_template('admin/viewCancel.html', ID_Bill = ID_Bill, bill = bill, cancelBill = cancelBill)

    
    return redirect(url_for('admin_app.bills', error = "No se pudo obtener la información de la factura anulada."))





    return render_template('admin/viewCancel.html', ID_Bill = ID_Bill)

@admin_app.route('/getClients', methods = ['GET'])
@login_required
@admin_permission.require(http_exception=403)
def getClientsPay():
    conection = Conection.conectar()
    clients = ModelClient.get_all(conection)
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
    conection = Conection.conectar()
    products = ModelProduct.get_all(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        product = ModelProduct.getDataProduct(request, None)
        productValidated = ModelProduct.validateDataForm(product)
        if not type(productValidated) == bool:
            return render_template("admin/inventory.html", products=products, error=productValidated, product = product)
        conection = Conection.conectar()
        if conection == None:
            return render_template("admin/inventory.html", products=products, error= "Error en la conexión.", product = product)
        insert = ModelProduct.insertProduct(conection, product)
        if insert and type(insert) == bool:
            products = ModelProduct.get_all(conection)
            Conection.desconectar()
            # return render_template("admin/inventory.html", products=products, done = "Producto creado correctamente.", product = None)
            return redirect(url_for('admin_app.inventory', done = "Producto creado correctamente."))
        elif insert == "Unique":
            Conection.desconectar()
            return render_template("admin/inventory.html", products=products, error= "El nombre del producto ingresado ya esta registrado.", product = product)
        elif insert == "DataBase":
            return render_template("admin/inventory.html", products=products, error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", product = product)
        else:
            Conection.desconectar()
            return render_template("admin/inventory.html", products=products, error= "No se pudo ingresar el producto, por favor inténtalo más tarde.", product = product)
    else:
        return render_template("admin/inventory.html", products=products, product = None, done = doneMessage, error = errorMessage)

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

@admin_app.route("/inventory/view", methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def viewProduct():
    productId = session.get('IdProduct') 
    if not productId:
        return redirect(url_for('admin_app.inventory', error="No product selected."))

    conexion = Conection.conectar()
    product = ModelProduct.get_product_by_id(conexion, productId)  # Asegurarse de que se usa productId
    Conection.desconectar()

    if product:
        return render_template("admin/viewProduct.html", product=product)
    else:
        return redirect(url_for('admin_app.inventory', error="Producto no encontrado"))

@admin_app.route("/inventory/updateProduct", methods=['POST', 'GET'])
@login_required
@admin_permission.require(http_exception=403)
def updateProduct():
    productId = session.get('IdProduct') 
    conexion = Conection.conectar()
    product = ModelProduct.get_product_by_id(conexion, productId)
    Conection.desconectar()
    if product:
        if request.method == 'POST':
            productUpdated = ModelProduct.getDataProduct(request, product.Image)
            productValidated = ModelProduct.validateDataForm(productUpdated)
            if not type(productValidated) == bool:
                return render_template("admin/updateProduct.html", error=productValidated, product = product)
            conection = Conection.conectar()
            if conection == None:
                return render_template("admin/updateProduct.html", error= "Error en la conexión.", product = product)
            update = ModelProduct.updateProduct(conection, productUpdated, product.ID_Product)
            Conection.desconectar()
            if update and type(update) == bool:
                return redirect(url_for('admin_app.inventory', done = "Producto actualizado correctamente."))
            elif update == "DataBase":
                return render_template("admin/updateProduct.html", error= "No se puede conectar a la base de datos, por favor inténtalo más tarde o comuniquese con el desarrollador.", product = product)
            else:
                return render_template("admin/updateProduct.html", error= "No se pudo actualizar el Producto.", product = product)
        else:
            return render_template("admin/updateProduct.html", product=product)
    else:
        return redirect(url_for("admin_app.inventory", error = "Producto no encontrado"))

@admin_app.route("/inventory/view/disable", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def disableProduct():
    data = request.get_json()
    ID_Product = data.get('ProductId')
    conexion = Conection.conectar()
    disable = ModelProduct.disableProduct(conexion, ID_Product)
    Conection.desconectar()
    if disable:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo deshabilitar"})
    
@admin_app.route("/inventory/view/able", methods = ['POST'])
@login_required
@admin_permission.require(http_exception=403)
def ableProduct():
    data = request.get_json()
    ID_Product = data.get('ProductId')
    conexion = Conection.conectar()
    able = ModelProduct.ableProduct(conexion, ID_Product)
    Conection.desconectar()
    if able:
        return jsonify({"message": "Hecho"})
    else:
        return jsonify({"error": "No se pudo habilitar"})


#-------------Rutas de Notificaciones-------------#
@admin_app.route("/notifications", methods = ['GET', 'POST'])
@login_required
def notifications():
    conection = Conection.conectar()
    notifications = ModelUser.get_Notifications(conection)
    Conection.desconectar()
    doneMessage = request.args.get('done')
    errorMessage = request.args.get('error')
    if request.method == 'POST':
        notification = ModelUser.getDataNotification(request)
        conection = Conection.conectar()
        if conection == None:
            return render_template("admin/notifications.html", notifications=notifications, error= "Error en la conexión.", notification=notification)
        insert = ModelUser.insertNotification(conection, notification)
        if insert and type(insert) == bool:
            notifications = ModelUser.get_Notifications(conection)
            Conection.desconectar()
            return render_template("admin/notifications.html", notifications=notifications, done = "Notificación creada correctamente.", notification = None)
        else:
            Conection.desconectar()
            return render_template("admin/notifications.html", notifications=notifications, error= "No se pudo ingresar la notificación, por favor inténtalo más tarde.", notification=notification)
    else:
        return render_template("admin/notifications.html", notifications=notifications, notification = None, done = doneMessage, error = errorMessage)

@admin_app.route("/notifications/ver")
@login_required
def notificationsView(id):
    return render_template("admin/verNotificacion.html")

@admin_app.route("/notifications/delete")
@login_required
def notificationsDesable(id):
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