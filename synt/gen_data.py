import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
import numpy as np
from textwrap import wrap
import cv2


class SyntheticDataGenerator:
    def __init__(self, gt_file_path, output_dir, num_samples=1000):
        self.gt_file_path = gt_file_path
        self.output_dir = output_dir
        self.num_samples = num_samples
        self.texts = self.load_texts()

        # Шрифты (укажите пути к шрифтам на вашей системе)
        self.fonts = [
            "arial.ttf",
            "arialbd.ttf",
            "times.ttf",
            "timesbd.ttf",
            "cour.ttf"
        ]

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

    def load_texts(self):
        """Загрузка текстов из файла разметки"""
        texts = []
        try:
            with open(self.gt_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if '\t' in line:
                        parts = line.strip().split('\t')
                        if len(parts) >= 2:
                            texts.append(parts[1])
            print(f"Загружено {len(texts)} текстов")
            return texts
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            return []

    def get_random_font(self, font_size):
        """Выбор случайного шрифта"""
        font_path = random.choice(self.fonts)
        try:
            return ImageFont.truetype(font_path, font_size)
        except:
            # Fallback font
            return ImageFont.load_default()

    def apply_augmentations(self, image):
        """Применение аугментаций к изображению"""
        img_array = np.array(image)

        # Случайное размытие
        if random.random() > 0.7:
            kernel_size = random.choice([3, 5])
            img_array = cv2.GaussianBlur(img_array, (kernel_size, kernel_size), 0)

        # Случайный шум
        if random.random() > 0.8:
            noise = np.random.normal(0, random.uniform(1, 3), img_array.shape)
            img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)

        # Изменение яркости/контраста
        if random.random() > 0.6:
            alpha = random.uniform(0.8, 1.2)  # контраст
            beta = random.randint(-30, 30)  # яркость
            img_array = cv2.convertScaleAbs(img_array, alpha=alpha, beta=beta)

        return Image.fromarray(img_array)

    def create_text_image(self, text, img_width=320, img_height=100):
        """Создание изображения с текстом"""
        # Создаем белое изображение
        image = Image.new('L', (img_width, img_height), 255)
        draw = ImageDraw.Draw(image)

        # Случайный размер шрифта
        font_size = random.randint(20, 35)
        font = self.get_random_font(font_size)

        # Пытаемся вписать текст
        text_width = draw.textlength(text, font=font)
        max_attempts = 5
        attempt = 0

        while text_width > img_width - 40 and attempt < max_attempts:
            font_size -= 2
            font = self.get_random_font(font_size)
            text_width = draw.textlength(text, font=font)
            attempt += 1

        # Если текст не влезает, разбиваем на строки
        if text_width > img_width - 40:
            words = text.split()
            lines = []
            current_line = ""

            for word in words:
                test_line = current_line + " " + word if current_line else word
                test_width = draw.textlength(test_line, font=font)

                if test_width <= img_width - 40:
                    current_line = test_line
                else:
                    if current_line:
                        lines.append(current_line)
                    current_line = word

            if current_line:
                lines.append(current_line)

            text = "\n".join(lines)

        # Позиционирование текста
        bbox = draw.multiline_textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (img_width - text_width) // 2 - bbox[0]
        y = (img_height - text_height) // 2 - bbox[1]

        # Рисуем текст
        draw.multiline_text((x, y), text, font=font, fill=0, spacing=5)

        # Применяем аугментации
        image = self.apply_augmentations(image)

        return image

    def generate_dataset(self):
        """Генерация набора данных"""
        if not self.texts:
            print("Нет текстов для генерации!")
            return

        gt_file_path = os.path.join(self.output_dir, "synthetic_gt.txt")

        with open(gt_file_path, 'w', encoding='utf-8') as gt_file:
            for i in range(self.num_samples):
                # Выбираем случайный текст
                text = random.choice(self.texts)

                # Создаем изображение
                img = self.create_text_image(text)

                # Сохраняем изображение
                img_filename = f"synthetic_{i:04d}.png"
                img_path = os.path.join(self.output_dir, "images", img_filename)
                img.save(img_path)

                # Записываем в файл разметки
                gt_file.write(f"images/{img_filename}\t{text}\n")

                if (i + 1) % 100 == 0:
                    print(f"Сгенерировано {i + 1} изображений")

        print(f"Генерация завершена! Создано {self.num_samples} изображений")
        print(f"Файл разметки: {gt_file_path}")


# Использование
if __name__ == "__main__":
    # Настройки
    GT_FILE_PATH = "../text/test/rec_gt.txt"  # ваш файл с текстами
    OUTPUT_DIR = "../text/test/"  # выходная директория
    NUM_SAMPLES = 5000  # количество синтетических изображений

    # Создаем генератор
    generator = SyntheticDataGenerator(GT_FILE_PATH, OUTPUT_DIR, NUM_SAMPLES)

    # Генерируем данные
    generator.generate_dataset()