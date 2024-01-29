import functools

import sqlalchemy
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from comrade_wolf.database import init_db, db_session
from comrade_wolf.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        init_db()

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User(username=username, password=generate_password_hash(password))
                db_session.add(user)
                db_session.commit()

            except sqlalchemy.exc.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.route('/login', methods=('GET', 'POST'))
def login():
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
