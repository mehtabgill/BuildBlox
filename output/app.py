from flask import Flask
from flask import request, redirect, render_template
# -*- coding: utf-8 -*-

import support.fun0
import support.fun1


app = Flask(__name__)
app.static_folder = 'static'

@app.route("/",methods = ['POST', 'GET'])
def index():
    result1 = {'doc':'','language':'','score':'','name':''}
    output = 'None'
    # Input phase
    if request.method == 'POST':
        result = request.form
        
        if 'text' in result.keys():
            output = result['text']
        elif 'image' in result.keys():
            output = result['image']
        print('This is output: ', output)
        # Our sequence of support functions
        output = support.fun0.startModule(output) 
        print('Output after first wave: ', output)
        output = support.fun1.startModule(output)
        output = ''
    else:
        return render_template("index.html", output='')
    
    outputList = []

     
    print("***** THIS IS OUR RESULT MESSAGE ********")
    print(output)

    return render_template("index.html", output=output)

from twilio.twiml.messaging_response import MessagingResponse, Message
@app.route("/sms", methods=['GET', 'POST'])
def sms_receive():
    # Display sent message
    number = request.form['From']
    msg = request.form["Body"]
    print("Message recieved from: " + number)
    print("Message: " + msg)

    try: 
        result1 =  support.fun0.input_taker(msg,'sentiment')
    except:
        result1 =  support.fun1.input_taker(msg,'sentiment')
    
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


    
    output = result1['score'] 
    print('output: ',output)

    response = MessagingResponse()
    msgStr = 'The person you are talking with has a positivity of ' + str(output)
    response.message(msgStr)

    print(str(response))
    return str(response)

if __name__ == __name__:
    #app.run(debug=True)
    app.run(host='localhost', port=6060)
