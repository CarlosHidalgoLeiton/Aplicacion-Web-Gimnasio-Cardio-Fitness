from flask import Blueprint, render_template

landingPage_app = Blueprint('landingPage_app', __name__)

@landingPage_app.route("/")
def index():
    return render_template("index.html")

