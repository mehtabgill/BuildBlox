from flask import Flask
from flask import request, redirect, render_template
# -*- coding: utf-8 -*-
from twilio.rest import Client
import support.fun0


app = Flask(__name__)

@app.route("/",methods = ['POST', 'GET'])
def index():
    result1 = {'doc':'','language':'','score':'','name':''}

    # Input phase
    if request.method == 'POST':
        result = request.form
        output = result['text']
    else:
        return render_template("index.html", output=None)
    
    outputList = []

    # Our sequence of support functions
    output = support.fun0.startModule(output)  # function for sending text and receiving response
    #output = support.fun1.startModule(output)  # function for sentimental analysis
    ############################

    return render_template("index.html", output=output)

@app.route("/sms", methods=['GET', 'POST'])
def sms_receive():
    # Display sent message
    number = request.form['From']
    msg = request.form["Body"]
    print("Message recieved from: " + number)
    print("Message: " + msg)

    result1 =  support.fun0.input_taker(msg,'sentiment')
    
    resFeeling = 'I am quite happy' 
    
    if result1 is not None and result1['score'] != '':
        if float(result1['score']) >= 0.75: 
            resFeeling = 'I am quite happy' 
        elif float(result1['score'])  >= 0.5: 
            resFeeling = 'I am okay'
        elif float(result1['score'])  >= 0.25: 
            resFeeling = 'I am not okay'
        else: 
            resFeeling = 'I am sad'   
    else:
        result1 = {'doc':'','language':'','score':'','name':''}
        result1['score'] = 'Please enter text'
        resFeeling = 'Invalid'


    print(resFeeling)
    output = result1['score'] 

    return render_template("index.html", ana = output)


if __name__ == __name__:
    app.run(debug=True)