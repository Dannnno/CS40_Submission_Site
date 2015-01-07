from contextlib import closing
import os
import sqlite3

from flask import g

from sub_site import parent_directory


def main(app):
    global _database_exists
    DATABASE = os.path.join(parent_directory, 'submissions.db')
    SCHEMA = os.path.join(parent_directory, 'schema.sql')
    _database_exists = os.path.exists(DATABASE)

    def connect_to_database():
        global _database_exists
        with sqlite3.connect(DATABASE) as conn:
            if not _database_exists:
                init_db(conn)
                _database_exists = os.path.exists(DATABASE)
            return conn

    def init_db(db):
        with app.open_resource(SCHEMA, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    def get_db():
        db = getattr(g, 'db', None)
        if db is None:
            db = g.db = connect_to_database()
        return db

    def query_db(query, args=()):
        with closing(get_db()) as db:
            cursor = db.cursor()
            cur = cursor.execute(query, args)
            rv = cur.fetchall()
            db.commit()
            return rv

    @app.before_request
    def before_request():
        g.db = connect_to_database()

    @app.teardown_request
    def teardown_request(exception):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()

    return query_db

