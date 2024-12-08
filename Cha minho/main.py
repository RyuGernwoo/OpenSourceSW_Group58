from transformers import pipeline, GPT2LMHeadModel, GPT2Tokenizer
from PIL import Image

def extract_keywords_from_image(image_path):
    captioning_pipeline = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")
    image = Image.open(image_path)
    caption = captioning_pipeline(image)[0]['generated_text']
    return caption

def generate_sentence_from_keywords(keywords):
    model_name = "gpt2"
    model = GPT2LMHeadModel.from_pretrained(model_name)
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)

    input_ids = tokenizer.encode(keywords, return_tensors="pt")

    outputs = model.generate(input_ids, max_length=50, num_return_sequences=1,
                             no_repeat_ngram_size=2, top_p=0.9, top_k=50, do_sample=True)

    sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return sentence

image_path = "test.jpg"
keywords = extract_keywords_from_image(image_path)
print(f"추출된 키워드: {keywords}")

sentence = generate_sentence_from_keywords(keywords)
print(f"생성된 문장: {sentence}")
