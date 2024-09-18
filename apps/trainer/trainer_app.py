from flask import Blueprint, render_template, jsonify

trainer_app = Blueprint('trainer_app', __name__)

@trainer_app.route("/")
def inicio():
    return render_template("/hola")

