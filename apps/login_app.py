from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.entities.User import Usuario


login_app = Blueprint('login_app', __name__)

@login_app.route("/")
def inicio():
    return render_template("login/login.html")

@login_app.route("/recuperarContrasena")
def recuperarContrasena():
    return render_template("login/recuperarContrasena.html")

@login_app.route("/cambiarContrasena")
def cambiarContrasena():
    return render_template("login/cambiarContrasena.html")

@login_app.route("/login", methods=["GET", "POST"])
def inicioSesion():
    if request.method == "POST":
        user = Usuario( 0 ,request.form['cedula'], request.form['contrasena'])
        
        # Establecer una conexión a la base de datos

        try:
            conexion = Conection.conectar()  # Cambiado para crear una instancia
            logged_user = ModelUser.login(user, conexion)
            if logged_user is not None:
                if logged_user != 'Inactivo':
                    login_user(logged_user)
                    return redirect(url_for('admin_app.inicio'))
                else:
                    print('Usuario inactivo')
                    return render_template("login/login.html", error="Invalid credentials") 
            else:
                return render_template("login/login.html", error="Invalid credentials")
        except Exception as e:
            print(e)
        finally:
            Conection().desconectar()  # Cambiado para crear una nueva instancia

    return render_template("login/login.html")