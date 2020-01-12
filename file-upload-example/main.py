from flask import Flask
from flask import request, redirect, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.files:

            image = request.files["image"]

            print(image)


    return render_template("index.html")


if __name__ == __name__:
    app.run(debug=True)