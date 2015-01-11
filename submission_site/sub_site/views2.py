import os

from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, login_user, \
    current_user

from submission_site.sub_site.app import app, bcrypt_app
from submission_site.sub_site.handle_database2 import query_db, init_db, \
    connect_db, disconnect_db
from submission_site.sub_site.handle_login2 import LoginForm, login_manager, \
    CreateUserForm
from submission_site.sub_site.users import User


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.before_first_request
def init_db_load_users():
    if not os.path.exists(app.config['DATABASE']):
        init_db()
    query = "SELECT userid, username FROM users"
    results = query_db(query)
    for userid, username in results:
        User(userid, username)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))
    if request.method == 'POST':
        return _handle_login(LoginForm())
    return render_template('login.html', form=LoginForm())


def _handle_login(form):
    error = None
    try:
        valid_form = form.validate_on_submit()
    except IndexError:
        # There are no entries in the database
        flash("You need to create an account before you can login")
        return redirect(url_for('create_account'))
    else:
        if valid_form:
            userid = User.get_id_by_name(form.username.data)
            if userid is None:
                error = "No such user {}".format(form.username.data)
            else:
                user = load_user(userid)
                login_user(user, remember=form.remember.data)
                app.config['CURRENT_UPLOAD_FOLDER'] = \
                    os.path.join(app.config['UPLOAD_FOLDER'],
                                 form.username.data)
                flash('login successful')
                return redirect(url_for('index'))
    return render_template('login.html', form=form, error=error)


@app.route('/logout')
def logout():
    if current_user.is_authenticated():
        logout_user()
        app.config['CURRENT_UPLOAD_FOLDER'] = None
        return render_template('logout.html')
    else:
        return redirect(url_for('login'))


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateUserForm()
    if form.validate_on_submit():
        _create_user(form.username.data, form.password.data)
        return redirect(url_for('index'))
    return render_template(
        "create.html", form=form, error="Invalid username or password")


def _create_user(username, password):
    query = "INSERT INTO users (username, passwordhash) VALUES (?, ?)"
    hashed_password = bcrypt_app.generate_password_hash(password)
    args = username, hashed_password
    query_db(query, args)
    user_id = query_db("SELECT userid FROM users WHERE username=?", [username])
    User(user_id, username)


@app.route('/upload_file')
@login_required
def upload():
    return 'success'


@app.route('/add_assignment')
@login_required
def add_assignment():
    return 'success'


@app.route('/view_assignments')
@login_required
def view_assignments():
    return 'success'


@app.route('/gradebook')
@login_required
def gradebook():
    return 'success'


@app.route('/static/<name>')
def serve_static_file(name):
    return app.send_static_file(name)
