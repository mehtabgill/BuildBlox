from flask import Flask
from flask import request, redirect, render_template
import re
import os
# -*- coding: utf-8 -*-
import os
os.environ["COMPUTER_VISION_SUBSCRIPTION_KEY"] = "5898631625714b43b27b6cd31dd0d3ad"
os.environ["COMPUTER_VISION_ENDPOINT"] = "https://westcentralus.api.cognitive.microsoft.com"
RE_CONTENT_RANGE = re.compile(r'^bytes (\d+)-(\d+)/(\d+)$')
RE_ALLOWED_FILEKEYS = re.compile(r'^[a-zA-Z0-9-]+$')

from support.fun0 import analyze_img, stdLib

app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
    dis1 = {'imd': '', 'anr': ''}
    if request.method == "POST":
        if request.files:
            file_ = request.files["image"]
            file_.save('/tmp/'+file_.filename)
            pathi = str('/tmp/'+file_.filename)
            print(pathi)
            # Our sequence of support functions
            output = analyze_img(img_file=pathi, analytic=request.form['analytic'])
            stdLib(img=pathi, info=output )
            dis1['imd'] = output['Image Description']
            dis1['anr'] = output['Analytic Result']

    # return render_template('index.html',data=dis1)
    return render_template('index.html',data=dis1)


if __name__ == __name__:
    app.run(debug=True)

# run this before runninf anything
# export COMPUTER_VISION_SUBSCRIPTION_KEY=5898631625714b43b27b6cd31dd0d3ad
# export COMPUTER_VISION_ENDPOINT=https://westcentralus.api.cognitive.microsoft.com