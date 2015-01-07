from contextlib import closing
import os
import sqlite3

from flask import Flask, render_template, request, session, redirect, \
    url_for, g
from flask.ext.login import LoginManager, current_user, login_required, \
    login_user, UserMixin, logout_user
from flask.ext.bcrypt import Bcrypt


app = Flask(__name__)
with open('secret.txt', 'r') as secret_key_file:
    app.secret_key = secret_key_file.read()
bcrypt_app = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

DATABASE = os.path.abspath('./submissions.db')
database_exists = os.path.exists(DATABASE)


def connect_to_database():
    with sqlite3.connect(DATABASE) as conn:
        if database_exists:
            init_db(conn)
        return conn


def init_db(db):
    print 'called'
    with app.open_resource('schema.sql', mode='r') as f:
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


class User(UserMixin):
    users = {}

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.users[self.get_id()] = self


@app.route('/')
def index():
    if current_user.is_authenticated():
        return render_template('index.html')
    else:
        return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return validate_login(request.form['username'],
                              request.form['password'],
                              'remember' in request.form)
    else:
        if not current_user.is_authenticated():
            return render_template('login.html')
        else:
            return render_template('index.html')


def validate_login(username, password, remember=False):
    query = "SELECT username, passwordhash FROM users where username='?'"
    args = (username,)
    print query_db(query, args)
    actual_password = 'hello'
    password_hash = bcrypt_app.generate_password_hash(password)
    correct_password = bcrypt_app.check_password_hash(password_hash,
                                                      actual_password)
    if correct_password:
        pass
    else:
        pass
    return render_template('index.html')


def create_account(username, password):
    hashed_password = bcrypt_app.generate_password_hash(password)
    pass


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.route('/static/<name>')
def serve_static_files(name):
    return app.send_static_file(name)


if __name__ == '__main__':
    app.run(debug=True)