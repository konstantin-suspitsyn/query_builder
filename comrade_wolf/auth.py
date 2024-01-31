import functools
from datetime import datetime

import sqlalchemy
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from comrade_wolf.database import init_db, db_session
from comrade_wolf.models import User, ActivationCode
from comrade_wolf.utilities.util_enums import FlashType
from comrade_wolf.utilities.utilities import generate_random_string

bp = Blueprint('auth', __name__, url_prefix='/auth')


def check_if_user_exists(email):
    """
    Checks if User exists
    If user not active, code will be send again
    If user active will return login
    :param email: User email
    :return:
    """
    user = User.query.filter_by(email=email).first()
    if user is None:
        return

    if user.is_active is False:
        message: str = "Пользователь с email {} уже был создан, но не был активирован".format(email)
        # TODO: Add send message with code to email
        flash(message, FlashType.info.value)

    if user.is_active is True:
        message: str = "Пользователь с email {} уже был создан".format(email)
        return redirect(url_for('auth.login', message=message))


@bp.route('/register', methods=('GET', 'POST'))
def register(message: str = None, error: str = None):
    flashing(error, message)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]
        error = None

        init_db()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not email:
            error = 'Email is required.'

        check_if_user_exists(email)

        if error is None:
            try:
                user = User(username=username, password=generate_password_hash(password), email=email)
                db_session.add(user)
                db_session.flush()
                db_session.refresh(user)

                activation_code_string = generate_random_string(64)
                activation_code = ActivationCode(user_id=user.id, activation_code=activation_code_string)
                db_session.add(activation_code)
                db_session.flush()

                # TODO: Add send message with code to email
                print(activation_code)

                db_session.commit()

            except sqlalchemy.exc.IntegrityError:
                error = f"User {username} is already registered."
        else:
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@bp.route('/login', methods=('GET', 'POST'))
def login(message: str = None, error: str = None):
    flashing(error, message)

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        init_db()
        error = None

        user = User.query.filter_by(username=username).first()
        print(user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.get_password(), str(password)):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user.get_id()
            return redirect(url_for('hello'))

        flash(error)

    return render_template('auth/login.html')


def flashing(error=None, message=None):
    if message is not None:
        flash(message, FlashType.info.value)
    if error is not None:
        flash(error, FlashType.warning.value)


@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    if request.method == 'POST':
        pass

    return render_template('auth/forgot_password.html')


@bp.route('/activate', methods=['GET'])
def activate_user():
    code = request.args.get("code")

    init_db()

    activation_code = ActivationCode.query.filter_by(activation_code=code).first()
    if activation_code is None:
        flash("Код активации не найден", FlashType.warning.value)
        return render_template('auth/login.html')

    activation_code.is_active = True
    activation_code.updated_at = datetime.now()

    user = User.query.filter_by(id=activation_code.user_id).first()
    user.is_active = True
    user.updated_at = datetime.now()

    db_session.commit()

    flash("Пользователь активирован", FlashType.success.value)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:

        user = User.query.filter_by(id=user_id).first()

        g.user = user


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
