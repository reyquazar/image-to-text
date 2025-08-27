from transformers import pipeline
from PIL import Image

ocr = pipeline("image-to-text", model="microsoft/trocr-base-printed")
results = ocr(Image.open("test10.png").convert("RGB"))

for idx, item in enumerate(results):
    print(f"Страница {idx+1}: {item['generated_text']}")