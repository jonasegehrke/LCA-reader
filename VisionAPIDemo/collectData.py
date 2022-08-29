import json


with open("result.json", "r") as outfile:
    rawData = json.loads(outfile.read())


for data in rawData:
    data["Indikatorer"] = {data["Fase"]: data["Indikatorer"]}

results = []
x = 0
noneFound = False

for data in rawData:
    if len(results) == 0:
        results.append(data)
        continue
    for result in results:
        if data["Ekstern id"] == result["Ekstern id"]:
            result["Indikatorer"][data["Fase"]] = data["Indikatorer"][data["Fase"]]
            noneFound = False
        else:
            noneFound = True
    if noneFound:
        noneFound = False
        results.append(data)
        continue

final = json.dumps(results, indent=2)
with open("collect.json", "w") as outfile:
    outfile.write(final)
