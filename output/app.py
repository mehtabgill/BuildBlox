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
        return render_template("index.html", output='')
    
    outputList = []

    # Our sequence of support functions
    output = support.fun0.startModule(output)   


    return render_template("index.html", output=output)


if __name__ == __name__:
    #app.run(debug=True)
    app.run(host='localhost', port=6060)
