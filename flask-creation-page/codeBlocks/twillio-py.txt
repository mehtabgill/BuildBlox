import os
import sys
from twilio.rest import Client
from flask import request
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from support.authkey import account_sid,auth_token

subscription_key = "5be536ec702a4487aa3c2b636a3cf887"
endpoint = "https://westcentralus.api.cognitive.microsoft.com"


def authenticateClient():
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client


def do_text_analysis(documents, analysis):
    client = authenticateClient()
    result = None 
    if analysis == 'sentiment':
        response = client.sentiment(documents=documents)
        for doc in response.documents:
            result = {"doc": doc.id, "score":doc.score} 
    elif analysis == 'language':
        response = client.detect_language(documents=documents)
        for doc in response.documents:
            result = {"doc": doc.id, "name":doc.detected_languages[0].name}
    elif analysis == 'entity':
        response = client.entities(documents=documents)
        for doc in response.documents:
            entities = []
            for entity in doc.entities:
                ent =  {"name": entity.name, "type": entity.type, "sub-type": entity.sub_type}
                entities.append(ent)
            result = {"doc": doc.id, "entities": entities} 
    elif analysis == 'phrase':
        response = client.key_phrases(documents=documents)
        for doc in response.documents:
            result = {"doc":doc.id, "phrases":doc.key_phrases}
    
    return result



def input_taker(text,ana):
    g = text

    analysis = ana

    doc = {}
    if analysis.lower() != 'language':
        # Sentimental analysis
        doc = [{"id":1, "language":'en', "text":g}]
    else:
        doc = [{"id":1, "text":g}]
    
    return do_text_analysis(documents=doc, analysis=analysis)

def sms_send(destNumber, srcNumber, sendMessage):
    print(str(sendMessage).isdigit())
    if str(sendMessage).isdigit() :
        
        sendMessage = 'There are ' + str(sendMessage) + ' people'
        print(sendMessage)
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to=destNumber, 
        from_=srcNumber,
        body=sendMessage)
    
    return 'I feel great'

def startModule(inputText):
    result1 = {'doc':'','language':'','score':'','name':''}
    if inputText is None:
        inputText = ''

    print("Sending text message")
    #output = sms_send("+17785583011", "+12056512211", inputText)
    output = sms_send("+12368334517", "+12056512211", inputText)
    print("Sent text message")
    

    return output 
