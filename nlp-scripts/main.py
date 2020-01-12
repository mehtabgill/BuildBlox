from flask import Flask
from flask import request, redirect, render_template
# -*- coding: utf-8 -*-
from twilio.twiml.messaging_response import MessagingResponse
import os
import sys
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials
import support.fun0

app = Flask(__name__)


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


@app.route("/",methods = ['POST', 'GET'])
def index():
    result1 = {'doc':'','language':'','score':'','name':''}
    if request.method == 'POST':
        result = request.form
        result1 =  input_taker(result['text'],result['ana'])
        print(result1)
    return render_template("index-original.html", ana = result1)

if __name__ == __name__:
    app.run(debug=True)