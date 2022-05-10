import audioread
import random
import os

import matplotlib.pyplot as plt

from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from Analysis import GetData
from UploadFile import UploadFile

from constants import (
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH,
    SECRET_KEY,
    MEL_SPEC_LOCATION
)

# initiates the Flask server
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['SECRET_KEY'] = SECRET_KEY


#  Gets the html file for the "/" directory know as the root directory
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
            #  This will be retrieved using the Analysis class by return 2 things
            filepath = f.getFilepath()

            print("THIS IS PATH", filepath)
            print(f.secure, "SECURE THING")
            analysis = GetData(f.secure, filepath)

            temp, dur = analysis.run()

            dur = round(int(dur), 5)
            tempo = round(int(temp), 4)

            os.remove(filepath)
            print(f.save(), "Removed")
            #  Renders the webpage using home.html located in the template folder
            return render_template('home.html', tempo=tempo, dur=dur)

    if error is None:
        #  Renders the webpage using home.html located in the template folder
        return render_template('home.html')
    else:
        #  Renders the webpage using home.html located in the template folder
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
    #  Renders the webpage using about.html located in the template folder
    #  only if the selected web url is example.com/about/ (example.com is just for demonstration)
    return render_template("about.html")


#  Only starts the flask server if this file is the main file
if __name__ == "__main__":
    app.run(debug=True)


def get_spec_test():
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
