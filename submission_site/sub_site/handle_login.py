import re

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, EqualTo

from flask.ext.login import LoginManager
from flask.ext.wtf import Form

from submission_site.sub_site.handle_database import main as db_main


good_password = re.compile('[\w\d!@#\$%\^&\*\-_=\+]')
good_username = re.compile('[\w\d\-_]')


def main(app, bcrypt_app):
    query_db = db_main(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    def check_login_password(form, field):
        username = form.username.data
        password = field.data
        query = "SELECT passwordhash FROM users WHERE username=?"
        args = [username]
        query_results = query_db(query, args)[0][0]
        return bcrypt_app.check_password_hash(query_results, password)

    def check_login_username(_, field):
        username = field.data
        query = "SELECT userid FROM users WHERE username=?"
        args = [username]
        query_results = bool(query_db(query, args)[0][0])
        return query_results

    class LoginForm(Form):
        username = StringField('username',
                               validators=[InputRequired(),
                                           check_login_username])
        password = PasswordField('password',
                                 validators=[InputRequired(),
                                             check_login_password])
        remember = BooleanField('remember', default=False)

    def check_create_password(_, field):
        password = field.data
        return all(good_password.match(char) for char in password)

    def check_create_username(_, field):
        username = field.data
        return all(good_username.match(char) for char in username)

    class CreateUserForm(Form):
        username = StringField('username', validators=[InputRequired(),
                                                       check_create_username])
        password = PasswordField('password',
                                 validators=[InputRequired(),
                                             check_create_password,
                                             EqualTo('confirm')])
        confirm = PasswordField('confirm', validators=[InputRequired()])

    return login_manager, LoginForm, CreateUserForm
