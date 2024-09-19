from flask import Blueprint, render_template, jsonify

login_app = Blueprint('login_app', __name__)

@login_app.route("/")
def inicio():
    return render_template("/hola")

