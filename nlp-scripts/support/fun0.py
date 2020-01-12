import os
import sys
from twilio.rest import Client
from flask import request
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
from .twilio_authentication import authenticator

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

    # Your Account SID from twilio.com/console
    account_sid = authenticator.account_sid
    # Your Auth Token from twilio.com/console
    auth_token  = authenticator.auth_token

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
    sms_text = sms_send("+17785583011", "+12056512211", inputText)
    print("Sent text message")


    result1 =  input_taker(sms_text,'sentiment')
        #result1 =  input_taker(result['text'],result['ana'])
    
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

    return output 
