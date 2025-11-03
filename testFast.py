import argparse

from paddleocr import *


def PRec_old(image):
    ocr = PaddleOCR(
        text_recognition_model_name="PP-OCRv5_server_rec",
        use_doc_orientation_classify=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(image)
    return result


def PRec_new1(image):
    ocr = PaddleOCR(
        text_recognition_model_dir="./Foutput1/inference/",
        use_doc_orientation_classify=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(image)
    return result


def PRec_new2(image):
    ocr = PaddleOCR(
        text_recognition_model_dir="./Foutput2/inference/",
        use_doc_orientation_classify=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(image)
    return result


def PRec_latest(image):
    ocr = PaddleOCR(
        text_recognition_model_dir="./output/inference/",
        use_doc_orientation_classify=False,
        use_textline_orientation=False,
    )
    result = ocr.predict(image)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str)
    args = parser.parse_args()
    image_path = args.image_path
    # image_path = './text/typed_text/testWords.png'
    result = PRec_old(image_path)
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("=" * 100)
    print("PaddleModel")
    print(combined_text)
    print("=" * 100)

    result = PRec_new1(image_path)
    # save_txt(result, filename='temp1.txt')
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("=" * 100)
    print("MyModel1")
    print(combined_text)
    print("=" * 100)

    result = PRec_latest(image_path)
    # save_txt(result, filename='temp1.txt')
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("=" * 100)
    print("MyModel2")
    print(combined_text)
    print("=" * 100)
    result = PRec_new2(image_path)
    # save_txt(result, filename='temp1.txt')
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("=" * 100)
    print("LatestModel")
    print(combined_text)
    print("=" * 100)


if __name__ == "__main__":
    main()
