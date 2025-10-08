from paddleocr import *


def PRec(image):
    ocr = PaddleOCR(text_recognition_model_dir="./output/best_accuracy")
    result = ocr.predict(image)
    ocr
    return result


def main():
    image_path = 'text/debug/img1.jpg'
    result = PRec(image_path)
    # save_txt(result, filename='temp1.txt')
    if result and len(result) > 0:
        page = result[0]
        texts = page.get('rec_texts', [])
        combined_text = ' '.join(texts)
    print(combined_text)


if __name__ == "__main__":
    main()
