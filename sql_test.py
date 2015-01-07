import sqlite3
import os
from contextlib import closing


DATABASE = os.path.abspath('./submissions.db')
database_exists = os.path.exists(DATABASE)


def connect():
    with sqlite3.connect(DATABASE) as conn:
        if not database_exists:
            init_db(conn)
    return conn


def init_db(db):
    print 'called'
    with open('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def query_db(query, args=()):
    with closing(connect()) as db:
        cursor = db.cursor()
        cur = cursor.execute(query, args)
        rv = cur.fetchall()
        db.commit()
        return rv


conn = connect()
print conn
print query_db("SELECT * FROM users")
print query_db("INSERT INTO users (username, passwordhash) VALUES ('dan', 'hello')")