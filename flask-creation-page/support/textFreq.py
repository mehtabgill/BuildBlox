import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from sklearn.pipeline import FeatureUnion
from nltk.corpus import stopwords 
import os
import string

import heapq 



complaintSubPath = 'complaintMain/'


newHTMLPath = './codeBlocks/output/index.html'
newPyPath = './codeBlocks/output/generatedSupport.py'

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

        resCode = '<input type="text" value="twillio"><br>\n'
        moduleResList.append(resCode)


        # Python part

        resCode = '<button>Send text to Twillio</button><br>\n'
        moduleResList.append(resCode)

    elif moduleBlock == 'slack':
        resCode = '<b>Slack</b><br>\n'
        moduleResList.append(resCode)
        resCode = '<input type="text" value="slack"><br>\n'
        moduleResList.append(resCode)
    elif moduleBlock == 'azure':
        resCode = '<b>Azure</b><br>\n'
        moduleResList.append(resCode)
        resCode = '<input type="text" value="azure"><br>\n'
        moduleResList.append(resCode)
    else:
        moduleResList('<b>Error<b>\n')

    return moduleResList



def generateCode(moduleList):



    resList = []
    resCode = ''

    # Initalize with starting HTML
    resList.append(getStartHTMLCode())

    # Insert middle code
    for moduleBlock in moduleList: 
        resList = resList + getModuleCode(moduleBlock.lower())
        resList.append('<b><b>\n\n')


    resList.append(getEndHTMLCode())

    print(resList)


    # Save resList as HTML file
    newHTML_file = open(newHTMLPath ,"w") 
    for codeLine in resList:
        newHTML_file.write(codeLine)

    newHTML_file.close() 


    return resList,moduleBlock







def removeStopWords(wordList):
    return [word for word in wordList if word not in stopwords.words('english')]

# DO NOT USE
def calcCosSimOld(aMat,bVec):
    # Calculate cosine simularity
    a = np.sum(aMat,axis=0)/aMat.shape[0]
    b = bVec.copy()
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

def calcCosSim(a,b):
    # Calculate cosine simularity
    return np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))

def removeStem(sentence):
    ps = PorterStemmer()
    words = word_tokenize(sentence)
    tmpStr = ''
    for w in words:
        tmpStr += ps.stem(w) + ' '
    return tmpStr



def textFreqCal(topNRankNum,splitNum,rootPath):
    contractPath = rootPath + 'termService/' + '0.txt'
    print(rootPath + complaintSubPath)
    contractTxtOrg = open(contractPath, encoding="utf8", errors='ignore').read()
    contractTxt = contractTxtOrg
    contractVec = removeStopWords([removeStem(contractTxt)])

    vec = CountVectorizer()
    contractFreq = vec.fit_transform(contractVec)


    compList = []

    # Used for removing stem from words
    for cFilePath in os.listdir(rootPath + complaintSubPath):
        cFilePath = rootPath + complaintSubPath + cFilePath
        cFileTxt = open(cFilePath, encoding="utf8", errors='ignore').read()

        cFileTxt = removeStem(cFileTxt)
        
        compList.append(cFileTxt + ' ')
        

    compList = [''.join(str(v) for v in compList)]  # We are combining all complaints into one
    complantCnt = CountVectorizer()
    a = complantCnt.fit_transform(compList)

    resPara = []
    resScore = []

    
    #for paragraph in contractTxt.split('\n'):
    for paragraph in [contractTxt[i:i+splitNum] for i in range(0, len(contractTxt), splitNum)]:
        paragraph = paragraph.translate(string.punctuation)


        try:
            vec = CountVectorizer()
            contractFreq = vec.fit_transform([paragraph])
        except:
            continue
        complaintDf = pd.DataFrame(a.toarray(),columns=complantCnt.get_feature_names())
        contractDf = pd.DataFrame(contractFreq.toarray(),columns=vec.get_feature_names())

        combinedDf = pd.concat([complaintDf, contractDf],sort=False).fillna(value=0.0)
        complainVec = combinedDf.iloc[0].values
        contractVec = combinedDf.iloc[1].values

        simRes = calcCosSim(complainVec,contractVec)
        resPara.append(paragraph)
        resScore.append(simRes)




    rankAr = np.asarray(resPara).argsort()[::-1][:topNRankNum]

    heapLi = []


    for ind in rankAr:    
        heapq.heappush(heapLi,[-resScore[ind],ind])
    
    resText = []
    resRank = []

    while len(heapLi) > 0:
        score,ind = heapq.heappop(heapLi)
        score = score*-1
        
        resText.append(resPara[ind])
        resRank.append(score)


    return resText,resRank, contractTxtOrg.split('\n')





