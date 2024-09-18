from flask import Blueprint, request, url_for, redirect, render_template, flash, jsonify

login_app = Blueprint('admin_app', __name__, template_folder='')

@login_app.route("/")
def inicio():
    return render_template("/hola")

