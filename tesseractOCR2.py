import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

image_path = 'test9.png'

image = Image.open(image_path)
text_aze = pytesseract.pytesseract.image_to_string(image, lang='aze')
text_aze_cyrl = pytesseract.pytesseract.image_to_string(image, lang='aze_cyrl')
text_ru = pytesseract.pytesseract.image_to_string(image, lang='rus')
text2 = pytesseract.pytesseract.image_to_string(image, lang='aze_cyrl+rus')

print('=' * 50, 'AZE')
print(text_aze)
print('=' * 50, 'AZE_CYRL')
print(text_aze_cyrl)
print('=' * 50, 'RU')
print(text_ru, 'TOGETHER')
print('=' * 50)
print(text2)
