import os


dirname = os.path.dirname(os.path.abspath(__file__))


def get_secret_key(_secret=os.path.join(dirname, 'secret.txt')):
    with open(_secret, 'r') as _secret_key_file:
        return _secret_key_file.read()


SECRET_KEY = get_secret_key()
DATABASE = os.path.join(dirname, 'submissions.db')
SCHEMA = os.path.join(dirname, 'schema.sql')
UPLOAD_FOLDER = os.path.join(dirname, 'submissions')
ALLOWED_EXTENSIONS = ['py', 'js', 'html', 'css', 'png', 'jpg', 'jpeg', 'gif',
                      'htm', 'txt', 'csv', 'pdf', 'json', 'xml', 'xhtml']


