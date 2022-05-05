import os, random

from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from UploadFile import UploadFile
##from AnalyseFile import Predict

from constants import (
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH
)

# initiates the Flask server
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':

        file = request.files['file']
        secure = secure_filename(file.filename)

        f = UploadFile(file, secure)
        f.use_file()

        error = f.exception

        if error is None:

            prediction = "hello"

            os.remove(f.save())
            print(f.save(), "Removed")
            return render_template('home.html', genre=prediction)

    if error == None:
        return render_template('home.html')
    else:
        return render_template('home.html', error=error)


@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    return render_template('home.html', error='File is too large!'), 413


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
