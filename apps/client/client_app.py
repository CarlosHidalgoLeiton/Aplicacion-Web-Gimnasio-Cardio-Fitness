from flask import Blueprint, render_template, jsonify

client_app = Blueprint('client_app', __name__)

@client_app.route("/")
def inicio():
    return render_template("/hola")

