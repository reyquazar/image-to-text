from PIL import Image
import pytesseract
from pathlib import Path
from pytesseract import TesseractNotFoundError

folder = Path('images')
total_images = len(list(folder.iterdir()))
print(f"In folder Images {total_images} image")

try:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program FilesTesseract-OCR\tesseract.exe'
    pytesseract.pytesseract.tessdata_dir_config = r'C:\Program FilesTesseract-OCR\tessdata'
    try:
        for image in range(total_images):
            print(f'            Image № {image + 1}')
            if image == 0:
                image_print = Image.open(f'images/img.png')
            else:
                image_print = Image.open(f'images/img_{image}.png')
            text = pytesseract.image_to_string(image_print, lang='rus+eng')
            print('=' * 200)
            print(text)
            print('=' * 200)
    except FileNotFoundError as e:
        print('No images in the folder')
except TesseractNotFoundError as e:
    print('Pytesseract not found')
