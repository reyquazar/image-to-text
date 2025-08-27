import cv2
import pytesseract
import os
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = "test10.png"
img = cv2.imread(image_path)

# Улучшенная предобработка изображения
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)  # Уменьшение шума
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Используем улучшенную конфигурацию Tesseract
custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitespace=0'
data = pytesseract.image_to_data(thresh, lang="rus+eng+aze",
                                 output_type=pytesseract.Output.DICT, config=custom_config)

os.makedirs("words_output", exist_ok=True)

counter = 1
for i, word in enumerate(data["text"]):
    # Фильтруем только значимые слова
    if len(word.strip()) > 1 and data["conf"][i] > 30:  # Минимальная уверенность 30%
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]

        # Увеличиваем отступ для лучшего захвата
        pad_x = int(w * 0.3)  # 30% от ширины слова
        pad_y = int(h * 0.5)  # 50% от высоты слова

        x1 = max(0, x - pad_x)
        y1 = max(0, y - pad_y)
        x2 = min(img.shape[1], x + w + pad_x)
        y2 = min(img.shape[0], y + h + pad_y)

        # Проверяем, что область не пустая
        if x2 > x1 and y2 > y1:
            word_img = img[y1:y2, x1:x2]

            # Сохраняем только если изображение не слишком маленькое
            if word_img.shape[0] > 5 and word_img.shape[1] > 5:
                cv2.imwrite(f"words_output/word_{counter}.png", word_img)
                counter += 1

print(f"Сохранено {counter - 1} слов в папке words_output/")