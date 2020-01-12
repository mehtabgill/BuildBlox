from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
from krakenio import Client 

# Add your Computer Vision subscription key to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
kraken_client = api = Client('ae65a61c61cc2727fb9e76f36ae20286', '6dbcf2c42eac9f2b4213696005b94b978046a9ca')




def analyze_img(img_file, analytic):
    result = "No Objects"

    kraken_data = {'wait': True}
    kraken_img_result = kraken_client.upload(img_file, kraken_data)
    kraken_img_url = None 
    if kraken_img_result.get('success'):
        kraken_img_url = kraken_img_result.get('kraked_url')
    else:
        print(kraken_img_result.get('message'))

    if analytic=='objects':
        response = computervision_client.detect_objects(kraken_img_url)
        for object in response.objects:
            result = "object at location {}, {}, {}, {}".format( \
                object.rectangle.x, object.rectangle.x + object.rectangle.w, \
                object.rectangle.y, object.rectangle.y + object.rectangle.h)
    elif analytic=='brands':
        response = computervision_client.analyze_image(kraken_img_url, ["brands"])
        for brand in response.brands:
            result.append("'{}' brand detected with confidence {:.1f}% at location {}, {}, {}, {}".format( \
                brand.name, brand.confidence * 100, brand.rectangle.x, brand.rectangle.x + brand.rectangle.w, \
                brand.rectangle.y, brand.rectangle.y + brand.rectangle.h))
    elif analytic=='faces':
        response = computervision_client.analyze_image(kraken_img_url, ["faces"])
        for face in response.faces:
            result.append("'{}' of age {} at location {}, {}, {}, {}".format(face.gender, face.age, \
                face.face_rectangle.left, face.face_rectangle.top, \
                face.face_rectangle.left + face.face_rectangle.width, \
                face.face_rectangle.top + face.face_rectangle.height))
    elif analytic=='adult':
        response = computervision_client.analyze_image(kraken_img_url, ["adult"])
        result.append(["Is adult content: {} with confidence {:.2f}".format(detect_adult_results_remote.adult.is_adult_content, detect_adult_results_remote.adult.adult_score * 100),
                        "Has racy content: {} with confidence {:.2f}".format(detect_adult_results_remote.adult.is_racy_content, detect_adult_results_remote.adult.racy_score * 100)])
    elif analytic=='written text':
        response = computervision_client.batch_read_file(kraken_img_url, raw=True)
        operation_location_remote = response.headers["Operation-Location"]
        operation_id = operation_location_remote.split("/")[-1]
        # Call the "GET" API and wait for it to retrieve the results 
        while True:
            get_printed_text_results = computervision_client.get_read_operation_result(operation_id)
            if get_printed_text_results.status not in ['NotStarted', 'Running']:
                break
            time.sleep(1)
        # Print the detected text, line by line
        if get_printed_text_results.status == TextOperationStatusCodes.succeeded:
            for text_result in get_printed_text_results.recognition_results:
                for line in text_result.lines:
                    result = (line.text)
                    # result = (line.bounding_box)
    
    #description

    desc_response = computervision_client.describe_image(kraken_img_url)
    desc_response_result = None
    if (len(desc_response.captions) == 0):
        desc_response_result = "No description detected." 
    else:
        for caption in desc_response.captions:
            desc_response_result = "'{}' with confidence {:.2f}%".format(caption.text, caption.confidence * 100)
    
    final_result = {"Image Description": desc_response_result, "Analytic Result": result}

    return final_result 

