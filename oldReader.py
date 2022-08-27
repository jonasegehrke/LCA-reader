import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import re
import csv
import json
import time

def predict(model, processor, path, isTop): 
    emission_qs = []

    if(isTop):
        emission_qs = [
            "headline",
        ]
    else:
        emission_qs = [
            "GWP",
            "ODP",
            "POCP",
            "AP",
            "EP",
            "ADPE",
            "ADPF",
            "PERT",
            "PENRT",
            "RSF",
            "NRSF",
        ]

    

    _img = Image.open(path)
    pixel_values = processor(_img.convert('RGB'), return_tensors="pt").pixel_values

    predicted_values = {}

    currentUnit = ""

    for q in emission_qs:
        user_input = ""
        if(isTop):
            user_input = f'What is the {q}?'
        else:
            user_input = f'What is {q}?'

        print(user_input)
        task_prompt = "<s_docvqa><s_question>{user_input}</s_question><s_answer>"
        prompt = task_prompt.replace("{user_input}", user_input)

        decoder_input_ids = processor.tokenizer(prompt, add_special_tokens=False, return_tensors="pt")["input_ids"]

        device = "cuda" if torch.cuda.is_available() else "cpu"

        model.to(device)

        outputs = model.generate(pixel_values.to(device),
                                    decoder_input_ids=decoder_input_ids.to(device),
                                    max_length=model.decoder.config.max_position_embeddings,
                                    early_stopping=True,
                                    pad_token_id=processor.tokenizer.pad_token_id,
                                    eos_token_id=processor.tokenizer.eos_token_id,
                                    use_cache=True,
                                    num_beams=1,
                                    bad_words_ids=[[processor.tokenizer.unk_token_id]],
                                    return_dict_in_generate=True,
                                    output_scores=True)


        seq = processor.batch_decode(outputs.sequences)[0]
        seq = seq.replace(processor.tokenizer.eos_token, "").replace(processor.tokenizer.pad_token, "")
        seq = re.sub(r"<.*?>", "", seq, count=1).strip()  # remove first task start token  
        
        value = seq.replace('<s_question> ', '')
        value = value.replace(user_input, '')
        value = value.replace('</s_question><s_answer> ', '')
        value = value.replace('</s_answer>', '')
        value = value.replace(',', ".")

        #find the unit used for current emission -> until found, then stop and do the same for rest
        if(len(currentUnit) > 0):
            if(x.find('/ m2') >= 0):
                currentUnit = "/ m2"

            if(x.find('/ m3') >= 0):
                currentUnit = "/ m3"

            if(x.find('/ kg') >= 0):
                currentUnit = "/ kg"

            if(x.find('/ stk') >= 0):
                focurrentUnitund = "/ stk"
        
        if(not isTop):
            value = removeUnits(value)

        #remove all unit data
        #append correct unit data depending on type of emission

        predicted_values[q] = value
        # append to csv file
    
    for x in predicted_values:
        predicted_values[x] += currentUnit
    return predicted_values

def removeUnits(value):
    for x in range(2):
        value = value.replace('/ m2', "")
        value = value.replace('/ m3', "")
        value = value.replace('/ kg', "")
        value = value.replace('/ stk.', "")
        value = value.replace('/ stk', "")
        value = value.replace('-eq.', "")
        value = value.replace('co.', "")
        value = value.replace('kg', "")
        value = value.replace('mj', "")
        value = value.replace('ethene', "")
        value = value.replace('so.', "")
        value = value.replace('po.3', "")
        value = value.replace('po.', "")
        value = value.replace('sb.', "")
        value = value.replace('/m2', "")
        value = value.replace('m3', "")
        value = value.replace('cfc11', "")
        value = value.replace('eq.', "")
        value = value.replace('sb', "")
        value = value.replace('/', "")
        value = value.replace(' ', "")
        value = value.replace('o', "0")
        value = value.replace('m.', "")
        value = value.replace('m', "")
        value = value.replace('\"', "")
        value = value.replace('%', "")
        value = value.replace('*', "")
        value = value.replace('-ep.', "")
        value = value.replace('j', "")
        value = value.replace('g', "")
        value = value.replace('l', "1")
        value = value.replace('\'', "")
    return value

def main(): 
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    """
    / stk
    / m3
    / m2
    / kg
    """

    results = []

    #testList = [0, 5, 20, 9]
    #testList = [226, 112, 405, 216, 1021, 591, 687, 695, 525, 461, 716, 1104, 438, 1218, 199, 788, 718, 213, 1252, 1257, 323, 422, 786, 1086, 373, 87, 1040, 975, 182, 1173, 1273, 977, 1230, 202, 424, 752, 335, 539, 51, 922, 288, 74, 420, 94, 917, 1264, 265, 393, 49, 910, 18, 522, 834, 7, 65, 384, 1167, 1088, 433, 963, 556, 692, 595, 885, 1043, 1142, 274, 361, 805, 928, 753, 269, 735, 48, 1261, 1075, 189, 760, 1157, 436, 568, 668, 218, 428, 1122, 1251, 814, 608, 320, 1260, 653, 976, 297, 133, 1092, 180, 460, 982, 1089, 1200]
    for x in range(25):
        print(x)
        result = predict(model, processor, "results/{}-top.png".format(x), True)
        result.update(predict(model, processor, "results/{}-bottom.png".format(x), False))
        results.append(result)
    final = json.dumps(results, indent=2)
    with open("test.json", "w") as outfile:
        outfile.write(final)










    """ keysList = ['GWP', 'ODP', 'POCP', 'AP', 'EP', 'ADPE', 'ADPF', 'PERT', 'PENRT', 'RSF', 'NRSF']
    with open('test.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keysList)
        writer.writeheader()
        for result in results:
            writer.writerow(result) """
    
main()
    
    