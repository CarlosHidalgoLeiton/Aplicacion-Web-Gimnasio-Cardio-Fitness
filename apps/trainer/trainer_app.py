from flask import Blueprint, request, url_for, redirect, render_template, flash, jsonify

trainer_app = Blueprint('admin_app', __name__, template_folder='')

@trainer_app.route("/")
def inicio():
    return render_template("/hola")

