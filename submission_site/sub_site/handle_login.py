import re

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, EqualTo

from flask_login import LoginManager
from flask_wtf import Form

from submission_site.sub_site.handle_database import query_db
from submission_site.sub_site.app import app, bcrypt_app


good_password = re.compile('[\w\d!@#\$%\^&\*\-_=\+]')
good_username = re.compile('[\w\d\-_]')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


def _check_login_password(form, field):
    username = form.username.data
    password = field.data
    query = "SELECT passwordhash FROM users WHERE username=?"
    args = [username]
    query_results = query_db(query, args)[0][0]
    return bcrypt_app.check_password_hash(query_results, password)


def _check_login_username(_, field):
    username = field.data
    query = "SELECT userid FROM users WHERE username=?"
    args = [username]
    query_results = query_db(query, args)[0][0]
    return bool(query_results)


class LoginForm(Form):
    username = StringField('username',
                           validators=[InputRequired(),
                                       _check_login_username])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         _check_login_password])
    remember = BooleanField('remember', default=False)


def _check_create_password(_, field):
    password = field.data
    return all(good_password.match(char) for char in password)


def _check_create_username(_, field):
    username = field.data
    return all(good_username.match(char) for char in username)


class CreateUserForm(Form):
    username = StringField('username', validators=[InputRequired(),
                                                   _check_create_username])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         _check_create_password,
                                         EqualTo('confirm')])
    confirm = PasswordField('confirm', validators=[InputRequired()])
