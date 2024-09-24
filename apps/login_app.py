from flask import Blueprint, render_template, jsonify

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