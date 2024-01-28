import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from comrade_wolf.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.cursor().execute(
                    "INSERT INTO query_builder.public.user (username, password) VALUES (%s, %s)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
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
        db = get_db()
        error = None
        with db.cursor() as cursor:
            cursor.execute(
                "SELECT id, username, password FROM query_builder.public.user WHERE username = %s", (username)
            )
            user = cursor.fetchone()
            print(user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user[2], str(password)):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user
            return redirect(url_for('hello'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with get_db().cursor() as cursor:
            print(user_id)
            g.user = cursor.execute(
                "SELECT * FROM query_builder.public.user WHERE id = %s", (user_id[0],)
            ).fetchone()

        print(g.user)


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
