from flask import Blueprint, render_template, current_app

bp = Blueprint('home', __name__, url_prefix='/')


@bp.route('')
def home_page():
    print(current_app.structure_generator.get_tables())
    return render_template("static/home.html")
