import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import argparse
import lmdb
import pickle


def create_lmdb_dataset(labels, output_path, image_dir):
    """Создает LMDB датасет из меток и изображений"""
    map_size = 1024 * 1024 * 1024 * 10  # 10GB
    env = lmdb.open(output_path, map_size=map_size)

    with env.begin(write=True) as txn:
        for i, label in enumerate(labels):
            filename, word = label.split('\t')
            img_path = os.path.join(image_dir, filename)

            # Читаем изображение
            with open(img_path, 'rb') as f:
                image_data = f.read()

            # Сохраняем в LMDB
            key = f"{i:08d}".encode()
            value = pickle.dumps({'image': image_data, 'label': word})
            txn.put(key, value)

    env.close()
    print(f"✅ LMDB dataset created: {output_path}")


def load_words_from_dataset(dataset_path):
    """Загружает слова из датасета"""
    words = []
    try:
        with open(dataset_path, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip().split()[0] if line.strip() else None
                if word and len(word) >= 2:
                    words.append(word)
        print(f"✅ Loaded {len(words)} words from dataset")
        return words
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None


def add_document_noise(img_array):
    """Добавляет шумы, характерные для документов"""
    h, w = img_array.shape[:2]

    if random.random() < 0.2:
        num_spots = random.randint(1, 5)
        for _ in range(num_spots):
            x, y = random.randint(0, w - 1), random.randint(0, h - 1)
            radius = random.randint(2, 10)
            intensity = random.randint(5, 20)
            cv2.circle(img_array, (x, y), radius, (intensity, intensity, intensity), -1)

    if random.random() < 0.15:
        num_lines = random.randint(1, 3)
        for _ in range(num_lines):
            x1, y1 = random.randint(0, w - 1), random.randint(0, h - 1)
            x2, y2 = random.randint(0, w - 1), random.randint(0, h - 1)
            thickness = random.randint(1, 2)
            intensity = random.randint(10, 30)
            cv2.line(img_array, (x1, y1), (x2, y2), (intensity, intensity, intensity), thickness)

    if random.random() < 0.1:
        shadow_intensity = random.randint(5, 15)
        direction = random.choice(['top', 'bottom', 'left', 'right'])
        if direction == 'top':
            img_array[:h // 8, :] = np.clip(img_array[:h // 8, :] - shadow_intensity, 0, 255)
        elif direction == 'bottom':
            img_array[7 * h // 8:, :] = np.clip(img_array[7 * h // 8:, :] - shadow_intensity, 0, 255)
        elif direction == 'left':
            img_array[:, :w // 8] = np.clip(img_array[:, :w // 8] - shadow_intensity, 0, 255)
        else:
            img_array[:, 7 * w // 8:] = np.clip(img_array[:, 7 * w // 8:] - shadow_intensity, 0, 255)

    return img_array


def apply_document_effects(img):
    """Применяет эффекты, характерные для отсканированных документов"""

    if random.random() < 0.3:
        blur_type = random.choice(['motion', 'gaussian', 'defocus'])
        if blur_type == 'motion':
            # Motion blur (размытие в движении) - ИСПРАВЛЕННАЯ ВЕРСИЯ
            size = random.choice([3, 5, 7])  # Только нечетные размеры
            kernel_motion_blur = np.zeros((size, size))
            kernel_motion_blur[int((size - 1) / 2), :] = np.ones(size)
            kernel_motion_blur = kernel_motion_blur / size

            img_array = np.array(img)
            img_array = cv2.filter2D(img_array, -1, kernel_motion_blur)
            img = Image.fromarray(img_array)

        elif blur_type == 'defocus':
            img = img.filter(ImageFilter.GaussianBlur(random.uniform(0.3, 0.8)))
        else:
            # Gaussian blur
            img = img.filter(ImageFilter.GaussianBlur(random.uniform(0.2, 0.5)))

    if random.random() < 0.25:
        try:
            quality = random.randint(30, 85)
            from io import BytesIO
            output = BytesIO()
            img.save(output, format='JPEG', quality=quality, optimize=True)
            img = Image.open(output)
        except Exception as e:
            print(f"⚠️ JPEG compression error: {e}")

    if random.random() < 0.1:
        try:
            skew = random.uniform(-0.1, 0.1)
            width, height = img.size
            xshift = abs(skew) * width
            new_width = width + int(xshift)
            img = img.transform((new_width, height), Image.AFFINE,
                                (1, skew, -xshift if skew > 0 else 0, 0, 1, 0))
        except Exception as e:
            print(f"⚠️ Skew error: {e}")

    return img


def generate_synthetic_data():
    output_dir = "./text/typed_text/az_config_train"
    os.makedirs(output_dir, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('train_number', type=int, help='Number of training images')
    parser.add_argument('test_number', type=int, help='Number of test images')
    parser.add_argument('--dataset', type=str, default='./az_words.txt', help='Path to dataset file')
    parser.add_argument('--format', type=str, default='both', choices=['txt', 'lmdb', 'both'], help='Output format')
    args = parser.parse_args()

    # Загружаем слова из датасета
    azerbaijani_words = load_words_from_dataset(args.dataset)
    if not azerbaijani_words:
        print("❌ Using fallback word list")
        azerbaijani_words = ["alma", "kitab", "ev", "şəhər", "adam"]

    fonts_dir = "./text/typed_text/az_config_train/fonts/3"

    print(f"🔍 Find fonts: {fonts_dir}")
    print(f"📊 Total unique words: {len(azerbaijani_words)}")

    # Разделяем слова на тренировочные и тестовые
    random.shuffle(azerbaijani_words)
    split_idx = int(0.8 * len(azerbaijani_words))

    train_words = azerbaijani_words[:split_idx]
    test_words = azerbaijani_words[split_idx:]

    print(f"📊 Words split: Train - {len(train_words)}, Test - {len(test_words)}")

    available_fonts = []
    if os.path.exists(fonts_dir):
        for file in os.listdir(fonts_dir):
            if file.lower().endswith('.ttf'):
                font_path = os.path.join(fonts_dir, file)
                try:
                    test_font = ImageFont.truetype(font_path, 20)
                    available_fonts.append(font_path)
                    print(f"✅ Font loaded: {file}")
                except Exception as e:
                    print(f"❌ Error font load: {file}: {e}")
    else:
        print(f"❌ Dir with fonts: {fonts_dir}")
        return

    if not available_fonts:
        print("❌ Not available fonts!")
        return

    print(f"🎯 Used {len(available_fonts)} fonts")

    # Цвета фона, характерные для документов
    document_backgrounds = [
        'white', '#f8f8f8', '#f0f0f0', '#f5f5f5', '#fafafa',
        '#fffaf0', '#fdf5e6', '#fff8dc',
        '#f0fff0', '#f5fffa', '#f0f8ff'
    ]

    def generate_images(word_list, count, prefix):
        """Генерирует изображения для заданного списка слов"""
        labels = []

        for i in range(count):
            word = random.choice(word_list)

            font_size = random.randint(18, 28)
            bg_color = random.choice(document_backgrounds)

            text_color_variants = [
                (0, 0, 0),
                (20, 20, 20),
                (30, 30, 30),
                (10, 10, 10),
                (15, 15, 15),
            ]
            text_color = random.choice(text_color_variants)

            rotation = random.randint(-2, 2)
            blur_radius = random.uniform(0, 0.2)
            contrast = random.uniform(0.9, 1.1)
            brightness = random.uniform(0.95, 1.05)

            try:
                font_path = random.choice(available_fonts)
                font = ImageFont.truetype(font_path, font_size)

                bbox = font.getbbox(word)
                text_width = bbox[2] - bbox[0] + 60
                text_height = bbox[3] - bbox[1] + 60

                img = Image.new('RGB', (text_width, text_height), color=bg_color)
                draw = ImageDraw.Draw(img)

                if random.random() < 0.05:
                    for y in range(img.height):
                        shade = 245 + int(10 * (y / img.height))
                        for x in range(img.width):
                            img.putpixel((x, y), (shade, shade, shade))

                x_offset = (img.width - (bbox[2] - bbox[0])) // 2
                y_offset = (img.height - (bbox[3] - bbox[1])) // 2
                draw.text((x_offset, y_offset), word, font=font, fill=text_color)

                try:
                    img = apply_document_effects(img)
                except Exception as e:
                    print(f"⚠️ Document effects skipped for '{word}': {e}")

                if rotation != 0:
                    img = img.rotate(rotation, expand=True, fillcolor=bg_color)

                if blur_radius > 0.03:
                    img = img.filter(ImageFilter.GaussianBlur(blur_radius))

                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)

                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)

                img_array = np.array(img)

                try:
                    img_array = add_document_noise(img_array)
                except Exception as e:
                    print(f"⚠️ Document noise skipped for '{word}': {e}")

                if random.random() < 0.2:
                    noise = np.random.normal(0, random.randint(1, 4), img_array.shape).astype('uint8')
                    img_array = cv2.add(img_array, noise)

                final_width, final_height = 320, 48
                img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

                if random.random() < 0.15:
                    img_resized = cv2.GaussianBlur(img_resized, (3, 3), 0)

                filename = f"{prefix}_{i:07d}.jpg"
                cv2.imwrite(os.path.join(output_dir, filename), img_resized)

                labels.append(f"{filename}\t{word}")

                if (i + 1) % 500 == 0:
                    print(f"✅ {prefix}: {i + 1}/{count}")

            except Exception as e:
                print(f"❌ {prefix} gen error for word '{word}': {e}")
                continue

        return labels

    print("🚀 Generating training data...")
    labels_train = generate_images(train_words, args.train_number, "train")

    print("🧪 Generating test data...")
    labels_test = generate_images(test_words, args.test_number, "test")

    # Сохраняем в текстовые файлы (опционально)
    with open(os.path.join(output_dir, "train_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels_train:
            f.write(label + '\n')

    with open(os.path.join(output_dir, "val_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels_test:
            f.write(label + '\n')

    # Создаем LMDB датасеты
    print("🗄️ Creating LMDB datasets...")
    create_lmdb_dataset(labels_train, os.path.join(output_dir, "train.lmdb"), output_dir)
    create_lmdb_dataset(labels_test, os.path.join(output_dir, "val.lmdb"), output_dir)

    unique_train_words = len(set([label.split('\t')[1] for label in labels_train]))
    unique_test_words = len(set([label.split('\t')[1] for label in labels_test]))

    print(f"\n🎉 Generation completed!")
    print(f"📊 Training: {len(labels_train)} images, {unique_train_words} unique words")
    print(f"📊 Val: {len(labels_test)} images, {unique_test_words} unique words")
    print(
        f"📊 Coverage: {unique_train_words / len(train_words) * 100:.1f}% train words, {unique_test_words / len(test_words) * 100:.1f}% test words")


generate_synthetic_data()
