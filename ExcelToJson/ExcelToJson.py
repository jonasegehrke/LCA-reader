import json

import pandas as pd



data = pd.read_excel('tabel-7.xlsx', sheet_name='Bilag 2, tabel 7 renset')

json_data = data.to_json(orient='records')


results = json.loads(json_data)

new_results = []
new_result = {
  "Indikatorer": {}
}
for key in results:
    new_result = {}
    new_result_indikatorer = {}

    new_result["Title"] = key["Navn"]    
    new_result["Fase"] = key["Fase"]    
    new_result["Indikatorfaktor"] = str(key["Deklareret faktor"] )   
    new_result["Indikatorenhed"] = key["Deklareret enhed"]    
    new_result["Massefaktor"] = str(key["Massefaktor"] ) 

    new_result_indikatorer["GWP"] = str(key["Global Opvarmning"]) + "kg CO\u2082 - eq . / m\u00b2"
    new_result["Indikatorer"] = new_result_indikatorer
    new_results.append(new_result)

    

final = json.dumps(new_results, indent=2)



with open("resultTabel7.json", "w") as outfile:
    outfile.write(final)


