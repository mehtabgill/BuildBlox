import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.pipeline import FeatureUnion
from nltk.corpus import stopwords 
import os
import string


# generate index.html
# generate fun0.py, fun1.py, fun2.py

complaintSubPath = 'complaintMain/'

'''
newHTMLPath = './codeBlocks/output/index.html'
newPyPath = './codeBlocks/output/generatedSupport.py'
'''
newHTMLPath = '../output/templates/index.html'


def readCodeFromFile(filePath):
    with open(filePath, "r", encoding='utf-8') as f:
        outCode= f.read()
    return outCode

def getStartHTMLCode():
    with open("./codeBlocks/startHTML.txt", "r", encoding='utf-8') as f:
        startHTML= f.read()
    return startHTML

def getEndHTMLCode():
    with open("./codeBlocks/endHTML.txt", "r", encoding='utf-8') as f:
        endHTML= f.read()
    return endHTML

def getModuleCode(moduleBlock):
    # Returns a list of code
    moduleResList = []
    modulePyList = []

    if moduleBlock == 'twillio':
        # HTML part
        resCode = '<b>Twillio feature</b><br>\n'
        moduleResList.append(resCode)

        # Web app
        resCode = readCodeFromFile('./codeBlocks/twillio-html.txt')
        moduleResList.append(resCode)

        # Python app
        resPyCode = readCodeFromFile('./codeBlocks/twillio-py.txt')
        modulePyList.append(resPyCode)

    elif moduleBlock == 'slack':
        resCode = '<b>Slack</b><br>\n'
        moduleResList.append(resCode)
        resCode = '<input type="text" value="slack"><br>\n'
        moduleResList.append(resCode)

    elif moduleBlock == 'senemental':
        # Web app
        resCode = readCodeFromFile('./codeBlocks/sentiment-analysis-html.txt')
        moduleResList.append(resCode)

        # Python app
        resPyCode = readCodeFromFile('./codeBlocks/sentimental-analysis-py.txt')
        modulePyList.append(resPyCode)

    elif moduleBlock == 'azure':
        resCode = '<b>Azure</b><br>\n'
        moduleResList.append(resCode)
        resCode = '<input type="text" value="azure"><br>\n'
        moduleResList.append(resCode)
    else:
        moduleResList('<b>Error<b>\n')

    return moduleResList,modulePyList



def generateCode(moduleList):



    resList = []
    resPyList = []
    resCode = ''

    # Initalize with starting HTML
    resList.append(getStartHTMLCode())

    # Insert middle code
    for i,moduleBlock in enumerate(moduleList): 
        moduleResList,modulePyList = getModuleCode(moduleBlock.lower())
        resList = resList + moduleResList 

        resList.append('<b><b>\n\n')

        resPyList = resPyList+ modulePyList

    resList.append(getEndHTMLCode())

    print(resList)


    # Save resList as HTML file
    newHTML_file = open(newHTMLPath ,"w") 
    for codeLine in resList:
        newHTML_file.write(codeLine)

    # Save results as a Python file
    for i,pyBlock in enumerate(resPyList):
        newPyPath = '../output/support/fun'+str(i)+'.py'
        pyFun_file = open(newPyPath,"w")
        pyFun_file.write(pyBlock)
        pyFun_file.close()
    newHTML_file.close() 


    return resList,moduleBlock




