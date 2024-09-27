from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user
from db.conection import Conection
from db.models.ModelUser import ModelUser
from db.models.entities.User import User


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
def login():
    if request.method == "POST":
        user = User( 0 ,request.form['DocumentId'], request.form['Password'])
        # Establecer una conexión a la base de datos
        try:
            conexion = Conection.conectar()  # Cambiado para crear una instancia
            logged_user = ModelUser.login(user, conexion)
            if logged_user is not None:
                if logged_user != 'Inactivo':
                    login_user(logged_user)
                    if logged_user.Role == "Admin":
                        return redirect(url_for('admin_app.inicio'))
                    elif logged_user.Role == "Client":
                        return redirect(url_for('client_app.inicio'))
                    elif logged_user.Role == 'Trainer':
                        return redirect(url_for('trainer_app.inicio'))
                    else:
                        return render_template("login/login.html")
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

@login_app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login_app.login'))