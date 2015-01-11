import os

from flask import Flask

from flask.ext.bcrypt import Bcrypt
from submission_site.sub_site import parent_directory


_templates = os.path.join(parent_directory, 'templates')
_static = os.path.join(parent_directory, 'static')

app = Flask(__name__, template_folder=_templates, static_folder=_static)
app.config.from_object('submission_site.config')

bcrypt_app = Bcrypt(app)
