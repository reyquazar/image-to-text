import argparse
from paddleocr import *


def PRec(image):
    ocr = PaddleOCR(
        text_recognition_model_name="PP-OCRv5_server_rec",
        use_doc_orientation_classify=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(image)
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("=" * 100)
    print("PaddleModel")
    print("=" * 100)
    print(combined_text)
    print("=" * 100)


def printL(model, image):
    ocr = PaddleOCR(
        text_recognition_model_dir=f"./{model}/inference/",
        use_doc_orientation_classify=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(image)
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("=" * 100)
    print(model)
    print("=" * 100)
    print(combined_text)
    print("=" * 100)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str)
    args = parser.parse_args()
    image_path = args.image_path
    # image_path = './text/typed_text/testWords.png'

    PRec(image_path)  # default paddle model
    # printL("output1", image_path)  # synt data with gDTV2Words.py
    # printL("output2", image_path)  # synt data with gDTV2Words.py
    # printL("output3", image_path)  # synt data with gDTV2Words2.py
    # printL("output4", image_path)  # synt data with gDTV2Words2.py
    printL("output", image_path)  # synt data with gDTV2Words2.py


if __name__ == "__main__":
    main()
