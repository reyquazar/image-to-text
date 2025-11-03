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


def format_result(result, model_name):
    """Форматирует результат распознавания в организованную структуру"""
    if not result or len(result) == 0:
        return f"{model_name}\nРезультаты не найдены\n"

    output_lines = [f"{model_name}"]
    output_lines.append("=" * 50)

    for page_num, page in enumerate(result):
        output_lines.append(f"Страница {page_num + 1}:")
        output_lines.append("-" * 30)

        texts = page.get('rec_texts', [])
        boxes = page.get('det_boxes', [])
        scores = page.get('rec_scores', [])

        for i, (text, score) in enumerate(zip(texts, scores)):
            # Добавляем информацию о позиции, если есть bounding boxes
            if i < len(boxes):
                box = boxes[i]
                # Берем координаты левого верхнего угла для позиционирования
                x, y = int(box[0][0]), int(box[0][1])
                position_info = f"[Позиция: ({x},{y})]"
            else:
                position_info = ""

            output_lines.append(f"{i + 1:2d}. {text} {position_info} (точность: {score:.3f})")

    output_lines.append("=" * 50)
    return "\n".join(output_lines)


def format_result_simple(result, model_name):
    """Упрощенное форматирование с группировкой по строкам"""
    if not result or len(result) == 0:
        return f"{model_name}\nРезультаты не найдены\n"

    output_lines = [f"{model_name}"]
    output_lines.append("=" * 50)

    for page_num, page in enumerate(result):
        output_lines.append(f"Страница {page_num + 1}:")
        output_lines.append("-" * 30)

        texts = page.get('rec_texts', [])
        boxes = page.get('det_boxes', [])

        # Группируем тексты по строкам (основано на Y-координате)
        lines = {}
        for i, (text, box) in enumerate(zip(texts, boxes)):
            if i < len(boxes):
                y_coord = int(box[0][1])  # Y-координата верхнего левого угла
                line_key = (y_coord // 20) * 20  # Группируем по Y с допуском 20 пикселей

                if line_key not in lines:
                    lines[line_key] = []
                lines[line_key].append((int(box[0][0]), text))  # (X-координата, текст)

        # Сортируем строки по Y и слова в строке по X
        for y_key in sorted(lines.keys()):
            line_words = sorted(lines[y_key], key=lambda x: x[0])
            line_text = ' '.join([word[1] for word in line_words])
            output_lines.append(f"  {line_text}")

    output_lines.append("=" * 50)
    return "\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('image_path', type=str)
    args = parser.parse_args()
    image_path = args.image_path

    print("\n" + "=" * 80)
    print("РЕЗУЛЬТАТЫ РАСПОЗНАВАНИЯ ТЕКСТА")
    print("=" * 80)

    # Обработка каждой моделью с организованным выводом
    results = [
        ("PaddleModel", PRec_old(image_path)),
        ("MyModel1", PRec_new1(image_path)),
        ("MyModel2", PRec_latest(image_path)),
        ("LatestModel", PRec_new2(image_path))
    ]

    for model_name, result in results:
        formatted_output = format_result_simple(result, model_name)
        print(formatted_output)
        print()  # Пустая строка между моделями


if __name__ == "__main__":
    main()