# from PIL import Image, ImageDraw, ImageFont
# import textwrap
# import random
# import datetime
#
#
# def generate_realistic_azerbaijani_text():
#     """Генерирует более реалистичный азербайджанский текст для документов"""
#
#     # Реалистичные данные для документов
#     document_types = [
#         "Şəxsiyyət vəsiqəsi",
#         "Doğum şəhadətnaməsi",
#         "Yaşayış yerinin spravkası",
#         "Əmək kitabçası",
#         "Təhsil haqqında arayış"
#     ]
#
#     cities = ["Bakı", "Gəncə", "Sumqayıt", "Mingəçevir", "Şirvan", "Naxçıvan", "Şəki"]
#     regions = ["Səbail", "Nəsimi", "Nərimanov", "Xətai", "Yasamal", "Binəqədi"]
#     streets = ["Nizami küçəsi", "Füzuli prospekti", "Xətai küçəsi", "28 May küçəsi"]
#
#     # Генерация реалистичного содержания
#     content = f"""
# AZƏRBAYCAN RESPUBLİKASI
# {document_types[random.randint(0, len(document_types) - 1)]}
#
# Şəxsi məlumatlar:
# Ad: ƏLİ
# Soyad: HƏSƏNOV
# Ata adı: VƏLİ
# Doğum tarixi: {random.randint(1, 28)}.{random.randint(1, 12)}.{random.randint(1960, 2000)}
# Doğum yeri: {cities[random.randint(0, len(cities) - 1)]} şəhəri
#
# Qeydiyyat ünvanı:
# Şəhər: {cities[random.randint(0, len(cities) - 1)]}
# Rayon: {regions[random.randint(0, len(regions) - 1)]}
# Küçə: {streets[random.randint(0, len(streets) - 1)]}
# Ev: {random.randint(1, 150)}
# Mənzil: {random.randint(1, 100)}
#
# Sənədin verilmə tarixi: {datetime.datetime.now().strftime('%d.%m.%Y')}
# Sənədin etibarlılıq müddəti: {(datetime.datetime.now() + datetime.timedelta(days=365)).strftime('%d.%m.%Y')}
#
# Qeyd: Bu sənəd rəsmi sənəd kimi istifadə edilə bilər.
# Sənədin nömrəsi: {random.randint(100000, 999999)}
# Qeydiyyat kodu: AZ{random.randint(1000, 9999)}
#
# Rəsmiləşdirən orqan: Azərbaycan Respublikası Ədliyyə Nazirliyi
# Vəsiqənin seriyası: {chr(random.randint(65, 90))}{chr(random.randint(65, 90))}
# Nömrə: {random.randint(100000, 999999)}
# """
#
#     return content
#
#
# def create_professional_document():
#     """Создает профессионально выглядящий документ"""
#
#     # Размеры A4
#     width, height = 2480, 3508
#     image = Image.new('RGB', (width, height), 'white')
#     draw = ImageDraw.Draw(image)
#
#     margin = 200
#     text_width = width - 2 * margin
#
#     # Получаем текст
#     text = generate_realistic_azerbaijani_text()
#
#     try:
#         # Основной шрифт
#         font_path = "arial.ttf"
#         font = ImageFont.truetype(font_path, 32)
#         title_font = ImageFont.truetype(font_path, 42)
#         header_font = ImageFont.truetype(font_path, 36)
#
#     except:
#         font = ImageFont.load_default()
#         title_font = ImageFont.load_default()
#         header_font = ImageFont.load_default()
#
#     # Разделяем текст на строки
#     lines = text.split('\n')
#     y_position = margin
#
#     for i, line in enumerate(lines):
#         if not line.strip():
#             y_position += 40
#             continue
#
#         # Выбираем шрифт в зависимости от типа строки
#         if i == 0 or "AZƏRBAYCAN" in line:
#             current_font = title_font
#             fill = 'black'
#         elif line.strip().endswith(':'):
#             current_font = header_font
#             fill = 'darkblue'
#         else:
#             current_font = font
#             fill = 'black'
#
#         # Центрируем заголовки
#         if i < 2:
#             bbox = draw.textbbox((0, 0), line, font=current_font)
#             text_width_line = bbox[2] - bbox[0]
#             x_position = margin + (text_width - text_width_line) / 2
#         else:
#             x_position = margin
#
#         draw.text((x_position, y_position), line, font=current_font, fill=fill)
#
#         bbox = draw.textbbox((0, 0), line, font=current_font)
#         text_height = bbox[3] - bbox[1]
#         y_position += text_height + 15
#
#     # Добавляем печать
#     seal_radius = 80
#     seal_x = width - margin - seal_radius
#     seal_y = height - margin - 150
#
#     # Рисуем круг печати
#     draw.ellipse([
#         seal_x - seal_radius, seal_y - seal_radius,
#         seal_x + seal_radius, seal_y + seal_radius
#     ], outline='red', width=4)
#
#     # Текст печати
#     seal_text = "AZƏRBAYCAN RESPUBLİKASI"
#     seal_font = ImageFont.truetype(font_path, 20) if font != ImageFont.load_default() else font
#
#     # Сохраняем
#     output_path = "professional_azerbaijani_document.png"
#     image.save(output_path, 'PNG', dpi=(300, 300))
#     print(f"Профессиональный документ сохранен как: {output_path}")
#
#     return output_path
#
#
# # Запуск
# if __name__ == "__main__":
#     create_professional_document()

