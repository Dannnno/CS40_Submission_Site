from contextlib import closing
import os
import sqlite3

from submission_site.sub_site import parent_directory


DATABASE = os.path.join(parent_directory, 'submissions.db')
SCHEMA = os.path.join(parent_directory, 'schema.sql')


def main(app):
    app.config['DATABASE'] = DATABASE
    app.config['SCHEMA'] = SCHEMA

    def database_exists():
        return os.path.exists(app.config['DATABASE'])

    def connect_to_database():
        with sqlite3.connect(app.config['DATABASE']) as conn:
            if not database_exists():
                init_db(conn)
            return conn

    def init_db(db):
        with app.open_resource(app.config['SCHEMA'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    def query_db(query, args=()):
        with closing(connect_to_database()) as db:
            cursor = db.cursor()
            cur = cursor.execute(query, args)
            rv = cur.fetchall()
            db.commit()
            return rv

    return query_db

