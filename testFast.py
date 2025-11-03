import argparse
from paddleocr import *


def process_and_display_result(result, model_name):
    print("=" * 100)
    print(model_name)

    if result and len(result) > 0:
        # Группируем текст по строкам на основе координат Y
        lines = {}

        for line in result[0]:
            text = line.get('rec_text', [''])[0]
            bbox = line.get('det_box', [])

            if bbox:
                # Вычисляем среднюю Y-координату для группировки по строкам
                y_center = sum(point[1] for point in bbox) / len(bbox)

                # Округляем для группировки (можно настроить чувствительность)
                line_key = round(y_center / 10) * 10

                if line_key not in lines:
                    lines[line_key] = []

                # Сохраняем текст и X-координату для сортировки слева направо
                x_center = sum(point[0] for point in bbox) / len(bbox)
                lines[line_key].append((x_center, text))

        # Сортируем строки по Y (сверху вниз) и слова в строке по X (слева направо)
        for y_key in sorted(lines.keys()):
            line_words = sorted(lines[y_key], key=lambda x: x[0])
            line_text = ' '.join(word[1] for word in line_words)
            print(line_text)

    print("=" * 100)


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

    # Обработка разными моделями
    result_old = PRec_old(image_path)
    process_and_display_result(result_old, "PaddleModel")

    result_new1 = PRec_new1(image_path)
    process_and_display_result(result_new1, "MyModel1")

    result_latest = PRec_latest(image_path)
    process_and_display_result(result_latest, "MyModel2")

    result_new2 = PRec_new2(image_path)
    process_and_display_result(result_new2, "LatestModel")


if __name__ == "__main__":
    main()