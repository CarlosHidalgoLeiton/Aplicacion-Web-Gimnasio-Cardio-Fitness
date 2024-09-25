from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from flask import current_app
from ..db.models.ModelUser import ModelUser
from ..db.models.entities.User import Usuario

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


@login_app.route("/login", methods = ["POST"])
def inicioSesion():
    if request.method == "POST":
        user = Usuario(0, request.form['cedula'], request.form['contrasena'])
        logged_user = ModelUser.login(current_app.extensions['db'], user)
        if logged_user != None:
            if logged_user.Contrasena:
                login_user(logged_user)
                return redirect(url_for('admin_app.inicio'))
            else:
                return render_template("login/login.html")
        else:
            return render_template("login/login.html")
    else:
        return render_template("login/login.html")
