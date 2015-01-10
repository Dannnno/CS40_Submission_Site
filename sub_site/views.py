import os

from flask import render_template, redirect, url_for, g
from flask.ext.login import current_user, login_user, logout_user, \
    login_required

from sub_site.app import app, bcrypt_app
from sub_site.handle_database import main as db_main
from sub_site.handle_login import main as login_main
from sub_site.handle_submissions import main as submission_main, UPLOAD_FOLDER
from sub_site.users import User


submission_main(app)
query_db = db_main(app)
login_manager, LoginForm, CreateUserForm = login_main(app, bcrypt_app)


@login_manager.user_loader
def load_user(userid):
    return User.get(userid)


@app.before_first_request
def load_all_users():
    query = "SELECT * FROM users"
    results = query_db(query)
    for userid, username, _ in results:
        User(userid, username)


@app.before_request
def before_request():
    g.user = current_user


@app.route('/')
@app.route('/index')
def index():
    if current_user.is_authenticated():
        return render_template('index.html')
    else:
        return redirect(url_for('login'))


@app.route('/success')
def success():
    return 'working'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    try:
        valid_form = form.validate_on_submit()
    except IndexError:
        return redirect(url_for('new_account'))
    else:
        if valid_form:
            userid = query_db("SELECT userid FROM users WHERE username=?",
                              [form.username.data])[0][0]
            user = load_user(userid)
            if user is None:
                error = "No such user"
            else:
                login_user(user)
                app.config['UPLOAD_FOLDER'] = os.path.join(
                    UPLOAD_FOLDER, current_user.username)
                return redirect(url_for('success'))
    return render_template('login.html', form=form, error=error)


@app.route('/new_account', methods=['GET', 'POST'])
def new_account():
    form = CreateUserForm()
    if form.validate_on_submit():
        print form, vars(form)
        return redirect(url_for('success'))
    return render_template(
        "create.html", form=form, error="Invalid username or password")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/static/<name>')
def serve_static_files(name):
    return app.send_static_file(name)
