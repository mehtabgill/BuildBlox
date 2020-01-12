# import the Flask class from the flask module
from flask import Flask, render_template, request
from support.textFreq import generateCode

# create the application object
app = Flask(__name__)

# use decorators to link the function to a url
@app.route('/')
def home():
    resPrint = 'twillio'
    resCode = ''
    return render_template('create.html', **locals())  # render a template


@app.route('/submitCreation',methods=['POST','GET'])
def submitCreation():

    topNRankNum = 5
    splitNum = 300
    contractDir = './company0/'

    if request.method == 'POST':
        result = request.form

        moduleList = []
        moduleList.append(result['moduleType0'])


        #moduleList.append(result['moduleType1'])
        #moduleList.append(result['moduleType2'])
    
    
        resList,resPrint = generateCode(moduleList)


    #resText,resRank, mainContract = textFreqCal(topNRankNum,splitNum,contractDir)


    return render_template('create.html', **locals())


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)