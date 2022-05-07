import os, random

import audioread
import librosa
from flask import Flask, render_template, url_for, request, flash, redirect, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

from UploadFile import UploadFile
from Analysis import GetData

from constants import (
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
    MEL_SPEC_LOCATION
)

import matplotlib.pyplot as plt

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
            # this will be retrived using the Analysis class by return 2 things
            filepath = f.getFilepath()

            print("THIS IS PATH",filepath)
            print(f.secure, "SECURE THING")
            analysis = GetData(f.secure, filepath)

            temp, dur = analysis.run()

            dur = round(int(dur), 5)
            tempo = round(int(temp), 4)

            #analysis.getSpec(str(analysis.path))
            getSpecTest()

            os.remove(filepath)
            print(f.save(), "Removed")
            return render_template('home.html', tempo=tempo, dur=dur)

    if error is None:
        return render_template('home.html')
    else:
        return render_template('home.html', error=error)


@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    return render_template('home.html', error='File is too large!'), 413

@app.errorhandler(audioread.exceptions.NoBackendError)
def app_handle_audioread(e):
    return render_template('home.html', error='File corrupted :(')

@app.route("/about")
def about():
    return render_template("about.html")



def getSpecTest(self):
    x = [1, 2, 3, 4, 5, 6, 7]
    y = []

    for i in range(0, 7):
        val = random.randint(1, 20)
        y.append(val)

    plt.plot(x, y)
    plt.xlabel('X Var')
    plt.ylabel('Y Var')

    plt.savefig(MEL_SPEC_LOCATION)
    print("hi this is me working")
    plt.close()

if __name__ == "__main__":
    app.run(debug=True)
