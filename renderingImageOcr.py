import cv2
import numpy as np
import pytesseract
from PIL import Image
import matplotlib.pyplot as plt


def preprocess_handwritten_text(image_path):
    # Загрузка изображения
    img = cv2.imread(image_path)

    # 1. Увеличение резкости
    kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
    sharpened = cv2.filter2D(img, -1, kernel)

    # 2. Конвертация в grayscale
    gray = cv2.cvtColor(sharpened, cv2.COLOR_BGR2GRAY)

    # 3. Адаптивная бинаризация (критически важно для рукописного текста)
    binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)

    # 4. Удаление шума
    denoised = cv2.medianBlur(binary, 3)

    # 5. Морфологические операции для улучшения текста
    kernel = np.ones((1, 1), np.uint8)
    processed = cv2.morphologyEx(denoised, cv2.MORPH_CLOSE, kernel)

    return processed


def ocr_handwritten_azerbaijani(image_path):
    # Предобработка изображения
    processed_img = preprocess_handwritten_text(image_path)

    # Настройки Tesseract для рукописного текста
    custom_config = r'--oem 3 --psm 6 -l aze'

    # Распознавание текста
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    text = pytesseract.image_to_string(processed_img, config=custom_config)

    return text


# Использование
image_path = "test_15.png"
result = ocr_handwritten_azerbaijani(image_path)
print("Распознанный текст:")
print(result)
