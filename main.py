from PIL import Image
import pytesseract
from pathlib import Path
from pytesseract import TesseractNotFoundError


def set_tesseract_path():
    try:
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        pytesseract.pytesseract.tessdata_dir_config = r'C:\Program Files\Tesseract-OCR\tessdata'
    except TesseractNotFoundError:
        print('Pytesseract not found')


def process_image(image_path):
    try:
        image_print = Image.open(image_path)
        text = pytesseract.image_to_string(image_print, lang='rus+eng')
        text = text.replace('\n', ' ')
        print('=' * 200)
        print(text)
        print('=' * 200)
    except FileNotFoundError:
        print(f'File not found: {image_path}')
    except Exception as e:
        print(f'Error processing image {image_path}: {e}')


def main():
    folder = Path('images')
    total_images = len(list(folder.iterdir()))
    print(f"In folder Images {total_images} image")

    set_tesseract_path()

    for image in range(total_images):
        print(f'            Image № {image + 1}')
        if image == 0:
            image_path = 'images/img.png'
        else:
            image_path = f'images/img_{image}.png'
        process_image(image_path)


if __name__ == "__main__":
    main()
