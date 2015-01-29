"""The source of our site's flask app.  All other modules that need a `Flask`
object should import it from here.
"""

import os

from flask import Flask
from flask.ext.bcrypt import Bcrypt

from submission_site.sub_site import parent_directory


# Make sure that flask knows where we're keeping our files
_templates = os.path.join(parent_directory, 'templates')
_static = os.path.join(parent_directory, 'static')
app = Flask(__name__, template_folder=_templates, static_folder=_static)
app.config.from_object('submission_site.config')

# This lets us handle password hashing and salting.
bcrypt_app = Bcrypt(app)
