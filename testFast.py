from paddleocr import *


def PRec_old(image):
    ocr = PaddleOCR(text_recognition_model_name="PP-OCRv5_server_rec")
    result = ocr.predict(image)
    return result


def PRec_new(image):
    ocr = PaddleOCR(text_recognition_model_dir="./output/")
    result = ocr.predict(image)
    return result


def main():
    image_path = 'text/debug/synthetic_0001.jpg'
    result = PRec_old(image_path)
    # save_txt(result, filename='temp1.txt')
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("="*100, combined_text)
    result = PRec_new(image_path)
    # save_txt(result, filename='temp1.txt')
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print("="*100, combined_text)


if __name__ == "__main__":
    main()
