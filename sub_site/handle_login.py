from flask.ext.login import LoginManager, current_user, login_required, \
    login_user, UserMixin, logout_user
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, EqualTo

from sub_site.handle_database import main as db_main


def main(app, bcrypt_app):
    query_db = db_main(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = '/login'

    def check_login_password(form, field):
        username = form.username
        password = field.data
        query = """SELECT passwordhash
                   FROM users
                   WHERE username=?"""
        args = (username,)
        return bcrypt_app.check_password_hash(
            query_db(query, args)[0], password)

    def check_login_username(_, field):
        username = field.data
        query = "SELECT userid FROM users WHERE username=?"
        args = (username,)
        return bool(query_db(query, args)[0])

    class LoginForm(Form):
        username = StringField('username',
                               validators=[InputRequired(),
                                           check_login_username])
        password = PasswordField('password',
                                 validators=[InputRequired(),
                                             check_login_password])
        remember_me = BooleanField('remember_me', default=False)

    def check_create_password(form, field): pass

    def check_create_username(form, field): pass

    class CreateUserForm(Form):
        username = StringField('username', validators=[InputRequired(),
                                                       check_create_username])
        password = PasswordField('password',
                                 validators=[InputRequired(),
                                             check_create_password,
                                             EqualTo('confirm')])
        confirm = PasswordField('confirm', validators=[InputRequired()])

    return login_manager, LoginForm, CreateUserForm
