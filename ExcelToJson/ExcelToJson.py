import json
from itertools import chain, islice, tee
from re import T

import pandas as pd


def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)


data = pd.read_excel('tabel-7.xlsx', sheet_name='Bilag 2, tabel 7 renset')

json_data = data.to_json(orient='records')

rawData = json.loads(json_data)


def get_names():
    name_list = []
    for data in rawData:
        name_list.append(data["Navn"])
    return list(dict.fromkeys(name_list))


names_list = get_names()


def sort():
    results = []
    for name in names_list:
        stages = []
        epd = {
            "stages": stages
        }

        for data in rawData:
            if data["Navn"] == name:
                stage = {}
                stage["measures"] = {}
                epd = {
                    "stages": stages,
                    "declaredUnit": {},
                    "epdInfo": {}
                }
                if data["Fase"] == "A1tilA3":
                  stage["stageType"] = 0

                if data["Fase"] == "C3":
                  stage["stageType"] = 15

                if data["Fase"] == "C4":
                  stage["stageType"] = 16

                if data["Fase"] == "D":
                  stage["stageType"] = 17

                stage["stageStatus"] = 2
                stage["measures"] = {"GWP": data["Global Opvarmning"]}
                
                epd["shortName"] = name
                epd["ownerId"] = None
                epd["custom"] = False
                epd["scraped"] = True
                epd["generic"] = True
                epd["expectedLifespan"] = None
                epd["description"] = None
                epd["link"] = ["https://hoeringsportalen.dk/Hearing/Details/66338", "https://prodstoragehoeringspo.blob.core.windows.net/a25cc0f0-2669-42ea-bc8a-f2f84aca8600/Tabel%207%20-%20Generisk%20datagrundlag%202023.pdf"]
                epd["additionalSources"] = [""]
                epd["declaredUnit"]["declaredUnit"] = data["Deklareret enhed"]
                epd["declaredUnit"]["declaredValue"] = data["Deklareret faktor"]
                epd["declaredUnit"]["mass"] = data["Massefaktor"]
                epd["declaredUnit"]["massUnit"] = None
                epd["epdInfo"]["epdSpecificationForm"] = 0
                epd["epdInfo"]["epdProductIndustryType"] = None
                epd["epdInfo"]["issuedAt"] = None
                epd["epdInfo"]["validTo"] = None
                epd["tags"] = [""]
                epd["stages"].append(stage)
        results.append(epd)
    return results


results = sort()


final = json.dumps(results, indent=2)


with open("result-tabel-7.json", "w") as outfile:
    outfile.write(final)
