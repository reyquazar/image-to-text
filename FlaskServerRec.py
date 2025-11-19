from flask import Flask, request, jsonify
from paddleocr import PaddleOCR
import base64
import cv2
import numpy as np
import io
from PIL import Image

app = Flask(__name__)

# Инициализация PaddleOCR один раз при запуске
ocr = PaddleOCR(
    use_doc_orientation_classify=False,
    use_textline_orientation=False,
)


@app.route('/ocr', methods=['POST'])
def process_ocr():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({'error': 'No image data provided'}), 400

        # Декодируем base64 изображение
        image_data = base64.b64decode(data['image'])

        # Конвертируем в numpy array для OpenCV
        image = Image.open(io.BytesIO(image_data))
        image_np = np.array(image)

        # Если изображение в RGBA, конвертируем в RGB
        if image_np.shape[2] == 4:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGBA2RGB)

        # Выполняем OCR
        result = ocr.predict(image_np)

        # Извлекаем текст из результата
        texts = []
        if result and len(result) > 0:
            for line in result[0]:
                if line and len(line) >= 2:
                    text = line[1][0]  # Текст находится в [1][0]
                    texts.append(text)

        combined_text = ' '.join(texts) if texts else 'Текст не распознан'

        return jsonify({'text': combined_text})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Запуск сервера OCR на http://localhost:5000")
    print("Убедитесь, что установлены все зависимости:")
    print("pip install flask paddleocr opencv-python pillow")
    app.run(host='localhost', port=5000, debug=False)