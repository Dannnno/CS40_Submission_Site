from contextlib import closing
import os
import sqlite3

from flask import g

from submission_site.sub_site.app import app


def _connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    with closing(_connect_to_database()) as db:
        with app.open_resource(app.config['SCHEMA'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def connect_db():
    g.db = _connect_to_database()


@app.teardown_request
def disconnect_db(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


def query_db(query, args=()):
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = _connect_to_database()
    cursor = db.cursor()
    query_result = cursor.execute(query, args)
    db.commit()
    return query_result
