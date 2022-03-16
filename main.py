from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/upload/")
def upload():
    return render_template("upload.html")


@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
