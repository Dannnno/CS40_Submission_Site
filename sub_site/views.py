import sqlite3

from flask import request, render_template, redirect, flash, session, url_for
from flask.ext.login import current_user, login_user, logout_user, \
    login_required

from sub_site.app import app, bcrypt_app
from sub_site.handle_database import main as db_main
from sub_site.handle_login import main as login_main
from sub_site.users import User

query_db = db_main(app)
login_manager, LoginForm = login_main(app, bcrypt_app)


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
    query = """SELECT userid, passwordhash
               FROM users
               WHERE username=?"""
    args = (username,)
    userid, correct_hash = query_db(query, args)[0]
    print bcrypt_app.check_password_hash(correct_hash, password)
    # print login_user(User(userid), remember=remember)
    return render_template('index.html')


@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
    if request.method == 'POST':
        return create_account(request.form['username'],
                              request.form['password'],
                              request.form['confirm_password'])
    return render_template("create.html")


def create_account(username, password, confirm):
    query = "INSERT INTO users (username, passwordhash) VALUES (?, ?)"
    args = username, bcrypt_app.generate_password_hash(password)
    if password == confirm:
        try:
            query_db(query, args)
        except sqlite3.IntegrityError:   # existing username
            return render_template("create.html")
        else:
            return render_template('index.html')
    else:
        return render_template("create.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('/'))


@app.route('/static/<name>')
def serve_static_files(name):
    return app.send_static_file(name)
