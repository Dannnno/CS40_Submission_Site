import os

from flask import request, redirect, url_for, render_template
from werkzeug import secure_filename
from flask_login import login_required, current_user

from submission_site.sub_site.app import app
from submission_site.sub_site.handle_database import query_db


def _allowed_file(filename):
    """Checks whether or not the file is of an appropriate type.

    Parameters
    ----------
    filename : unicode
        The name of the file being uploaded.

    Returns
    -------
    bool
        Whether or not the file has the correct extension.
    """

    return ('.' in filename and
            filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS'])


def _upload_file(file_, destination, submission=True):
    """Saves a file to any destination.

    Parameters
    ----------
    file_ : wtforms.File
        The file to be saved.
    destination : unicode
        The filepath to where the file should be saved.
    submission : bool, optional
        Whether or not the file is an assignment submission.
    """

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
    """View for the page to submit an assignment.

    Returns
    -------
    redirect
        If submitting an assignment, is redirected to the appropriate assignment
        page.
    rendered template
        If viewing the page returns the rendered template for the webpage.
    """

    error = None
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = uploaded_file.filename
        if uploaded_file and _allowed_file(filename):
            _upload_file(uploaded_file, app.config['UPLOAD_FOLDER'])
            return redirect(url_for('view_assignment_n',
                                    assignmentid=0,
                                    filename=filename))
        error = "Invalid file"
    return render_template('submit.html', error=error)


@app.route('/assignments/<assignmentid>')
@login_required
def view_assignment_n(assignmentid):
    """View for a given assignment.

    Returns
    -------
    rendered template
        The rendered template for the nth assignment page.
    """

    query = """SELECT filepath, grade_received, time_submitted
               FROM submissions
               WHERE userid=? AND assignmentid=?"""
    args = (current_user.get_id(), assignmentid)
    results = query_db(query, args)
    return render_template('assignment.html', result=results)
