"""Functions to handle accessing and querying databases."""

from contextlib import closing
import os
import sqlite3

from flask import g

from submission_site.sub_site.app import app


def connect_to_database():
    """Connects to the submission site database.

    Returns
    -------
    sqlite3.Connection
        Connection to the database.

    Notes
    -----
    If there is no database file then we have to initialize the database with
    our schema.  If there is a database file but it hasn't been properly
    initialized with the schema then we re-initialize it (this will delete any
    existing values).
    """

    if not os.path.exists(app.config['DATABASE']):
        init_db()
    else:
        try:
            query_db("SELECT * FROM users")
        except sqlite3.OperationalError:
            init_db()
    return _connect_to_database()


def _connect_to_database():
    """Keeps the level of abstraction consistent."""

    return sqlite3.connect(app.config['DATABASE'])


def init_db():
    """Initializes our database."""

    with closing(_connect_to_database()) as db:
        with app.open_resource(app.config['SCHEMA'], mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_request
def connect_db():
    """Connects to the database before every request.

    Notes
    -----
    Uses flask's global, thread-safe variable `g`.
    """

    g.db = connect_to_database()


@app.teardown_request
def disconnect_db(exception):
    """Closes our database after a request or if an exception occurs.

    Parameters
    ----------
    exception : Exception
        The exception that was raised.  Not used.
    """

    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


# Todo: Make this work better with transactions. sqlite3 doesn't handle those
# well by default
def query_db(query, args=()):
    """Queries or edits the database.

    Parameters
    ----------
    query : unicode
        The query statement.  Should only be used with SQL parameters `?` and
        not standard Python string formatters like `%s` or `{}` (those are
        sources of SQL injection).
    args : tuple, optional
        The arguments to the query, if any.

    Returns
    -------
    list
        The list of results from the query.  Can be empty if there are no
        matches or if the query was an insert/update/etc query.
    """

    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    cursor = db.cursor()
    cursor.execute(query, args)
    query_result = cursor.fetchall()
    cursor.close()
    db.commit()
    return query_result
