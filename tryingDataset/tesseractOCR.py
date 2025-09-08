import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def createFolderWithWords(image_path, counter):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    data = pytesseract.image_to_data(img, lang="rus+eng+aze", output_type=pytesseract.Output.DICT)
    os.makedirs(f"{image_path[:-4]}", exist_ok=True)
    for i, word in enumerate(data["text"]):
        if word.strip() != "":
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            pad = 5
            x1 = max(0, x - pad)
            y1 = max(0, y - pad)
            x2 = min(img.shape[1], x + w + pad)
            y2 = min(img.shape[0], y + h + pad)
            word_img = img[y1:y2, x1:x2]
            cv2.imwrite(f"{image_path[:-4]}/word_{counter}.png", word_img)
            counter += 1
    print(f"Сохранено {counter - 1} слов в папке {image_path[:-4]}/")
    return counter

counter = 1
total_count = createFolderWithWords("../testCopySmall.png", 1)
total_count = createFolderWithWords("../testCopyWindCleaner.png", total_count)
total_count = createFolderWithWords("../testCopy.png", total_count)
total_count = createFolderWithWords("../test10.png", total_count)
total_count = createFolderWithWords("../test15.png", total_count)
total_count = createFolderWithWords("../test20.png", total_count)
total_count = createFolderWithWords("../test25.png", total_count)
total_count = createFolderWithWords("../testStart.png", total_count)
