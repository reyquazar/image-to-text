import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont


def generate_synthetic_data():
    output_dir = "synthetic_dataset"
    os.makedirs(output_dir, exist_ok=True)

    # Словарь азербайджанских кириллических слов
    azerbaijani_words = [
        "район", "республика", "шәһәр", "кәнд", "вилајәт", "өлкә",
        "район", "область", "республика", "шәһәр", "кәнд", "вилајәт",
        "административ", "территориал", "бөлгү", "ҹәмијјәт", "мухтар",
        "әһали", "населен", "место", "јашајыш", "јерлешмә", "гурту",
        "дәјәш", "гәдәбәј", "шағыр", "гүзәк", "тәпә", "чәләби",
        "дәһә", "гәдәбәј", "бәлгән", "ҹәбраил", "ғубалы", "дәвәчи",
        "һаҹығabul", "бейләган", "гөйгөл", "дәшкәсән", "ғоҹа", "иммет"
    ]

    # Шрифты (можно скачать дополнительные)
    fonts = ["arial.ttf", "times.ttf"]  # Добавьте больше шрифтов

    generated_count = 0
    labels = []

    for i in range(500):  # Генерируем 500 примеров
        word = random.choice(azerbaijani_words)
        font_size = random.randint(20, 35)

        try:
            # Создаем изображение с текстом
            font = ImageFont.truetype(random.choice(fonts), font_size)

            # Вычисляем размер текста
            bbox = font.getbbox(word)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Создаем изображение
            img = Image.new('RGB', (text_width + 20, text_height + 20), color='white')
            draw = ImageDraw.Draw(img)

            # Добавляем текст
            text_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
            draw.text((10, 10), word, font=font, fill=text_color)

            # Добавляем шум
            img_array = np.array(img)
            noise = np.random.randint(0, 50, img_array.shape, dtype='uint8')
            img_array = cv2.add(img_array, noise)

            # Сохраняем
            filename = f"synthetic_{i:04d}.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), img_array)

            labels.append(f"{filename}\t{word}")
            generated_count += 1

            if generated_count % 50 == 0:
                print(f"Сгенерировано: {generated_count}")

        except Exception as e:
            print(f"Ошибка генерации: {e}")
            continue

    # Сохраняем labels
    with open(os.path.join(output_dir, "labels.txt"), 'w', encoding='utf-8') as f:
        for label in labels:
            f.write(label + '\n')

    print(f"✅ Сгенерировано {generated_count} синтетических примеров")


generate_synthetic_data()