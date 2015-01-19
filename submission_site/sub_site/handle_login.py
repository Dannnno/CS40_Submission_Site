"""Functions and classes to handle login and user creation."""

import re

from wtforms import StringField, BooleanField, PasswordField
from wtforms.validators import InputRequired, EqualTo

from flask_login import LoginManager
from flask_wtf import Form

from submission_site.sub_site.handle_database import query_db
from submission_site.sub_site.app import app, bcrypt_app


# Regular expressions to validate usernames and passwords
good_password = re.compile('[\w\d!@#\$%\^&\*\-_=\+]')
good_username = re.compile('[\w\d\-_]')


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'


def _check_login_password(form, field):
    """Validates that the entered password matches the stored password's hash.

    Parameters
    ----------
    form : flask_wtf.Form
        The form that the information is submitted from.
    field : wtforms.PasswordField
        The specific field (in this case the password field) that is being
        validated.

    Returns
    -------
    bool
        Whether or not the hashed value of the entered password is a match for
        the stored password hash.
    """

    username = form.username.data
    password = field.data
    query = "SELECT passwordhash FROM users WHERE username=?"
    args = [username]
    query_results = query_db(query, args)[0][0]
    return bcrypt_app.check_password_hash(query_results, password)


def _check_login_username(_, field):
    """Validates that the username provided matches an existing user.

    Parameters
    ----------
    _ : flask_wtf.Form
        The form the information is submitted from. Required for the API but not
        used here.
    field : wtforms.StringField
        The field that is being validated, in this case the username.

    Returns
    -------
    bool
        Whether or not the provided username is an existing user.
    """

    username = field.data
    query = "SELECT userid FROM users WHERE username=?"
    args = [username]
    query_results = query_db(query, args)[0][0]
    return bool(query_results)


class LoginForm(Form):
    """Form used to login a user.

    Attributes
    ----------
    username : wtforms.StringField
        The username field of the form.
    password : wtforms.PasswordField
        The password field of the form.
    remember : wtforms.BooleanField
        Whether or not the user should be remembered and their login data stored
        in a cookie.
    """

    username = StringField('username',
                           validators=[InputRequired(),
                                       _check_login_username])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         _check_login_password])
    remember = BooleanField('remember', default=False)


def _check_create_password(_, field):
    """Validates that the password being used has no invalid code points.

    Parameters
    ----------
    _ : flask_wtf.Form
        The form the information is submitted from. Required for the API but not
        used here.
    field : wtforms.PasswordField
        The field that is being validated, in this case the password..

    Returns
    -------
    bool
        Whether or not the provided password is acceptable.
    """

    password = field.data
    return all(good_password.match(char) for char in password)


def _check_create_username(_, field):
    """Validates that the username provided is acceptable.

    Parameters
    ----------
    _ : flask_wtf.Form
        The form the information is submitted from. Required for the API but not
        used here.
    field : wtforms.StringField
        The field that is being validated, in this case the username.

    Returns
    -------
    bool
        Whether the username uses only acceptable code points.
    """

    username = field.data
    return all(good_username.match(char) for char in username)


class CreateUserForm(Form):
    """Form used to create a user.

    Attributes
    ----------
    username : wtforms.StringField
        The username field of the form.
    password : wtforms.PasswordField
        The password field of the form.
    confirm : wtforms.PasswordField
        Confirms the password chosen.
    """

    username = StringField('username', validators=[InputRequired(),
                                                   _check_create_username])
    password = PasswordField('password',
                             validators=[InputRequired(),
                                         _check_create_password,
                                         EqualTo('confirm')])
    confirm = PasswordField('confirm', validators=[InputRequired()])
