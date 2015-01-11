from contextlib import closing
import os
import sqlite3

from sub_site import parent_directory


DATABASE = os.path.join(parent_directory, 'submissions.db')
SCHEMA = os.path.join(parent_directory, 'schema.sql')
_database_exists = os.path.exists(DATABASE)


def main(app):
    def connect_to_database():
        global _database_exists
        with sqlite3.connect(DATABASE) as conn:
            if not _database_exists:
                init_db(conn)
            _database_exists = True
            return conn

    def init_db(db):
        with app.open_resource(SCHEMA, mode='r') as f:
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

