import os, io
from google.cloud import vision_v1
import pandas as pd
import json
import time

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

client = vision_v1.ImageAnnotatorClient()

def detectText(img, isTop):
    with io.open(img, 'rb') as image_file:
        content = image_file.read()

    image = vision_v1.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations

    result = {}
    currentText = ""
    start = True
    del texts[0].description

    if(isTop):
        for text in texts:
            text.description = text.description.replace(':',"")
            text.description = text.description.replace('[',"")
            text.description = text.description.replace(']',")")
            if(start):
                currentKey = "title"
                start = False
            if(text.description == "Hovedkategori"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Mellemkategori"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Underkategori"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Beskrivelse"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Fase"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Faseenhed"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Indikatorenhed"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Indikatorfaktor"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Massefaktor"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Enhedsfaktor"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Datatype"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Kilde"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(text.description == "Udlebsdato"):
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            
            
            currentText = currentText + text.description + " "
        return result
        
    
    for text in texts:
        text.description = text.description.replace('Indikatorer',"")
        text.description = text.description.replace(':',"")
        text.description = text.description.replace('[',"")
        if(text.description == "GWP"):
            currentKey = text.description
            continue
        
        if(text.description == "ODP"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "POCP"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "AP"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "EP"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "ADPE"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "ADPF"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "PERT"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "PENRT"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "RSF"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        if(text.description == "NRSF"):
            result[currentKey] = currentText.strip()
            currentText = ""
            currentKey = text.description
            continue
        currentText = currentText + text.description + " "
    result[currentKey] = currentText.strip()
    return result



results = []

FOLDER_PATH = r'C:\\Users\\jonas\\capacit\\LCA-reader\\VisionAPIDemo\\results'

amountOfResults=3  #1308 == all
for x in range(amountOfResults):
    FILE_NAME = '{}-top.png'.format(x)
    image = os.path.join(FOLDER_PATH, FILE_NAME)
    topResult = detectText(image, True)
    FILE_NAME = '{}-bottom.png'.format(x)
    image = os.path.join(FOLDER_PATH, FILE_NAME)
    bottomResult = detectText(image, False)

    topResult["Indikatorer"] = bottomResult

    results.append(topResult)

print(results)

final = json.dumps(results, indent=2)
with open("result.json", "w") as outfile:
    outfile.write(final)



