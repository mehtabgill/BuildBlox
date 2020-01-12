# import the Flask class from the flask module
from flask import Flask, render_template, request
from support.textFreq import textFreqCal, generateCode

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
    '''
        if result['moduleType0'] == 'slack':
            splitNum = 300
            contractDir = './slack/'

            moduleBlock = 'slack'

        elif result['moduleType0'] == 'azure':
            splitNum = 400
            contractDir = './azure/'

            moduleBlock = 'azure'
        else:
            # We are doing hotel
            splitNum = 400
            contractDir = './twillio/'

            moduleBlock = 'twillio'
    
    else:
        topNRankNum  = request.args.get('top',None)

    if topNRankNum is None:
        topNRankNum = 5
    '''
    moduleList = []
    moduleList.append(result['moduleType0'])
    moduleList.append(result['moduleType1'])
    moduleList.append(result['moduleType2'])
    
    
    resList,resPrint = generateCode(moduleList)


    #resText,resRank, mainContract = textFreqCal(topNRankNum,splitNum,contractDir)


    return render_template('create.html', **locals())


# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)