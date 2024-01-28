import click
import psycopg2
from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = psycopg2.connect(host='localhost',
                                database='query_builder',
                                user="postgres",
                                password="postgres",
                                port=5433)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.autocommit = True
        cursor = db.cursor()
        cursor.execute(f.read().decode('utf8'))
        db.commit()
        cursor.close()


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
