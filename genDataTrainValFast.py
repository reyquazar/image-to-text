import os
import random
from PIL import Image, ImageDraw, ImageFont


def generate_ocr_dataset_correct():
    # Создаем папки
    os.makedirs('./text/typed_text/az_config_train', exist_ok=True)

    # Азербайджанские слова для теста
    az_words = [
        "kitab", "ev", "maşın", "qələm", "stol",
        "şəhər", "çiçək", "gün", "ay", "il",
        "su", "od", "hava", "torpaq", "ağac",
        "uşaq", "məktəb", "müəllim", "tələbə", "dərs",
        "ana", "ata", "qardaş", "bacı", "ailə",
        "yemək", "çay", "çörək", "pendir", "bal",
        "kitabxana", "hospital", "park", "küçə", "bazar",
        "avtomobil", "avtobus", "təyyarə", "gəmi", "velosiped"
    ]

    # Разделяем на train и val СЛОВА
    train_words = az_words[:30]  # 30 слов для train
    val_words = az_words[30:]  # 10 слов для val

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
    # Train: 30 слов × 5 изображений = 150 (разные вариации)
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
            filename = f"train_{i + 1:02d}_{j + 1:02d}.jpg"
            img_path = f'./text/typed_text/az_config_train/{filename}'
            img.save(img_path)
            train_lines.append(f"images/{filename} {word}\n")

    print("Генерация VAL изображений...")
    # Val: 10 слов × 1 изображение = 10 (только для проверки)
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
        filename = f"val_{i + 1:02d}.jpg"
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
    for word in az_words:
        all_chars.update(word)

    char_list = sorted(list(all_chars))
    with open('./text/typed_text/az_config_train/dict.txt', 'w', encoding='utf-8') as f:
        for char in char_list:
            f.write(char + '\n')

    print(f"Сгенерировано:")
    print(f"- Train: {len(train_words)} слов, {len(train_lines)} изображений")
    print(f"- Val: {len(val_words)} слов, {len(val_lines)} изображений")
    print(f"- Всего: {len(az_words)} уникальных слов")
    print(f"- Train слова: {train_words}")
    print(f"- Val слова: {val_words}")


if __name__ == "__main__":
    generate_ocr_dataset_correct()