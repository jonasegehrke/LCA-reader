import os, io
from google.cloud import vision_v1
import json
from itertools import tee, islice, chain

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)

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
    old = ""
    continue_next = False
    start = True
    del texts[0].description

    if(isTop):
        for previous, text, nxt in previous_and_next(texts):
            text.description = text.description.replace(':',"")
            text.description = text.description.replace('[',"")
            text.description = text.description.replace(']',")")
            text.description = text.description.replace('EOL',"")
            text.description = text.description.replace('|',"")
            if(start):
                currentKey = "Title"
                start = False
            if(text.description == "Hovedkategori"):
                continue_next = False
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description
                continue
            if(continue_next):
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
                if(currentText.strip().startswith("Skriv")):
                    currentText = ""
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
                currentKey = "Udløbsdato"
                continue
            if(text.description == "Ekstern" and nxt.description == "kilde"):
                old = nxt.description
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description + " " + nxt.description
                continue
            if(text.description == "Ekstern" and nxt.description == "id"):
                old = nxt.description
                result[currentKey] = currentText.strip()
                currentText = ""
                currentKey = text.description + " " + nxt.description
                continue
            if(text.description == "Ekstern" and nxt.description == "version"):
                currentText = currentText.replace("O","0")
                old = nxt.description
                result[currentKey] = currentText.strip().replace(" ", "")
                currentText = ""
                currentKey = text.description + " " + nxt.description
                continue
            if(text.description == "Ekstern" and nxt.description == "url"):
                old = nxt.description
                result[currentKey] = currentText.strip().replace(" ", "")
                currentText = ""
                currentKey = text.description + " " + nxt.description
                currentText = "https://oekobaudat.de/OEKOBAU.DAT/resource/processes/{}&version={}".format(result['Ekstern id'], result['Ekstern version'])
                break
            if(old == text.description):
                continue
            if(text.description == "(" and (nxt.description == "A1" or nxt.description == "C3" or nxt.description == "C4" or nxt.description == "D")):
                if(currentKey == "Beskrivelse"):
                    currentText = currentText + text.description + " " 
                    continue
                continue_next = True
                continue
            currentText = currentText + text.description + " "
        result[currentKey] = currentText.strip()
        return result
        
    
    for previous, text, nxt in previous_and_next(texts):
        text.description = text.description.replace('Indikatorer',"")
        text.description = text.description.replace(':',"")
        text.description = text.description.replace('[',"")
        
        if(text.description == "\u00b3"):
            continue
        if(continue_next):
            continue_next = False
            continue
        if(text.description.startswith('PO') and text.description != "POCP"):
            text.description = "PO\u2084\u00b3"
            if(nxt.description == ","):
                continue_next = True

        if(text.description == 'O' and nxt.description == "MJ"):
            text.description = text.description.replace('O',"0")

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

FOLDER_PATH = r'C:\\Users\\jonas\\Capacit\\abc-carbon\\lca-hacker\\VisionAPIDemo\\results'

amountOfResults=100  #1308 == all
for x in range(amountOfResults):
    FILE_NAME = '{}-top.png'.format(x)
    image = os.path.join(FOLDER_PATH, FILE_NAME)
    topResult = detectText(image, True)
    FILE_NAME = '{}-bottom.png'.format(x)
    image = os.path.join(FOLDER_PATH, FILE_NAME)
    bottomResult = detectText(image, False)

    topResult["Indikatorer"] = bottomResult

    results.append(topResult)



final = json.dumps(results, indent=2)
with open("result.json", "w") as outfile:
    outfile.write(final)



