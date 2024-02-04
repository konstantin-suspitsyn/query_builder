import os

from flask_login import LoginManager

from comrade_wolf.comrade_wolf_flask import ComradeWolfFlask
from comrade_wolf.engine.builder_engine import create_structure_generator

BASE_PATH = r"./db_structure"
JOINS_PATH = os.path.join(BASE_PATH, "joins")
TABLES_PATH = os.path.join(BASE_PATH, "tables")
STANDARD_FIELDS_PATH = os.path.join(BASE_PATH, "standard_filters")


def create_app(test_config=None):
    # create and configure the app
    app = ComradeWolfFlask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import database
    database.init_app(app)

    create_structure_generator(app, JOINS_PATH, TABLES_PATH, STANDARD_FIELDS_PATH)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from comrade_wolf.models.auth_models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.filter_by(id=user_id).first()

    from comrade_wolf.blueprints import auth
    app.register_blueprint(auth.bp)

    from comrade_wolf.blueprints import home
    app.register_blueprint(home.bp)

    return app
