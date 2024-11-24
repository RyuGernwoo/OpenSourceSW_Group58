from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import CLIPProcessor, CLIPModel
import torch
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # CORS 활성화

# CLIP 모델과 프로세서 로드
model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

animal_texts = [
    "a photo of a mouse", "a photo of a cow", "a photo of a tiger", 
    "a photo of a rabbit", "a photo of a dragon", "a photo of a snake", 
    "a photo of a horse", "a photo of a sheep", "a photo of a monkey", 
    "a photo of a chicken", "a photo of a dog", "a photo of a pig",
    "a photo of a cat", "a photo of an eagle", "a photo of an elephant"
]

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    image = Image.open(io.BytesIO(file.read()))

    # 이미지와 텍스트를 모델에 입력
    inputs = processor(text=animal_texts, images=image, return_tensors="pt", padding=True)
    outputs = model(**inputs)

    # 확률 계산
    logits_per_image = outputs.logits_per_image
    probs = logits_per_image.softmax(dim = 1)

    # 결과를 딕셔너리로 변환
    animal_probs = [{"animal": animal_texts[i], "probability": probs[0][i].item()} for i in range(len(animal_texts))]
    print(animal_probs)
    return jsonify(animal_probs)

if __name__ == '__main__':
    app.run(debug=True)
