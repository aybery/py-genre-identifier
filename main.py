import os

from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'wav', 'mp3'} # only .wav and .mp3 files can be uploaded

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Audio'
app.config['MAX_CONTENT_LENGTH'] = 800 * 1000 * 1000 # 800MB max size


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    return render_template("home.html")


@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    message = ""
    if request.method == 'POST':
        f = request.files['file']
        print(f.filename, "this is the file name :)")

        # checks if the user actually uploaded anything
        if f.filename == "":
            message = "no data??"
        else:
            # Checks if there is a folder called "Audio" to put any files that are uploaded into
            path = os.getcwd() + "\Audio"
            if os.path.isdir(path):
                pass
            else:
                os.mkdir("Audio")

            # gets the complete path of the file and tries to save it
            path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
            if os.path.isfile(path):
                message = "error saving file, it already exists"
            else:
                f.save(path)
                message = "file uploaded successfully"
    return render_template('upload.html', message=message)


@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)

