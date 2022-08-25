import torch
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import re

def predict(model, processor, path): 
    emission_qs = [
        "GWP",
    ]

    _img = Image.open(path)
    pixel_values = processor(_img.convert('RGB'), return_tensors="pt").pixel_values

    predicted_values = {}

    for q in emission_qs:
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
        predicted_values[q] = value

        print(predicted_values)
        # append to csv file
    
    return seq




def main(): 
    model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-docvqa")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # 
    """
    For each image in folder
        Predict all emission attributes
        Append all emission attributes in a dataframe/excel/csv
    """
    results = predict(model, processor, "results/0-bottom.png")

    # 
main()
    
    