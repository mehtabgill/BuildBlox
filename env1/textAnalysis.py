# -*- coding: utf-8 -*-

import os
import sys
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials


subscription_key = "5be536ec702a4487aa3c2b636a3cf887"
endpoint = "https://westcentralus.api.cognitive.microsoft.com"


def authenticateClient():
    credentials = CognitiveServicesCredentials(subscription_key)
    text_analytics_client = TextAnalyticsClient(
        endpoint=endpoint, credentials=credentials)
    return text_analytics_client

def sentiment():
    
    client = authenticateClient()

    try:
        documents = [
            {"id": "1", "language": "en", "text": "I had the best day of my life."},
            {"id": "2", "language": "en",
                "text": "This was a waste of my time. The speaker put me to sleep."},
            {"id": "3", "language": "es", "text": "No tengo dinero ni nada que dar..."},
            {"id": "4", "language": "it",
                "text": "L'hotel veneziano era meraviglioso. È un bellissimo pezzo di architettura."}
        ]

        response = client.sentiment(documents=documents)
        for document in response.documents:
            print("Document Id: ", document.id, ", Sentiment Score: ",
                  "{:.2f}".format(document.score))

    except Exception as err:
        print("Encountered exception. {}".format(err))
        
# sentiment()


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
    
    print('REsponse is ', result)
    # counter = 0 
    # for doc in response.documents:
    #     result.append({"doc": counter, "Analysis": })
    #     counter+=1


def input_taker():
    print('helo')
    g = input("Docs: ")

    analysis = input("Analysis: ")

    doc = {}
    if analysis.lower() != 'language':
        lang = input("Language: ")
        doc = [{"id":1, "language":lang, "text":g}]
    else:
        doc = [{"id":1, "text":g}]
    
    do_text_analysis(documents=doc, analysis=analysis)

input_taker()


            