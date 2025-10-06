import pytesseract
from PIL import Image
import pandas as pd
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = '../text/typed_text/test3.png'
image = Image.open(image_path)

# 1. Базовое распознавание текста
text_aze = pytesseract.image_to_string(image, lang='aze')
print('=' * 50, 'AZE - BASIC TEXT')
print(text_aze)

# 2. Получить данные с уверенностью (confidence)
print('\n' + '=' * 50, 'DETAILED DATA WITH CONFIDENCE')
data = pytesseract.image_to_data(image, lang='aze', output_type=pytesseract.Output.DICT)

# Создаем DataFrame для удобного просмотра
df = pd.DataFrame(data)
print(df[['text', 'conf', 'left', 'top', 'width', 'height']].head(20))

# 3. Только слова с высокой уверенностью
high_confidence_words = [(text, conf) for text, conf in zip(data['text'], data['conf']) if conf > 60 and text.strip()]
print('\n' + '=' * 50, 'HIGH CONFIDENCE WORDS (conf > 60)')
for word, conf in high_confidence_words:
    print(f"'{word}' (confidence: {conf}%)")

# 4. Получить информацию о расположении (bounding boxes)
print('\n' + '=' * 50, 'BOUNDING BOXES')
boxes = pytesseract.image_to_boxes(image, lang='aze')
print("Первые 10 символов с координатами:")
for i, box in enumerate(boxes.splitlines()[:10]):
    print(f"{i + 1}: {box}")

# 5. Получить данные в формате OSDU (более детальная информация)
print('\n' + '=' * 50, 'OSD (Orientation and Script Detection)')
try:
    osd = pytesseract.image_to_osd(image)
    print(osd)
except Exception as e:
    print(f"OSD не поддерживается: {e}")

# 6. Получить информацию о тексте с разметкой (hOCR)
print('\n' + '=' * 50, 'HOCR OUTPUT (first 500 chars)')
hocr = pytesseract.image_to_pdf_or_hocr(image, lang='aze', extension='hocr')
print(hocr[:500])  # Показываем только начало

# 7. Альтернативный вывод - только цифры
print('\n' + '=' * 50, 'DIGITS ONLY')
digits_only = pytesseract.image_to_string(image, lang='aze', config='--psm 6 -c tessedit_char_whitelist=0123456789')
print(f"Найденные цифры: {digits_only}")

# 8. Получить информацию о блоках текста
print('\n' + '=' * 50, 'TEXT BLOCKS')
blocks = pytesseract.image_to_boxes(image, lang='aze')
print(f"Всего обнаружено символов: {len(boxes.splitlines())}")

# 9. Анализ уверенности по словам
print('\n' + '=' * 50, 'CONFIDENCE ANALYSIS')
confidences = [conf for conf in data['conf'] if conf != -1]
if confidences:
    print(f"Средняя уверенность: {sum(confidences) / len(confidences):.2f}%")
    print(f"Максимальная уверенность: {max(confidences)}%")
    print(f"Минимальная уверенность: {min(confidences)}%")

# 10. Получить альтернативные варианты распознавания
print('\n' + '=' * 50, 'ALTERNATIVES (if available)')
try:
    # Этот метод может не работать во всех версиях
    alt_text = pytesseract.image_to_string(image, lang='aze', config='--psm 8')
    print("Альтернативный вариант (PSM 8):")
    print(alt_text)
except Exception as e:
    print(f"Альтернативы недоступны: {e}")


# 11. Визуализация результатов (если есть OpenCV)
def visualize_results(image_path, data):
    """Визуализация bounding boxes"""
    try:
        img = cv2.imread(image_path)
        for i in range(len(data['text'])):
            if int(data['conf'][i]) > 30:  # Только с уверенностью > 30%
                x = data['left'][i]
                y = data['top'][i]
                w = data['width'][i]
                h = data['height'][i]
                text = data['text'][i]
                conf = data['conf'][i]

                # Рисуем bounding box
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # Добавляем текст
                cv2.putText(img, f"{text}({conf}%)", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        print(f"\nВизуализация создана. Размеры изображения: {img.shape}")
        # Сохраняем результат
        cv2.imwrite('ocr_result_visualization.jpg', img)
        print("Визуализация сохранена как 'ocr_result_visualization.jpg'")

    except Exception as e:
        print(f"Визуализация недоступна: {e}")


# Запускаем визуализацию
visualize_results(image_path, data)

# 12. Экспорт в файлы
print('\n' + '=' * 50, 'EXPORT OPTIONS')
# Сохраняем текст в файл
with open('ocr_result.txt', 'w', encoding='utf-8') as f:
    f.write(text_aze)
print("Текст сохранен в 'ocr_result.txt'")

# Сохраняем детальные данные в CSV
df.to_csv('ocr_detailed_data.csv', index=False, encoding='utf-8')
print("Детальные данные сохранены в 'ocr_detailed_data.csv'")