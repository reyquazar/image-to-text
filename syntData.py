import os
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageEnhance
import cv2
from skimage import exposure
import arabic_reshaper
from bidi.algorithm import get_display
import textwrap


class AdvancedSyntheticDataGenerator:
    def __init__(self, gt_file_path, output_dir, num_samples=2000):
        self.gt_file_path = gt_file_path
        self.output_dir = output_dir
        self.num_samples = num_samples
        self.texts = self.load_texts()

        # Больше разнообразных шрифтов
        self.fonts = self.get_available_fonts()

        # Фоновые текстуры
        self.backgrounds = self.generate_backgrounds()

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(os.path.join(output_dir, "images"), exist_ok=True)

    def get_available_fonts(self):
        """Получение доступных шрифтов"""
        font_dirs = [
            "/usr/share/fonts/",
            "/usr/local/share/fonts/",
            "C:/Windows/Fonts/",
            "/System/Library/Fonts/",
            "/Library/Fonts/"
        ]

        fonts = []
        for font_dir in font_dirs:
            if os.path.exists(font_dir):
                for root, dirs, files in os.walk(font_dir):
                    for file in files:
                        if file.lower().endswith(('.ttf', '.otf', '.ttc')):
                            fonts.append(os.path.join(root, file))

        # Fallback fonts
        fallback_fonts = ["arial.ttf", "times.ttf", "cour.ttf", "verdana.ttf"]
        fonts.extend(fallback_fonts)

        return fonts[:50]  # Берем первые 50 шрифтов

    def generate_backgrounds(self):
        """Генерация разнообразных фонов"""
        backgrounds = []

        # Цветные фоны
        for _ in range(20):
            color = (random.randint(200, 255), random.randint(200, 255), random.randint(200, 255))
            backgrounds.append(('color', color))

        # Текстурированные фоны
        textures = ['noise', 'gradient', 'lines', 'dots']
        for texture in textures:
            for _ in range(10):
                backgrounds.append(('texture', texture))

        return backgrounds

    def create_background(self, width, height):
        """Создание разнообразного фона"""
        bg_type, bg_value = random.choice(self.backgrounds)

        if bg_type == 'color':
            return Image.new('RGB', (width, height), bg_value)
        else:
            # Создаем текстурированный фон
            base = Image.new('RGB', (width, height),
                             (random.randint(230, 255), random.randint(230, 255), random.randint(230, 255)))

            draw = ImageDraw.Draw(base)

            if bg_value == 'noise':
                # Добавляем шум
                noise = np.random.randint(0, 30, (height, width, 3), dtype=np.uint8)
                noise_img = Image.fromarray(noise, 'RGB')
                base = Image.blend(base, noise_img, alpha=0.1)

            elif bg_value == 'gradient':
                # Градиентный фон
                for y in range(height):
                    color = (
                        random.randint(230, 255),
                        random.randint(230, 255),
                        random.randint(230, 255)
                    )
                    draw.line([(0, y), (width, y)], fill=color)

            elif bg_value == 'lines':
                # Линии на фоне
                for _ in range(random.randint(5, 20)):
                    color = (random.randint(240, 255), random.randint(240, 255), random.randint(240, 255))
                    y = random.randint(0, height)
                    draw.line([(0, y), (width, y)], fill=color, width=random.randint(1, 3))

            elif bg_value == 'dots':
                # Точки на фоне
                for _ in range(random.randint(50, 200)):
                    color = (random.randint(240, 255), random.randint(240, 255), random.randint(240, 255))
                    x, y = random.randint(0, width), random.randint(0, height)
                    draw.ellipse([x, y, x + 2, y + 2], fill=color)

            return base

    def apply_document_augmentations(self, image):
        """Улучшенные аугментации для документов"""
        img_array = np.array(image)

        # 1. Искажения перспективы (как сканированные документы)
        if random.random() > 0.7:
            h, w = img_array.shape
            pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])

            # Случайные смещения углов
            max_offset = 5
            pts2 = np.float32([
                [random.randint(-max_offset, max_offset), random.randint(-max_offset, max_offset)],
                [w - random.randint(-max_offset, max_offset), random.randint(-max_offset, max_offset)],
                [random.randint(-max_offset, max_offset), h - random.randint(-max_offset, max_offset)],
                [w - random.randint(-max_offset, max_offset), h - random.randint(-max_offset, max_offset)]
            ])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            img_array = cv2.warpPerspective(img_array, matrix, (w, h), borderMode=cv2.BORDER_REPLICATE)

        # 2. Эластичные деформации (эффект бумаги)
        if random.random() > 0.6:
            alpha = random.randint(30, 80)  # интенсивность
            sigma = random.randint(5, 10)  # гладкость

            dx = np.random.uniform(-1, 1, img_array.shape) * alpha
            dy = np.random.uniform(-1, 1, img_array.shape) * alpha

            x, y = np.meshgrid(np.arange(img_array.shape[1]), np.arange(img_array.shape[0]))
            indices = np.reshape(y + dy, (-1, 1)), np.reshape(x + dx, (-1, 1))

            img_array = cv2.remap(img_array, indices[1].astype(np.float32),
                                  indices[0].astype(np.float32), cv2.INTER_LINEAR)

        # 3. Шумы, характерные для документов
        noise_type = random.choice(['gaussian', 'salt_pepper', 'speckle'])

        if noise_type == 'gaussian':
            noise = np.random.normal(0, random.uniform(1, 3), img_array.shape)
            img_array = np.clip(img_array + noise, 0, 255).astype(np.uint8)

        elif noise_type == 'salt_pepper':
            salt_vs_pepper = 0.5
            amount = random.uniform(0.01, 0.05)

            # Соль
            num_salt = np.ceil(amount * img_array.size * salt_vs_pepper)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img_array.shape]
            img_array[coords[0], coords[1]] = 255

            # Перец
            num_pepper = np.ceil(amount * img_array.size * (1. - salt_vs_pepper))
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img_array.shape]
            img_array[coords[0], coords[1]] = 0

        # 4. Размытие (имитация сканера)
        blur_type = random.choice(['gaussian', 'median', 'motion'])

        if blur_type == 'gaussian':
            ksize = random.choice([3, 5])
            img_array = cv2.GaussianBlur(img_array, (ksize, ksize), 0)

        elif blur_type == 'median':
            ksize = random.choice([3, 5])
            img_array = cv2.medianBlur(img_array, ksize)

        elif blur_type == 'motion':
            size = random.randint(5, 15)
            kernel = np.zeros((size, size))
            kernel[int((size - 1) / 2), :] = np.ones(size)
            kernel = kernel / size
            img_array = cv2.filter2D(img_array, -1, kernel)

        # 5. Изменение контраста и яркости (разные условия сканирования)
        contrast = random.uniform(0.7, 1.3)
        brightness = random.randint(-20, 20)
        img_array = cv2.convertScaleAbs(img_array, alpha=contrast, beta=brightness)

        # 6. Морфологические операции (износ документа)
        if random.random() > 0.8:
            op_type = random.choice(['erode', 'dilate'])
            kernel = np.ones((2, 2), np.uint8)

            if op_type == 'erode':
                img_array = cv2.erode(img_array, kernel, iterations=1)
            else:
                img_array = cv2.dilate(img_array, kernel, iterations=1)

        # 7. Имитация складок и теней на бумаге
        if random.random() > 0.9:
            h, w = img_array.shape
            for _ in range(random.randint(1, 3)):
                x1, y1 = random.randint(0, w - 1), random.randint(0, h - 1)
                x2, y2 = random.randint(0, w - 1), random.randint(0, h - 1)

                # Рисуем линию с размытием (складка)
                cv2.line(img_array, (x1, y1), (x2, y2), (200, 200, 200),
                         random.randint(2, 4), lineType=cv2.LINE_AA)

        return Image.fromarray(img_array)
    def add_gaussian_blur(self, img):
        """Добавление Gaussian blur"""
        if random.random() > 0.7:
            ksize = random.choice([3, 5, 7])
            return cv2.GaussianBlur(img, (ksize, ksize), 0)
        return img

    def add_motion_blur(self, img):
        """Добавление motion blur"""
        if random.random() > 0.8:
            size = random.randint(5, 15)
            kernel = np.zeros((size, size))
            kernel[int((size - 1) / 2), :] = np.ones(size)
            kernel = kernel / size
            return cv2.filter2D(img, -1, kernel)
        return img

    def add_gaussian_noise(self, img):
        """Добавление Gaussian noise"""
        if random.random() > 0.6:
            mean = 0
            sigma = random.uniform(1, 10)
            gauss = np.random.normal(mean, sigma, img.shape)
            noisy = np.clip(img + gauss, 0, 255).astype(np.uint8)
            return noisy
        return img

    def add_salt_pepper_noise(self, img):
        """Добавление salt and pepper noise"""
        if random.random() > 0.7:
            amount = random.uniform(0.001, 0.01)
            s_vs_p = 0.5
            out = np.copy(img)

            # Salt mode
            num_salt = np.ceil(amount * img.size * s_vs_p)
            coords = [np.random.randint(0, i - 1, int(num_salt)) for i in img.shape[:2]]
            out[coords[0], coords[1], :] = 255

            # Pepper mode
            num_pepper = np.ceil(amount * img.size * (1. - s_vs_p))
            coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in img.shape[:2]]
            out[coords[0], coords[1], :] = 0

            return out
        return img

    def adjust_brightness_contrast(self, img):
        """Коррекция яркости и контраста"""
        if random.random() > 0.5:
            alpha = random.uniform(0.7, 1.3)  # контраст
            beta = random.randint(-40, 40)  # яркость
            return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)
        return img

    def adjust_gamma(self, img):
        """Гамма-коррекция"""
        if random.random() > 0.6:
            gamma = random.uniform(0.5, 2.0)
            inv_gamma = 1.0 / gamma
            table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
            return cv2.LUT(img, table)
        return img

    def add_perspective_distortion(self, img):
        """Искажение перспективы"""
        if random.random() > 0.7:
            h, w = img.shape[:2]

            pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
            pts2 = np.float32([
                [random.randint(-10, 10), random.randint(-10, 10)],
                [w - random.randint(-10, 10), random.randint(-10, 10)],
                [random.randint(-10, 10), h - random.randint(-10, 10)],
                [w - random.randint(-10, 10), h - random.randint(-10, 10)]
            ])

            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            return cv2.warpPerspective(img, matrix, (w, h))
        return img

    def add_elastic_distortion(self, img):
        """Эластичная деформация"""
        if random.random() > 0.8:
            h, w = img.shape[:2]

            # Случайное поле смещений
            dx = np.random.uniform(-1, 1, (h, w)) * random.randint(2, 5)
            dy = np.random.uniform(-1, 1, (h, w)) * random.randint(2, 5)

            # Создаем сетку координат
            x, y = np.meshgrid(np.arange(w), np.arange(h))

            # Применяем смещения
            map_x = (x + dx).astype(np.float32)
            map_y = (y + dy).astype(np.float32)

            return cv2.remap(img, map_x, map_y, cv2.INTER_LINEAR)
        return img

    def create_text_image(self, text, img_width=320, img_height=100):
        """Создание разнообразного изображения с текстом"""
        # Создаем разнообразный фон
        background = self.create_background(img_width, img_height)
        draw = ImageDraw.Draw(background)

        # Случайный размер и стиль шрифта
        font_size = random.randint(18, 40)
        font_path = random.choice(self.fonts)

        try:
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # Случайный цвет текста (не только черный)
        text_color = (
            random.randint(0, 100),
            random.randint(0, 100),
            random.randint(0, 100)
        )

        # Разбиваем текст на строки если нужно
        max_width = img_width - 40
        lines = []
        words = text.split()
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width = draw.textlength(test_line, font=font)

            if test_width <= max_width:
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

        # Случайное смещение для естественности
        x = (img_width - text_width) // 2 - bbox[0] + random.randint(-10, 10)
        y = (img_height - text_height) // 2 - bbox[1] + random.randint(-10, 10)

        # Рисуем текст с тенью (иногда)
        if random.random() > 0.7:
            shadow_color = (random.randint(150, 200), random.randint(150, 200), random.randint(150, 200))
            draw.multiline_text((x + 1, y + 1), text, font=font, fill=shadow_color, spacing=3)

        # Основной текст
        draw.multiline_text((x, y), text, font=font, fill=text_color, spacing=3)

        # Применяем продвинутые аугментации
        final_image = self.apply_advanced_augmentations(background)

        # Конвертируем в grayscale для OCR
        final_image = final_image.convert('L')

        return final_image

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

    def generate_dataset(self):
        """Генерация разнообразного набора данных"""
        if not self.texts:
            print("Нет текстов для генерации!")
            return

        gt_file_path = os.path.join(self.output_dir, "synthetic_gt.txt")

        with open(gt_file_path, 'w', encoding='utf-8') as gt_file:
            for i in range(self.num_samples):
                # Выбираем случайный текст
                text = random.choice(self.texts)

                # Случайный размер изображения
                width = random.randint(300, 400)
                height = random.randint(80, 120)

                # Создаем изображение
                img = self.create_text_image(text, width, height)

                # Сохраняем изображение
                img_filename = f"synthetic_{i:05d}.png"
                img_path = os.path.join(self.output_dir, "images", img_filename)
                img.save(img_path)

                # Записываем в файл разметки
                gt_file.write(f"images/{img_filename}\t{text}\n")

                if (i + 1) % 100 == 0:
                    print(f"Сгенерировано {i + 1} изображений")

        print(f"Генерация завершена! Создано {self.num_samples} разнообразных изображений")
        print(f"Файл разметки: {gt_file_path}")


# Использование
if __name__ == "__main__":
    GT_FILE_PATH = "text/typed_text/rec_gt.txt"
    OUTPUT_DIR = "text/typed_text/synthetic_data_advanced"
    NUM_SAMPLES = 100

    generator = AdvancedSyntheticDataGenerator(GT_FILE_PATH, OUTPUT_DIR, NUM_SAMPLES)
    generator.generate_dataset()