from flask import Flask
from flask import request, redirect, render_template
# -*- coding: utf-8 -*-
import os
os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"] = "5898631625714b43b27b6cd31dd0d3ad"
os.environ["COMPUTER_VISION_ENDPOINT"] = "https://westcentralus.api.cognitive.microsoft.com"

from support.fun0 import analyze_img


app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
    dis1 = {'imd': '', 'anr': ''}
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(equest.data['analytic'])

            # Our sequence of support functions
            output = analyze_img(img_file=image, analytic=request.data['analytic']) # function for sending text and receiving response
            dis1['imd'] = output['Image Description']
            dis1['anr'] = output['Analytic Result']

    # return render_template('index.html',data=dis1)
    return render_template('index.html',data=dis1)


if __name__ == __name__:
    app.run(debug=True)

# run this before runninf anything
# export COMPUTER_VISION_SUBSCRIPTION_KEY=5898631625714b43b27b6cd31dd0d3ad
# export COMPUTER_VISION_ENDPOINT=https://westcentralus.api.cognitive.microsoft.com