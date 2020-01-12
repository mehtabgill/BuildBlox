from flask import Flask
from flask import request, redirect, render_template
# -*- coding: utf-8 -*-

import support.fun0


app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
    result1 = {'doc':'','language':'','score':'','name':''}

    # Input phase
    if request.method == 'POST':
        result = request.form
        '''
        if 'text' in result.keys()
            output = result['text']
        elif 'image' in result.keys():
            output = result['image']

        '''
        output = result['text']
    else:
        return render_template("index.html", output=None)
    
    outputList = []

    # Our sequence of support functions
    output = support.fun0.startModule(output)  # function for sending text and receiving response
    
    #output = support.fun1.startModule(output)  # function for sentimental analysis

    ############################

    return render_template("index.html", output=output)


if __name__ == __name__:
    app.run(debug=True)