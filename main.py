import audioread
import os

from flask import Flask, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

from Analysis import GetData
from UploadFile import UploadFile

from constants import (
    UPLOAD_FOLDER,
    MAX_CONTENT_LENGTH,
    SECRET_KEY
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
    tempo = None
    dur = None
    if request.method == 'POST':

        #  Collecting the file data
        file = request.files['file']
        secure = secure_filename(file.filename)
        #   Gets the file path
        filepath = UPLOAD_FOLDER + '\\' + secure

        #  Calls the class from UploadFile.py and sends the two variables declared above
        f = UploadFile(file, secure)
        #  Calls the use_file method so that the file starts to be handled
        f.use_file()

        #  The error is fetched from the UploadFile.py
        error = f.exception

        if error is None:
            #  Starts the analysis class
            analysis = GetData(f.secure, filepath)

            #  Gets the temp and dur value from run()
            temp, dur = analysis.run()

            #  Rounding the values to easier to read numbers
            dur = round(int(dur), 5)
            tempo = round(int(temp), 4)

            #  Deletes the file after use
            os.remove(filepath)
            print(f.save(), "Removed")

    #  Renders the webpage using home.html located in the template folder
    return render_template('home.html', tempo=tempo, dur=dur, error=error)


#  Handles EntityTooLarge Error
@app.errorhandler(413)
@app.errorhandler(RequestEntityTooLarge)
def app_handle_413(e):
    return render_template('home.html', error='File is too large!'), 413


#  Handles NoBackendError Error
@app.errorhandler(audioread.exceptions.NoBackendError)
def app_handle_audioread(e):
    return render_template('home.html', error='File corrupted :(')


#  Gets the html file for the "/about"
@app.route("/about")
def about():
    #  Renders the webpage using about.html located in the template folder
    #  only if the selected web url is example.com/about/ (example.com is just for demonstration)
    return render_template("about.html")


#  Only starts the flask server if this file is the main file
if __name__ == "__main__":
    app.run(debug=True)
