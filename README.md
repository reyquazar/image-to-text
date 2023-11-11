## Image to Text Converter

### Описание

Это приложение позволяет преобразовывать изображения в текст с использованием оптического распознавания символов (OCR).
Можно выбрать изображение для обработки из файловой системы или использовать изображение из буфера обмена.

### Требования

- Python 3.10
- Библиотека Pillow (PIL)
- Библиотека pytesseract
- Библиотека tkinter

### Установка [Tesseract OCR](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe)

В программе указан путь:

```
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

Убедительная просьба устанавливать по этому же пути и обязательно отметить русский язык в установщике.

### Использование

Есть 4 кнопки:

1. Clipboard - берет изображение из буфера обмена
2. Browse - выбор локального изображения
3. Copy - копирует считанный текст
4. Delete - очищает поле

### Чтобы скачать готовое приложение нажимите [сюда](https://github.com/reyquazar/image-to-text/releases/download/v1.0/imageToText.exe)