import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse


def load_words_from_dataset(dataset_path):
    """Loads words from dataset file - reads text file, extracts words, filters by length"""
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


def generate_words_per_font():
    """Generates N random words for each font"""
    output_dir = "./text/typed_text/az_config_train"
    os.makedirs(output_dir, exist_ok=True)

    dataset_path = './train_cleaned.txt'

    parser = argparse.ArgumentParser(description='Generate N random words for each font')
    parser.add_argument('words_per_font', type=int, help='Number of words to generate per font')
    parser.add_argument('--dataset', type=str, default=dataset_path, help='Path to dataset file')
    args = parser.parse_args()

    azerbaijani_words = load_words_from_dataset(args.dataset)
    if not azerbaijani_words:
        print("❌ No words loaded from dataset!")
        return

    fonts_dir = "./text/typed_text/fonts/3"

    print(f"🔍 Looking for fonts in: {fonts_dir}")
    print(f"📊 Total unique words available: {len(azerbaijani_words)}")
    print(f"🎯 Generating {args.words_per_font} words per font")

    available_fonts = []
    if os.path.exists(fonts_dir):
        for file in os.listdir(fonts_dir):
            if file.lower().endswith('.ttf'):
                font_path = os.path.join(fonts_dir, file)
                try:
                    # Test if font can be loaded
                    test_font = ImageFont.truetype(font_path, 20)
                    available_fonts.append(font_path)
                    print(f"✅ Font loaded: {file}")
                except Exception as e:
                    print(f"❌ Error loading font {file}: {e}")
    else:
        print(f"❌ Fonts directory not found: {fonts_dir}")
        return

    if not available_fonts:
        print("❌ No available fonts!")
        return

    print(f"\n🎯 Found {len(available_fonts)} fonts. Generating {args.words_per_font} words for each font...")

    # Document backgrounds
    document_backgrounds = [
        'white', '#f8f8f8', '#f0f0f0', '#f5f5f5', '#fafafa',
        '#fffaf0', '#fdf5e6', '#fff8dc',
        '#f0fff0', '#f5fffa', '#f0f8ff'
    ]

    # Text color variants
    text_color_variants = [
        (0, 0, 0), (20, 20, 20), (30, 30, 30),
        (10, 10, 10), (15, 15, 15)
    ]

    def create_text_image(word, font_path, font_size=24):
        """Creates text image with given word and font"""
        try:
            font = ImageFont.truetype(font_path, font_size)
            font_name = os.path.splitext(os.path.basename(font_path))[0]

            # Calculate text dimensions
            bbox = font.getbbox(word)
            text_actual_width = bbox[2] - bbox[0]
            text_actual_height = bbox[3] - bbox[1]

            # Add padding
            padding = 20
            text_width = text_actual_width + padding * 2
            text_height = text_actual_height + padding * 2

            # Ensure minimum dimensions
            text_width = max(text_width, 200)
            text_height = max(text_height, 60)

            # Create image
            bg_color = random.choice(document_backgrounds)
            img = Image.new('RGB', (text_width, text_height), color=bg_color)
            draw = ImageDraw.Draw(img)

            text_color = random.choice(text_color_variants)

            # Center the text
            x_offset = (text_width - text_actual_width) // 2
            y_offset = (text_height - text_actual_height) // 2

            draw.text((x_offset, y_offset), word, font=font, fill=text_color)

            return img, font_name

        except Exception as e:
            print(f"❌ Error creating text image for '{word}' with font {font_path}: {e}")
            return None, None

    # Create labels file
    labels = []

    # Track used words per font to avoid duplicates
    used_words_per_font = {}

    for font_path in available_fonts:
        font_name = os.path.splitext(os.path.basename(font_path))[0]
        print(f"\n🔄 Processing font: {font_name}")

        # Initialize used words set for this font
        used_words_per_font[font_name] = set()

        words_generated = 0
        attempts = 0
        max_attempts = args.words_per_font * 3  # Prevent infinite loop

        while words_generated < args.words_per_font and attempts < max_attempts:
            word = random.choice(azerbaijani_words)

            # Skip if word already used for this font
            if word in used_words_per_font[font_name]:
                attempts += 1
                continue

            try:
                # Random font size for variety
                font_size = random.randint(20, 32)

                img, actual_font_name = create_text_image(word, font_path, font_size)
                if img is None:
                    attempts += 1
                    continue

                # Optional: Apply slight rotation occasionally
                if random.random() < 0.2:
                    rotation = random.randint(-2, 2)
                    if rotation != 0:
                        img = img.rotate(rotation, expand=True, fillcolor=random.choice(document_backgrounds))

                # Convert to array for OpenCV and resize if needed
                img_array = np.array(img)

                # Ensure reasonable dimensions (resize if too large)
                h, w = img_array.shape[:2]
                if w > 400 or h > 100:
                    scale_factor = min(400 / w, 100 / h)
                    new_w = int(w * scale_factor)
                    new_h = int(h * scale_factor)
                    img_array = cv2.resize(img_array, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

                # Save image
                filename = f"{font_name}_{words_generated:04d}.png"
                filepath = os.path.join(output_dir, filename)
                cv2.imwrite(filepath, img_array)

                # Add to labels
                labels.append(f"{filename}\t{word}")
                used_words_per_font[font_name].add(word)
                words_generated += 1
                attempts = 0

                if words_generated % 10 == 0:
                    print(f"✅ Generated {words_generated}/{args.words_per_font} for {font_name}")

            except Exception as e:
                print(f"❌ Error generating word '{word}' for font {font_name}: {e}")
                attempts += 1
                continue

        print(f"🎉 Completed: {words_generated} words for {font_name}")

    # Save labels file
    labels_file = os.path.join(output_dir, "labels.txt")
    with open(labels_file, 'w', encoding='utf-8') as f:
        for label in labels:
            f.write(label + '\n')

    # Generate summary
    total_images = len(labels)
    unique_words_used = len(set([label.split('\t')[1] for label in labels]))

    print(f"\n🎉 Generation completed!")
    print(f"📊 Total images generated: {total_images}")
    print(f"📊 Unique words used: {unique_words_used}")
    print(f"📊 Fonts processed: {len(available_fonts)}")
    print(f"📁 Output directory: {output_dir}")
    print(f"📝 Labels file: {labels_file}")

    # Print per-font statistics
    print(f"\n📈 Per-font statistics:")
    for font_path in available_fonts:
        font_name = os.path.splitext(os.path.basename(font_path))[0]
        font_words = len(used_words_per_font[font_name])
        print(f"   {font_name}: {font_words} words")


if __name__ == "__main__":
    generate_words_per_font()