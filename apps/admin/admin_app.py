from flask import Blueprint, render_template, jsonify

admin_app = Blueprint('admin_app', __name__)

@admin_app.route("/")
def inicio():
    return render_template("admin/index.html")

