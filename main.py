import os

from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'wav', 'mp3'}  # only .wav and .mp3 files can be uploaded

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Audio'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000  # 16MB max size
app.config['SECRET_KEY'] = 'SA$r"f@l0oPz404{hi!].m&£'


@app.route("/")
def home():
    return render_template("home.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    error = None
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        #ftest = file.filename
        #remove = ftest.rsplit('.', 1)[1].lower()
        #print(file.filename.rsplit('.', 1)[1].lower())
        #fileminus = (ftest.replace(("."+remove), "")).replace(' ', '-').lower()
        #print(fileminus)

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        # Checks if there is a folder called "Audio"
        path = os.getcwd() + "\Audio"
        if os.path.isdir(path):
            pass
        else:
            os.mkdir("Audio")

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            return redirect(url_for('analyse_file', name=filename))
        else:
            error = "This is a file with a wrong extension :("

    return render_template('upload.html', error=error)


@app.route('/uploaded/<name>')
def analyse_file(name):
    path = os.path.join(app.config['UPLOAD_FOLDER'], name)
    return render_template('analysis.html', file=path)
    #return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    # somehow embed the audio file into html so that it can analyse instead of just presenting the file


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
