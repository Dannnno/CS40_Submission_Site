import os

from flask import request, redirect, url_for, render_template, \
    send_from_directory
from werkzeug import secure_filename
from flask_login import login_required, current_user

from submission_site.sub_site.app import app
from submission_site.sub_site.handle_database import query_db


def _allowed_file(filename):
    return ('.' in filename and
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'])


def _upload_file(file_, destination, submission=True):
    filename = secure_filename(file_.filename)
    filepath = os.path.join(destination, filename)
    file_.save(filepath)
    if submission:
        query = "INSERT INTO submissions (filepath) VALUES (?)"
        args = (filepath,)
        _ = query_db(query, args)


@app.route('/submit_assignment', methods=['GET', 'POST'])
@login_required
def upload_file():
    error = None
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = uploaded_file.filename
        if uploaded_file and _allowed_file(filename):
            _upload_file(uploaded_file, app.config['UPLOAD_FOLDER'])
            return redirect(url_for('view_assignment_n', assignmentid=0, filename=filename))
        error = "Invalid file"
    return render_template('submit.html', error=error)


@app.route('/assignments/<assignmentid>')
@login_required
def view_assignment_n(assignmentid):
    query = """SELECT filepath, grade_received, time_submitted
               FROM submissions
               WHERE userid=? AND assignmentid=?"""
    args = (current_user.get_id(), assignmentid)
    results = query_db(query, args)
    return render_template('assignment.html', result=results)
