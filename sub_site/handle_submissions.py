import os

from flask import request, redirect, url_for, render_template, \
    send_from_directory
from werkzeug import secure_filename

from sub_site import parent_directory


UPLOAD_FOLDER = os.path.join(parent_directory, 'submissions')
ALLOWED_EXTENSIONS = ['py', 'js', 'html', 'css', 'png', 'jpg', 'jpeg', 'gif',
                      'htm']


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def main(app):
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    @app.route('/submit_assignment', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            uploaded_file = request.files['file']
            if uploaded_file and allowed_file(uploaded_file.filename):
                filename = secure_filename(uploaded_file.filename)
                uploaded_file.save(
                    os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect(url_for('uploads', filename=filename))
        return render_template('submit.html', error="Invalid file")

    @app.route('/uploads/<filename>')
    def specific_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    @app.route('/uploads')
    def uploads():
        return render_template('uploads.html',
                               directory=os.listdir(UPLOAD_FOLDER))