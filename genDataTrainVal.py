import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import argparse


def generate_synthetic_data():
    output_dir = "./text/typed_text/az_config_train"
    os.makedirs(output_dir, exist_ok=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    args = parser.parse_args()

    fonts_dir = "./text/typed_text/az_config_train/fonts/3"

    print(f"🔍 Find fonts: {fonts_dir}")

    azerbaijani_words = [
        # 1. Базовые бытовые слова (100+ слов)
        "adam", "alma", "ana", "ata", "ev", "kitab", "qələm", "stol", "stul", "qapı",
        "pəncərə", "şəhər", "kənd", "yol", "maşın", "avtobus", "metro", "uşaq", "böyük",
        "kiçik", "yeni", "köhnə", "gözəl", "çirkin", "isti", "soyuq", "isti", "sərin",

        # 2. Семья и отношения (50+ слов)
        "ata", "ana", "bacı", "qardaş", "oğul", "qız", "nəvə", "bala", "əmi", "dayı",
        "xala", "bibi", "yoldaş", "ər", "arvad", "sevgili", "dost", "rəfiqə",

        # 3. Еда и напитки (80+ слов)
        "çörək", "pendir", "ət", "balıq", "toyuq", "süd", "su", "çay", "qəhvə", "şirniyyat",
        "düyü", "şorba", "tərəvəz", "meyvə", "alma", "armud", "şaftalı", "ərık", "qarpız",
        "pomidor", "xiyar", "soğan", "sarımsaq", "duz", "istiot", "yağ", "ball",

        # 4. Природа и география (100+ слов)
        "dağ", "dəniz", "çay", "göl", "meşə", "ağac", "gül", "çiçək", "günəş", "ay",
        "ulduz", "bulud", "yağış", "qar", "külək", "fırtına", "havа", "torpaq", "qum",
        "Bakı", "Gəncə", "Sumqayıt", "Naxçıvan", "Şəki", "Lənkəran", "Quba", "Xəzər",

        # 5. Профессии и работа (80+ слов)
        "həkim", "müəllim", "mühəndis", "tələbə", "şagird", "işçi", "fermer", "tacir",
        "sürücü", "polis", "əsgər", "rəssam", "yazıçı", "şair", "jurnalist", "aktyor",

        # 6. Цвета и описания (50+ слов)
        "qırmızı", "yaşıl", "mavi", "sarı", "qara", "ağ", "boz", "tünd", "açıq", "təmiz",
        "çirkli", "parlaq", "tər", "quru", "isti", "soyuq", "yumşaq", "sərt",

        # 7. Время и числа (60+ слов)
        "il", "ay", "həftə", "gün", "saat", "dəqiqə", "saniyə", "səhər", "günorta", "axşam",
        "gecə", "bir", "iki", "üç", "dörd", "beş", "altı", "yeddi", "səkkiz", "doqquz", "on",

        # 8. Глаголы и действия (100+ слов)
        "getmək", "gəlmək", "oxumaq", "yazmaq", "işləmək", "oynamaq", "yemək", "içmək",
        "görmək", "eşitmək", "danışmaq", "gülmək", "ağlamaq", "yatmaq", "oyanmaq",

        # 9. Абстрактные понятия (80+ слов)
        "sevgi", "nifrət", "xoşbəxtlik", "kədər", "qəzəb", "səbir", "ümüd", "qorxu",
        "cəsarət", "ədəb", "hörmət", "lütf", "şəfqət", "mərhəmət", "insaf",

        # 10. Техника и современность (70+ слов)
        "kompüter", "telefon", "internet", "proqram", "sistem", "şəbəkə", "maşın",
        "avtomat", "robot", "texnologiya", "elmi", "tədqiqat", "kəşf",

        # 11. Одежда и аксессуары (50+ слов)
        "paltar", "köynək", "şalvar", "ceket", "pencək", "ayaqqabı", "çəkmə", "başlıq",
        "şəlyak", "qolbaq", "saat", "üzük", "boyunbağı",

        # 12. Образование и наука (60+ слов)
        "məktəb", "universitet", "institut", "təhsil", "təlim", "dərs", "kitab", "dəftər",
        "imtahan", "qiymət", "diplom", "dərəcə", "elmi", "tədqiqat"
    ]
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

    backgrounds = ['white', 'lightgray', 'aliceblue', 'seashell']

    generated_count = 0
    labels = []

    for i in range(args.number):
        word = random.choice(azerbaijani_words)

        font_size = random.randint(22, 32)
        bg_color = random.choice(backgrounds)
        text_color = (
            random.randint(0, 80),
            random.randint(0, 80),
            random.randint(0, 80)
        )

        rotation = random.randint(-3, 3)
        blur_radius = random.uniform(0, 0.3)
        contrast = random.uniform(0.9, 1.2)
        brightness = random.uniform(0.9, 1.1)

        try:
            word_to_draw = word

            font_path = random.choice(available_fonts)
            font = ImageFont.truetype(font_path, font_size)

            bbox = font.getbbox(word_to_draw)
            text_width = bbox[2] - bbox[0] + 40
            text_height = bbox[3] - bbox[1] + 40

            img = Image.new('RGB', (text_width, text_height), color=bg_color)
            draw = ImageDraw.Draw(img)

            if random.random() < 0.1:  # Только 10% случаев
                for y in range(img.height):
                    shade = 240 + int(10 * (y / img.height))
                    for x in range(img.width):
                        img.putpixel((x, y), (shade, shade, shade))

            x_offset = (img.width - (bbox[2] - bbox[0])) // 2
            y_offset = (img.height - (bbox[3] - bbox[1])) // 2
            draw.text((x_offset, y_offset), word_to_draw, font=font, fill=text_color)

            if rotation != 0:
                img = img.rotate(rotation, expand=True, fillcolor=bg_color)

            if blur_radius > 0.05:
                img = img.filter(ImageFilter.GaussianBlur(blur_radius))

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)

            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)

            img_array = np.array(img)

            if random.random() < 0.3:
                noise_type = random.choice(['gaussian', 'none'])
                if noise_type == 'gaussian':
                    noise = np.random.normal(0, random.randint(1, 5), img_array.shape).astype('uint8')
                    img_array = cv2.add(img_array, noise)

            final_width, final_height = 320, 48

            img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

            filename = f"synthetic_{i:05d}.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), img_resized)

            labels.append(f"{filename}\t{word}")
            generated_count += 1

            if generated_count % 10 == 0:
                print(f"Generated: {generated_count}")

        except Exception as e:
            print(f"Gen error: {e}")
            continue

    random.shuffle(labels)
    split_idx = int(0.9 * len(labels))

    with open(os.path.join(output_dir, "train_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels[:split_idx]:
            f.write(label + '\n')

    with open(os.path.join(output_dir, "val_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels[split_idx:]:
            f.write(label + '\n')

    print(f"✅ Generated {generated_count} synt data")
    print(f"📊 Train: {split_idx}, Val: {len(labels) - split_idx}")


generate_synthetic_data()
