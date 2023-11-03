from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tessdata_dir_config = r'C:\Program Files\Tesseract-OCR\tessdata'
image = Image.open('img_4.png')
text = pytesseract.image_to_string(image, lang='rus+eng')
print(text)
