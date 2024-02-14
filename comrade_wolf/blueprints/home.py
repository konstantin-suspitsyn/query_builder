from flask import Blueprint, render_template, current_app

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('')
def home_page():
    return render_template("static/home.html")
