#Importaciones
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.ModelClient import ModelCliente
from db.models.entities.User import User
from datetime import datetime


#Creación de los blueprint para usar en app.py
admin_app = Blueprint('admin_app', __name__)


#Configuración de rutas y solicitudes
@admin_app.route("/")
@login_required
def inicio():
    return render_template("admin/index.html")

#-------------Rutas de Clientes-------------#
@admin_app.route("/clients")
@login_required
def clients():
    conexion = Conection.conectar()
    clients = ModelCliente.get_all(conexion)
    Conection.desconectar()
    return render_template("admin/clients.html", clients=clients)


@admin_app.route("/clientes/ver/<cedula>")
def verCliente(cedula):
    conexion = Conection.conectar()
    client = ModelCliente.get_cliente_by_cedula(conexion, cedula)
    Conection.desconectar()

    if client:
        return render_template("admin/viewClient.html", client=client)
    else:
        # Manejar el caso en que no se encuentre el cliente
        return "Cliente no encontrado"


@admin_app.route("/clientes/estadísticas")
@login_required
def estadisticas():
    return render_template("admin/estadisticas.html")

@admin_app.route("/cliente/estadistica/ver")
@login_required
def verEstadistica():
    return render_template("admin/verEstadistica.html")

@admin_app.route("/clientes/actualizar")
@login_required
def actualizarCliente():
    return render_template("admin/actualizarCliente.html")

@admin_app.route("/clientes/rutinas")
@login_required
def rutinasCliente():
    return render_template("admin/rutinaCliente.html")

@admin_app.route("/clientes/rutinas/sesiones")
@login_required
def sesionesCliente():
    return render_template("admin/verSesionesRutinaCliente.html")

@admin_app.route("/cliente/sesiones/ver")
@login_required
def verSesionCliente():
    return render_template("admin/verSesion.html")


    #-------------Rutas de Productos-------------#
@admin_app.route("/productos")
@login_required
def productos():
    return render_template("admin/inventario.html")

@admin_app.route("/productos/ver")
@login_required
def verProducto():
    return render_template("admin/verProducto.html")

@admin_app.route("/productos/actualizar")
@login_required
def actualizarProducto():
    return render_template("admin/actualizarProducto.html")




#-------------Rutas de Entrenadores-------------#
@admin_app.route("/entrenadores")
@login_required
def entrenadores():
    return render_template("admin/entrenadores.html")

@admin_app.route("/entrenadores/ver")
@login_required
def verEntrenador():
    return render_template("admin/verEntrenador.html")

@admin_app.route("/entrenadores/actualizar")
@login_required
def actualizarEntrenador():
    return render_template("admin/actualizarEntrenador")



#-------------Rutas de user-------------#
@admin_app.route('/users', methods=["GET", "POST"])
@login_required
def users():
    if request.method == "POST":
        # Obtener los datos del formulario
        documentId = request.form['DocumentId']
        password = request.form['Password']
        confirmPassword = request.form['ConfirmpPassword']
        state = request.form['State']
        role = request.form['Role']
        email = request.form['Email']
        
        # Validación de contraseñas
        if password != confirmPassword:
            return render_template("admin/users.html", error="Las contraseñas no coinciden.")

        # Validación adicional (puedes agregar más validaciones aquí)
        newUser = User(
            id=0,  
            DocumentId=documentId,
            Password=User.generate_password_hash(password), 
            State=state,
            Role=role,
            CreationDate=datetime.now(),
            Email=email
        )

        print(newUser)

        try:
            conexion = Conection.conectar()
            userCreated = ModelUser.insertUser(newUser, conexion)
            
            if userCreated:
                return redirect(url_for('admin_app.users')) 
            else:
                return render_template("admin/users.html", error="Error al crear usuario.")
        except Exception as e:
            print(e)
            return render_template("admin/users.html", error="Error al conectar a la base de datos.")
        finally:
            Conection().desconectar()  

    return render_template("admin/users.html")


@admin_app.route("/usuarios/ver")
@login_required
def verUsuario():
    return render_template("/admin/verUsuario.html")

@admin_app.route("/usuarios/actualizar")
@login_required
def actualizarUsuario():
    return render_template("/admin/actualizarUsuario.html")



#-------------Rutas de facturas-------------#
@admin_app.route("/facturas")
@login_required
def facturas():
    return render_template("admin/factura.html")

@admin_app.route("/facturas/ver")
@login_required
def verFactura():
    return render_template("admin/verFactura.html")

@admin_app.route("/facturas/anular")
@login_required
def anular():
    return render_template("admin/anular.html")  


#-------------Rutas de Inventario-------------#
@admin_app.route("/inventario")
@login_required
def inventario():
    return render_template("admin/inventario.html")

#-------------Rutas de Notificaciones-------------#
@admin_app.route("/notificaciones")
@login_required
def notificaciones():
    return render_template("admin/notificaciones.html")

@admin_app.route("/notificaciones/ver")
@login_required
def verNotificacion():
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
@admin_app.route("/perfil")
@login_required
def perfil():
    return render_template("admin/perfil.html")

#-------------Rutas de Membresias-------------#
@admin_app.route("/menbresias")
@login_required
def membresias():
    return render_template("admin/membresias.html")

@admin_app.route("/menbresias/ver")
@login_required
def verMembresia():
    return render_template("admin/verMembresia.html")

@admin_app.route("/menbresias/actualizar")
@login_required
def actualizarMembresia():
    return render_template("admin/actualizarMembresia.html")

