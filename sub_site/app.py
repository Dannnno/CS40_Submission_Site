import os

from flask import Flask
from flask.ext.bcrypt import Bcrypt

from sub_site import parent_directory


_templates = os.path.join(parent_directory, 'templates')
_static = os.path.join(parent_directory, 'static')
app = Flask(__name__, template_folder=_templates, static_folder=_static)
with open('secret.txt', 'r') as secret_key_file:
    app.secret_key = secret_key_file.read()
bcrypt_app = Bcrypt(app)