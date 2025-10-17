import os
import random
from PIL import Image, ImageDraw, ImageFont


def generate_ocr_dataset_from_file():
    # Создаем папки
    os.makedirs('./text/typed_text/az_config_train', exist_ok=True)

    # Читаем слова из файла
    print("Чтение слов из файла...")
    with open('./az_words.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Парсим слова (предполагаем формат "слово частота")
    az_words = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) >= 1:
            word = parts[0]
            # Берем только слова подходящей длины
            if 2 <= len(word) <= 20:
                az_words.append(word)

    print(f"Загружено {len(az_words)} слов")

    # Случайно выбираем слова для train и val
    random.seed(42)  # для воспроизводимости
    selected_words = random.sample(az_words, 100)  # 100 случайных слов

    # Разделяем на train и val
    train_words = selected_words[:80]  # 80 слов для train
    val_words = selected_words[80:]  # 20 слов для val

    print(f"Выбрано: {len(train_words)} train слов, {len(val_words)} val слов")

    # Шрифты
    try:
        fonts = [
            ImageFont.truetype("arial.ttf", 32),
            ImageFont.truetype("arial.ttf", 40),
            ImageFont.truetype("arial.ttf", 28),
            ImageFont.truetype("times.ttf", 36),
            ImageFont.truetype("times.ttf", 32),
        ]
    except:
        fonts = [ImageFont.load_default()] * 5
        print("Используются стандартные шрифты")

    text_colors = ['black', 'blue', 'darkred', 'darkgreen', 'purple']
    bg_colors = ['white', 'lightgray', 'lightyellow', 'lightblue']

    train_lines = []
    val_lines = []

    print("Генерация TRAIN изображений...")
    # Train: 80 слов × 5 изображений = 400
    for i, word in enumerate(train_words):
        for j in range(5):
            img = Image.new('RGB', (200, 64), color=random.choice(bg_colors))
            draw = ImageDraw.Draw(img)
            font = random.choice(fonts)
            text_color = random.choice(text_colors)

            bbox = draw.textbbox((0, 0), word, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (200 - text_width) // 2
            y = (64 - text_height) // 2

            draw.text((x, y), word, fill=text_color, font=font)
            filename = f"train_{i + 1:03d}_{j + 1:02d}.jpg"
            img_path = f'./text/typed_text/az_config_train/{filename}'
            img.save(img_path)
            train_lines.append(f"images/{filename} {word}\n")

    print("Генерация VAL изображений...")
    # Val: 20 слов × 1 изображение = 20
    for i, word in enumerate(val_words):
        img = Image.new('RGB', (200, 64), color=random.choice(bg_colors))
        draw = ImageDraw.Draw(img)
        font = random.choice(fonts)
        text_color = random.choice(text_colors)

        bbox = draw.textbbox((0, 0), word, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (200 - text_width) // 2
        y = (64 - text_height) // 2

        draw.text((x, y), word, fill=text_color, font=font)
        filename = f"val_{i + 1:03d}.jpg"
        img_path = f'./text/typed_text/az_config_train/{filename}'
        img.save(img_path)
        val_lines.append(f"images/{filename} {word}\n")

    # Сохраняем списки
    with open('./text/typed_text/az_config_train/train_list.txt', 'w', encoding='utf-8') as f:
        f.writelines(train_lines)

    with open('./text/typed_text/az_config_train/val_list.txt', 'w', encoding='utf-8') as f:
        f.writelines(val_lines)

    # Создаем словарь из ВСЕХ символов
    all_chars = set()
    for word in selected_words:
        all_chars.update(word)

    char_list = sorted(list(all_chars))
    with open('./text/typed_text/az_config_train/dict.txt', 'w', encoding='utf-8') as f:
        for char in char_list:
            f.write(char + '\n')

    print(f"Сгенерировано:")
    print(f"- Train: {len(train_words)} слов, {len(train_lines)} изображений")
    print(f"- Val: {len(val_words)} слов, {len(val_lines)} изображений")
    print(f"- Всего уникальных символов: {len(char_list)}")
    print(f"- Примеры train слов: {train_words[:10]}")
    print(f"- Примеры val слов: {val_words[:10]}")


if __name__ == "__main__":
    generate_ocr_dataset_from_file()