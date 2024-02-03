import functools
from datetime import datetime

import sqlalchemy
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from comrade_wolf.database import init_db, db_session
from comrade_wolf.models.auth_models import User, ActivationCode, ChangePasswordCode
from comrade_wolf.utilities.util_enums import FlashType
from comrade_wolf.utilities.utilities import generate_random_string

SHOULD_ENTER = "Необходимо заполнить {}"

ACTIVATE_USER = "Пользователь создан. Проверьте электронную почту для активации"

USER_NOT_FOUND_OR_PASSWORD_WRONG = "Пользователь не не найден или пароль некорректный"

bp = Blueprint('auth', __name__, url_prefix='/auth')


def error_if_user_exists(email: str, username: str) -> str | None:
    """
    Checks if User exists
    :param username:
    :param email: User email
    :return:
    """
    user = User.query.filter_by(email=email).first()

    if user is None:
        user = User.query.filter_by(username=username).first()
        print(user)
    else:
        return "Пользователь с почтой {} уже зарегистрирован".format(email)

    if user is not None:
        return "Пользователь с именем {} уже зарегистрирован".format(username)

    return None


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    Register user
    :return:
    """

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        email = request.form["email"]

        # Any possible error
        error: str | None = None

        error_message = SHOULD_ENTER

        init_db()

        if not username:
            error = error_message.format("имя пользователя")
        elif not password:
            error = error_message.format("пароль")
        elif not email:
            error = error_message.format("электронную почту")
        else:
            error = error_if_user_exists(email, username)

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

                db_session.commit()

                return redirect(url_for("auth.login"))

            except sqlalchemy.exc.IntegrityError:
                error = f"User {username} is already registered."
                flash(error, category=FlashType.warning.value)

        else:
            flash(error, category=FlashType.warning.value)

    return render_template("auth/register.html")


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    Login user
    :return:
    """

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Any possible error
        error: str | None = None

        error_message = "Необходимо заполнить {}"

        init_db()

        if not password:
            error = error_message.format("пароль")
        elif not email:
            error = error_message.format("электронную почту")

        init_db()

        user = User.query.filter_by(email=email).first()

        if (user is None) or (not check_password_hash(user.get_password(), str(password))):
            error = USER_NOT_FOUND_OR_PASSWORD_WRONG

        if error is None:
            session.clear()
            # TODO: remember to form
            login_user(user, remember=True)
            return redirect(url_for('hello'))

        flash(error, category=FlashType.warning.value)

    return render_template('auth/login.html')


def flashing(error=None, message=None):
    if message is not None:
        flash(message, FlashType.info.value)
    if error is not None:
        flash(error, FlashType.warning.value)


@bp.route('/forgot-password', methods=('GET', 'POST'))
def forgot_password():
    """
    Forgot password using email
    :return:
    """

    # TODO: Check if code exists for user. Send existing code if not expired if expired, create new

    if request.method == 'POST':

        email = request.form["email"]

        error: str | None = None

        if error is None:
            error = SHOULD_ENTER.format("email")

        user: User | None = User.query.filter_by(email=email)

        if user is None and error is not None:
            error = "Пользователь не найден"

        if error is None:
            init_db()
            change_code_string = generate_random_string(256)
            change_password_code = ChangePasswordCode(activation_code=change_code_string, user_id=user.id)

            db_session.add(change_password_code)
            db_session.flush()

            # TODO: send email

            db_session.commit()

    return render_template('auth/forgot_password.html')


@bp.route('/set-password', methods=('GET', 'POST'))
def set_new_forgotten_password():
    error: str | None = None

    code = request.args.get("code")

    if code is None:
        error = "Код восстановления не найден"

    if request.method == 'POST':

        password = request.form["password"]

        if password is None:
            error = "Введи пароль"

        forgotten_password_code = ChangePasswordCode.query.filter_by(activation_code=code, is_active=True).first()

        if forgotten_password_code is None:
            error = "Код восстановления не найден"

        if error is None:

            if forgotten_password_code.expiration_date <= datetime.now():
                error = "Срок годности кода закончился. Запросите новый код"

        init_db()
        forgotten_password_code.is_active = False
        forgotten_password_code.updated_at = datetime.now()
        db_session.add(forgotten_password_code)

        if error is None:
            user = User.query.filter_by(id=forgotten_password_code.user_id).first()
            user.password = generate_password_hash(password)

        db_session.commit()

    if error is not None:
        flash(error, category=FlashType.warning.value)

    return render_template('auth/new_forgotten_password.html')


@bp.route('/activate', methods=['GET'])
def activate_user():
    """
    Activate user using code from email
    :return:
    """
    code = request.args.get("code")

    current_error: str | None = None

    init_db()

    activation_code = ActivationCode.query.filter_by(activation_code=code, is_active=True).first()
    if activation_code is None or code is None:
        current_error = "Код активации не найден"

    user = None

    if activation_code is not None:
        user = User.query.filter_by(id=activation_code.user_id).first()

    if current_error is None and user is None:
        current_error = "Пользователь не найден"

    if current_error is None:

        activation_code.is_active = False
        activation_code.updated_at = datetime.now()

        user.is_active = True
        user.updated_at = datetime.now()

        db_session.commit()

        flash("Пользователь активирован", FlashType.success.value)

    else:
        flash(current_error, FlashType.warning.value)

    return render_template('auth/activate_user.html')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('hello'))
