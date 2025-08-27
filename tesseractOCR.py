import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = "testCopySmall.png"
img = cv2.imread(image_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

data = pytesseract.image_to_data(img, lang="rus+eng+aze", output_type=pytesseract.Output.DICT)

os.makedirs("words_output", exist_ok=True)

counter = 1
for i, word in enumerate(data["text"]):
    if word.strip() != "":
        x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]

        pad = 5
        x1 = max(0, x - pad)
        y1 = max(0, y - pad)
        x2 = min(img.shape[1], x + w + pad)
        y2 = min(img.shape[0], y + h + pad)

        word_img = img[y1:y2, x1:x2]

        cv2.imwrite(f"words_output/word_{counter}.png", word_img)

        counter += 1

print(f"Сохранено {counter - 1} слов в папке words_output/")
