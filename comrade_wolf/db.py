import os

import psycopg2
from flask import g


def get_db_connection():
    if 'db' not in g:
        g.db = psycopg2.connect(host='localhost',
                                database='query_builder',
                                user=os.environ['DB_USERNAME'],
                                password=os.environ['DB_PASSWORD'],
                                port=5432)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
