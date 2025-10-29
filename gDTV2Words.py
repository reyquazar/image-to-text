import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
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


def add_document_noise(img_array):
    """Adds document-like noise:
    - Random spots (ink splatters, dust particles)
    - Random lines (scratches, pen marks)
    - Shadows (uneven lighting during scanning)"""
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
    """Applies document scanning effects:
    - Blur effects (motion blur, defocus blur, Gaussian blur)
    - JPEG/PNG compression artifacts
    - Skew distortion (misaligned scanning)"""
    if random.random() < 0.3:
        blur_type = random.choice(['motion', 'gaussian', 'defocus'])
        if blur_type == 'motion':
            pass
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
            img.save(output, format='PNG', quality=quality, optimize=True)
            img = Image.open(output)
            img = img.copy()
            output.close()
        except Exception as e:
            print(f"⚠️ PNG compression error: {e}")

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


def apply_advanced_augmentations(img_array):
    """Applies advanced image augmentations:
    - Elastic distortions
    - Perspective transformations
    - Random erasing
    - Color jittering
    - Noise variations"""
    h, w = img_array.shape[:2]

    # Elastic distortions
    if random.random() < 0.1:
        try:
            alpha = random.randint(20, 40)
            sigma = random.randint(4, 6)
            dx = np.random.uniform(-1, 1, (h, w)) * alpha
            dy = np.random.uniform(-1, 1, (h, w)) * alpha

            x, y = np.meshgrid(np.arange(w), np.arange(h))
            indices = np.reshape(y + dy, (-1, 1)), np.reshape(x + dx, (-1, 1))

            img_array = cv2.remap(img_array, indices[1].astype(np.float32),
                                  indices[0].astype(np.float32),
                                  cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        except Exception as e:
            print(f"⚠️ Elastic distortion error: {e}")

    # Perspective transformation
    if random.random() < 0.08:
        try:
            pts1 = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
            max_offset = w * 0.05
            pts2 = np.float32([
                [random.uniform(-max_offset, max_offset), random.uniform(-max_offset, max_offset)],
                [w - random.uniform(-max_offset, max_offset), random.uniform(-max_offset, max_offset)],
                [random.uniform(-max_offset, max_offset), h - random.uniform(-max_offset, max_offset)],
                [w - random.uniform(-max_offset, max_offset), h - random.uniform(-max_offset, max_offset)]
            ])
            matrix = cv2.getPerspectiveTransform(pts1, pts2)
            img_array = cv2.warpPerspective(img_array, matrix, (w, h), borderMode=cv2.BORDER_REPLICATE)
        except Exception as e:
            print(f"⚠️ Perspective transformation error: {e}")

    # Random erasing (cutout)
    if random.random() < 0.1:
        try:
            erase_h = random.randint(5, 15)
            erase_w = random.randint(5, 30)
            erase_x = random.randint(0, w - erase_w)
            erase_y = random.randint(0, h - erase_h)
            img_array[erase_y:erase_y + erase_h, erase_x:erase_x + erase_w] = random.randint(200, 255)
        except Exception as e:
            print(f"⚠️ Random erasing error: {e}")

    # Color variations
    if random.random() < 0.3:
        try:
            # Convert to HSV for color manipulation
            hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)
            hsv = hsv.astype(np.float32)

            # Hue shift
            hsv[:, :, 0] = (hsv[:, :, 0] + random.uniform(-5, 5)) % 180

            # Saturation adjustment
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * random.uniform(0.8, 1.2), 0, 255)

            # Value adjustment
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * random.uniform(0.9, 1.1), 0, 255)

            hsv = hsv.astype(np.uint8)
            img_array = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        except Exception as e:
            print(f"⚠️ Color variation error: {e}")

    return img_array


