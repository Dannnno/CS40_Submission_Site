import os

from flask import request, redirect, url_for, render_template, \
    send_from_directory
from werkzeug import secure_filename
from flask.ext.login import login_required, current_user

from submission_site.sub_site import parent_directory
from submission_site.sub_site.handle_database import main as db_main


UPLOAD_FOLDER = os.path.join(parent_directory, 'submissions')
ALLOWED_EXTENSIONS = ['py', 'js', 'html', 'css', 'png', 'jpg', 'jpeg', 'gif',
                      'htm']


def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def main(app):
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    query_db = db_main(app)

    @app.route('/submit_assignment', methods=['GET', 'POST'])
    @login_required
    def upload_file():
        if request.method == 'POST':
            uploaded_file = request.files['file']
            filename = uploaded_file.filename
            if uploaded_file and _allowed_file(filename):
                _save_file(uploaded_file)
                return redirect(url_for('uploads', filename=filename))
        return render_template('submit.html', error="Invalid file")

    def _save_file(file_):
        filename = secure_filename(file_.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_.save(filepath)
        query = "INSERT INTO submissions (filepath) VALUES (?)"
        args = (filepath,)
        query_db(query, args)

    @app.route('/uploads/<filename>')
    @login_required
    def specific_file(filename):
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/uploads')
    @login_required
    def uploads():
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.mkdir(app.config['UPLOAD_FOLDER'])
        query = """SELECT (filepath, grade_received, time_submitted)
                   FROM submissions
                   WHERE userid=?"""
        args = (current_user.get_id(),)
        results=query_db(query, args)
        return render_template('uploads.html', uploaded_files=results)

    @app.route('/assignment<number>')
    def submit_assignment_n(number):
        pass