def generate_synthetic_data():
    """Main function - generates synthetic text images with document-like appearance for training/validation"""
    output_dir = "./text/typed_text/az_config_train"
    os.makedirs(output_dir, exist_ok=True)

    dataset_path = './train_cleaned.txt'

    parser = argparse.ArgumentParser()
    parser.add_argument('train_number', type=int, help='Number of training images')
    parser.add_argument('val_number', type=int, help='Number of val images')
    parser.add_argument('--dataset', type=str, default=dataset_path, help='Path to dataset file')
    args = parser.parse_args()

    azerbaijani_words = load_words_from_dataset(args.dataset)

    fonts_dir = "./text/typed_text/fonts/3"

    print(f"🔍 Find fonts: {fonts_dir}")
    print(f"📊 Total unique words: {len(azerbaijani_words)}")

    random.shuffle(azerbaijani_words)
    split_idx = int(0.8 * len(azerbaijani_words))

    train_words = azerbaijani_words[:split_idx]
    val_words = azerbaijani_words[split_idx:]

    print(f"📊 Words split: Train - {len(train_words)}, val - {len(val_words)}")

    available_fonts = []
    if os.path.exists(fonts_dir):
        for file in os.listdir(fonts_dir):
            if file.lower().endswith('.ttf'):
                font_path = os.path.join(fonts_dir, file)
                try:
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

    def generate_single_word_image(word, font, font_size, bg_color, text_color, text_width, text_height):
        """Generates image with single word"""
        img = Image.new('RGB', (text_width, text_height), color=bg_color)
        draw = ImageDraw.Draw(img)

        if random.random() < 0.05:
            for y in range(img.height):
                shade = 245 + int(10 * (y / img.height))
                for x in range(img.width):
                    img.putpixel((x, y), (shade, shade, shade))

        bbox = font.getbbox(word)
        x_offset = (img.width - (bbox[2] - bbox[0])) // 2
        y_offset = (img.height - (bbox[3] - bbox[1])) // 2
        draw.text((x_offset, y_offset), word, font=font, fill=text_color)

        return img, word

    def generate_double_word_image(word1, word2, font, font_size, bg_color, text_color, text_width, text_height):
        """Generates image with two words"""
        img = Image.new('RGB', (text_width, text_height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Gradient background (occasionally)
        if random.random() < 0.05:
            for y in range(img.height):
                shade = 245 + int(10 * (y / img.height))
                for x in range(img.width):
                    img.putpixel((x, y), (shade, shade, shade))

        # Combine words with random separator
        separators = [' ', '  ', '   ', '    ', ' - ', ' • ', ' | ']
        separator = random.choice(separators)
        combined_text = word1 + separator + word2

        bbox = font.getbbox(combined_text)

        # If text is too long, reduce font size
        max_width = text_width - 40
        if bbox[2] - bbox[0] > max_width:
            font_size = max(12, int(font_size * 0.8))
            font = ImageFont.truetype(font.path, font_size)
            bbox = font.getbbox(combined_text)

        x_offset = (img.width - (bbox[2] - bbox[0])) // 2
        y_offset = (img.height - (bbox[3] - bbox[1])) // 2
        draw.text((x_offset, y_offset), combined_text, font=font, fill=text_color)

        return img, combined_text

    def generate_images(word_list, count, prefix):
        """Generates images for given word list with augmentations"""
        labels = []
        single_word_count = int(count * 0.7)  # 70% single words
        double_word_count = count - single_word_count  # 30% double words

        print(f"📝 Generating {single_word_count} single-word and {double_word_count} double-word images for {prefix}")

        # Generate single word images
        for i in range(single_word_count):
            word = random.choice(word_list)

            font_size = random.randint(18, 32)
            bg_color = random.choice(document_backgrounds)

            text_color_variants = [
                (0, 0, 0),
                (20, 20, 20),
                (30, 30, 30),
                (10, 10, 10),
                (15, 15, 15),
            ]
            text_color = random.choice(text_color_variants)

            # Augmentation parameters
            rotation = random.randint(-5, 5)
            blur_radius = random.uniform(0, 0.1)
            contrast = random.uniform(0.9, 1.1)
            brightness = random.uniform(0.95, 1.05)

            try:
                font_path = random.choice(available_fonts)
                font = ImageFont.truetype(font_path, font_size)

                text_width = 320
                text_height = 48

                img, final_text = generate_single_word_image(word, font, font_size, bg_color, text_color, text_width,
                                                             text_height)

                # Apply augmentations
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

                # Apply advanced augmentations
                if random.random() < 0.4:
                    img_array = apply_advanced_augmentations(img_array)

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

                filename = f"{prefix}_single_{i:09d}.png"
                cv2.imwrite(os.path.join(output_dir, filename), img_resized)

                labels.append(f"{filename}\t{final_text}")

                if (i + 1) % 1000 == 0:
                    print(f"✅ {prefix} single-word: {i + 1}/{single_word_count}")

            except Exception as e:
                print(f"❌ {prefix} single-word gen error for word '{word}': {e}")
                continue

        # Generate double word images
        for i in range(double_word_count):
            word1 = random.choice(word_list)
            word2 = random.choice(word_list)

            # Avoid same words
            while word2 == word1:
                word2 = random.choice(word_list)

            font_size = random.randint(16, 28)  # Slightly smaller for double words
            bg_color = random.choice(document_backgrounds)

            text_color_variants = [
                (0, 0, 0),
                (20, 20, 20),
                (30, 30, 30),
                (10, 10, 10),
                (15, 15, 15),
            ]
            text_color = random.choice(text_color_variants)

            # Augmentation parameters
            rotation = random.randint(-3, 3)  # Less rotation for double words
            blur_radius = random.uniform(0, 0.08)
            contrast = random.uniform(0.9, 1.1)
            brightness = random.uniform(0.95, 1.05)

            try:
                font_path = random.choice(available_fonts)
                font = ImageFont.truetype(font_path, font_size)

                text_width = 320
                text_height = 48

                img, final_text = generate_double_word_image(word1, word2, font, font_size, bg_color, text_color,
                                                             text_width, text_height)

                # Apply augmentations
                try:
                    img = apply_document_effects(img)
                except Exception as e:
                    print(f"⚠️ Document effects skipped for double words '{final_text}': {e}")

                if rotation != 0:
                    img = img.rotate(rotation, expand=True, fillcolor=bg_color)

                if blur_radius > 0.03:
                    img = img.filter(ImageFilter.GaussianBlur(blur_radius))

                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)

                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)

                img_array = np.array(img)

                # Apply advanced augmentations (less frequently for double words)
                if random.random() < 0.3:
                    img_array = apply_advanced_augmentations(img_array)

                try:
                    img_array = add_document_noise(img_array)
                except Exception as e:
                    print(f"⚠️ Document noise skipped for double words '{final_text}': {e}")

                if random.random() < 0.15:
                    noise = np.random.normal(0, random.randint(1, 3), img_array.shape).astype('uint8')
                    img_array = cv2.add(img_array, noise)

                final_width, final_height = 320, 48
                img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

                if random.random() < 0.1:
                    img_resized = cv2.GaussianBlur(img_resized, (3, 3), 0)

                filename = f"{prefix}_double_{i:09d}.png"
                cv2.imwrite(os.path.join(output_dir, filename), img_resized)

                labels.append(f"{filename}\t{final_text}")

                if (i + 1) % 1000 == 0:
                    print(f"✅ {prefix} double-word: {i + 1}/{double_word_count}")

            except Exception as e:
                print(f"❌ {prefix} double-word gen error for words '{word1}', '{word2}': {e}")
                continue

        return labels

    print("🚀 Generating training data...")
    labels_train = generate_images(train_words, args.train_number, "train")

    print("🧪 Generating val data...")
    labels_val = generate_images(val_words, args.val_number, "val")

    with open(os.path.join(output_dir, "train_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels_train:
            f.write(label + '\n')

    with open(os.path.join(output_dir, "val_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels_val:
            f.write(label + '\n')

    unique_train_words = len(set([label.split('\t')[1] for label in labels_train]))
    unique_val_words = len(set([label.split('\t')[1] for label in labels_val]))

    print(f"\n🎉 Generation completed!")
    print(f"📊 Training: {len(labels_train)} images, {unique_train_words} unique texts")
    print(f"📊 Val: {len(labels_val)} images, {unique_val_words} unique texts")

    # Calculate coverage statistics
    total_train_texts = len(train_words) + len(train_words) * 0.3  # words + potential combinations
    total_val_texts = len(val_words) + len(val_words) * 0.3

    print(
        f"📊 Coverage: {unique_train_words / total_train_texts * 100:.1f}% train coverage, {unique_val_words / total_val_texts * 100:.1f}% val coverage")


generate_synthetic_data()