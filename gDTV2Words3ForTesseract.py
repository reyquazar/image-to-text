import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import argparse
import shutil


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
    """Adds document-like noise and returns noise type"""
    h, w = img_array.shape[:2]
    noise_types = []

    if random.random() < 0.2:
        num_spots = random.randint(1, 5)
        for _ in range(num_spots):
            x, y = random.randint(0, w - 1), random.randint(0, h - 1)
            radius = random.randint(2, 10)
            intensity = random.randint(5, 20)
            cv2.circle(img_array, (x, y), radius, (intensity, intensity, intensity), -1)
        noise_types.append(f"S{num_spots}")

    if random.random() < 0.15:
        num_lines = random.randint(1, 3)
        for _ in range(num_lines):
            x1, y1 = random.randint(0, w - 1), random.randint(0, h - 1)
            x2, y2 = random.randint(0, w - 1), random.randint(0, h - 1)
            thickness = random.randint(1, 2)
            intensity = random.randint(10, 30)
            cv2.line(img_array, (x1, y1), (x2, y2), (intensity, intensity, intensity), thickness)
        noise_types.append(f"L{num_lines}")

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
        noise_types.append(f"Sh{direction[0]}{shadow_intensity}")

    return img_array, "_".join(noise_types) if noise_types else "N0"


def apply_document_effects(img):
    """Applies document scanning effects and returns effect types"""
    effects = []

    if random.random() < 0.3:
        blur_type = random.choice(['gaussian', 'defocus'])
        if blur_type == 'defocus':
            blur_radius = random.uniform(0.3, 0.8)
            img = img.filter(ImageFilter.GaussianBlur(blur_radius))
            effects.append(f"BD{blur_radius:.1f}")
        else:
            blur_radius = random.uniform(0.2, 0.5)
            img = img.filter(ImageFilter.GaussianBlur(blur_radius))
            effects.append(f"BG{blur_radius:.1f}")

    if random.random() < 0.25:
        try:
            quality = random.randint(30, 85)
            from io import BytesIO
            output = BytesIO()
            img.save(output, format='PNG', quality=quality, optimize=True)
            img = Image.open(output)
            img = img.copy()
            output.close()
            effects.append(f"CQ{quality}")
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
            effects.append(f"SK{skew:.2f}")
        except Exception as e:
            print(f"⚠️ Skew error: {e}")

    return img, "_".join(effects) if effects else "E0"


def apply_safe_augmentations(img_array):
    """Applies safe augmentations that won't destroy the image and returns augmentation types"""
    h, w = img_array.shape[:2]
    aug_types = []

    # Light Gaussian noise
    if random.random() < 0.3:
        noise_std = random.randint(1, 3)
        noise = np.random.normal(0, noise_std, img_array.shape).astype('uint8')
        img_array = cv2.add(img_array, noise)
        aug_types.append(f"GN{noise_std}")

    # Light blur
    if random.random() < 0.2:
        img_array = cv2.GaussianBlur(img_array, (3, 3), 0)
        aug_types.append("BL")

    # Color variations (safer version)
    if random.random() < 0.2:
        try:
            # Small brightness adjustment
            brightness = random.uniform(0.9, 1.1)
            img_array = np.clip(img_array.astype(np.float32) * brightness, 0, 255).astype(np.uint8)
            aug_types.append(f"BR{brightness:.2f}")

            # Small contrast adjustment
            contrast = random.uniform(0.95, 1.05)
            mean = np.mean(img_array)
            img_array = np.clip((img_array.astype(np.float32) - mean) * contrast + mean, 0, 255).astype(np.uint8)
            aug_types.append(f"CO{contrast:.2f}")
        except Exception as e:
            print(f"⚠️ Color adjustment error: {e}")

    return img_array, "_".join(aug_types) if aug_types else "A0"


def create_tesseract_structure(base_dir="."):
    """Creates the proper Tesseract directory structure"""
    # Main directories - стандартная структура tesstrain
    data_dir = os.path.join(base_dir, "data")
    ground_truth_dir = os.path.join(data_dir, "aze-ground-truth")  # ВСЕ файлы здесь

    # Create directories
    os.makedirs(ground_truth_dir, exist_ok=True)

    print(f"📁 Created Tesseract structure:")
    print(f"  - {ground_truth_dir}")

    return {
        'data_dir': data_dir,
        'ground_truth_dir': ground_truth_dir
    }


def generate_synthetic_data():
    """Main function - generates synthetic text images in Tesseract format"""

    # Create Tesseract directory structure
    dirs = create_tesseract_structure()

    dataset_path = './train_cleaned_ocr_perfect.txt'

    parser = argparse.ArgumentParser(description='Generate Tesseract training data for Azerbaijani')
    parser.add_argument('train_number', type=int, help='Number of training images')
    parser.add_argument('val_number', type=int, help='Number of validation images')
    parser.add_argument('--dataset', type=str, default=dataset_path, help='Path to dataset file')
    parser.add_argument('--output-base', type=str, default='tessdata', help='Base output directory')
    args = parser.parse_args()

    azerbaijani_words = load_words_from_dataset(args.dataset)

    fonts_dir = "./fonts/3/"

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

    # Document backgrounds
    document_backgrounds = [
        'white', '#f8f8f8', '#f0f0f0', '#f5f5f5', '#fafafa',
        '#fffaf0', '#fdf5e6', '#fff8dc',
        '#f0fff0', '#f5fffa', '#f0f8ff'
    ]

    def create_text_image(word, is_double_word=False):
        """Creates basic text image with proper text rendering"""
        font_size = random.randint(10, 32) if not is_double_word else random.randint(18, 24)
        bg_color = random.choice(document_backgrounds)

        text_color_variants = [
            (0, 0, 0), (10, 10, 10), (20, 20, 20), (30, 30, 30),
            (40, 40, 40), (15, 15, 15), (25, 25, 25),
            (5, 5, 5), (35, 35, 35)
        ]
        text_color = random.choice(text_color_variants)

        try:
            font_path = random.choice(available_fonts)
            font = ImageFont.truetype(font_path, font_size)

            text_width = 320
            text_height = 48

            img = Image.new('RGB', (text_width, text_height), color=bg_color)
            draw = ImageDraw.Draw(img)

            # Simple gradient background (occasionally)
            gradient_applied = False
            if random.random() < 0.05:
                for y in range(img.height):
                    shade = 245 + int(10 * (y / img.height))
                    for x in range(img.width):
                        img.putpixel((x, y), (shade, shade, shade))
                gradient_applied = True

            bbox = font.getbbox(word)
            text_actual_width = bbox[2] - bbox[0]
            text_actual_height = bbox[3] - bbox[1]

            # Ensure text fits
            if text_actual_width > text_width - 20:
                # Text too long, reduce font size
                reduction_factor = (text_width - 40) / text_actual_width
                font_size = max(14, int(font_size * reduction_factor))
                font = ImageFont.truetype(font_path, font_size)
                bbox = font.getbbox(word)
                text_actual_width = bbox[2] - bbox[0]
                text_actual_height = bbox[3] - bbox[1]

            x_offset = (text_width - text_actual_width) // 2
            y_offset = (text_height - text_actual_height) // 2

            # Ensure offsets are positive
            x_offset = max(10, x_offset)
            y_offset = max(10, y_offset)

            draw.text((x_offset, y_offset), word, font=font, fill=text_color)

            # Create augmentation info for basic properties
            base_aug = f"FS{font_size}_TC{text_color[0]}"
            if gradient_applied:
                base_aug += "_GR"
            if is_double_word:
                base_aug += "_DW"

            return img, word, base_aug

        except Exception as e:
            print(f"❌ Error creating text image for '{word}': {e}")
            return None, None, None

    def generate_tesseract_images(word_list, count, output_dir, prefix):
        """Generates images in Tesseract format with .gt.txt files"""
        # Вместо отдельных папок train/eval - все в ground_truth_dir
        all_texts = []

        single_word_count = int(count * 0.6)
        double_word_count = count - single_word_count

        print(f"📝 Generating {single_word_count} single-word and {double_word_count} double-word images for {prefix}")

        # Generate single word images
        for i in range(single_word_count):
            word = random.choice(word_list)

            try:
                img, final_text, base_aug = create_text_image(word, is_double_word=False)
                if img is None:
                    continue

                # Collect all augmentation codes
                aug_codes = [base_aug]

                # Rotation
                rotation = random.randint(-10, 10)
                if rotation != 0:
                    img = img.rotate(rotation, expand=True, fillcolor=random.choice(document_backgrounds))
                    aug_codes.append(f"R{rotation:+d}")

                # Apply document effects
                try:
                    img, effect_code = apply_document_effects(img)
                    aug_codes.append(effect_code)
                except Exception as e:
                    print(f"⚠️ Document effects skipped: {e}")
                    aug_codes.append("E0")

                # Convert to array for OpenCV operations
                img_array = np.array(img)

                # Safe augmentations
                img_array, aug_code = apply_safe_augmentations(img_array)
                aug_codes.append(aug_code)

                # Add document noise
                try:
                    img_array, noise_code = add_document_noise(img_array)
                    aug_codes.append(noise_code)
                except Exception as e:
                    print(f"⚠️ Document noise skipped: {e}")
                    aug_codes.append("N0")

                # Combine all augmentation codes
                aug_string = "_".join(aug_codes)

                # Resize to final dimensions
                final_width, final_height = 320, 48
                img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

                # Create Tesseract-compatible filename (without complex augmentation info)
                base_filename = f"{prefix}_{i:09d}"
                image_filename = f"{base_filename}.png"
                gt_filename = f"{base_filename}.gt.txt"

                # Save image
                cv2.imwrite(os.path.join(output_dir, image_filename), img_resized)

                with open(os.path.join(output_dir, gt_filename), 'w', encoding='utf-8') as f:
                    f.write(final_text)

                all_texts.append(final_text)

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

            # Combine words with separator
            separators = [' ', '  ', '   ', ' - ']
            separator = random.choice(separators)
            combined_text = word1 + separator + word2

            try:
                img, final_text, base_aug = create_text_image(combined_text, is_double_word=True)
                if img is None:
                    continue

                # Collect all augmentation codes
                aug_codes = [base_aug]

                # Less rotation for double words
                rotation = random.randint(-2, 2)
                if rotation != 0:
                    img = img.rotate(rotation, expand=True, fillcolor=random.choice(document_backgrounds))
                    aug_codes.append(f"R{rotation:+d}")

                # Apply document effects
                try:
                    img, effect_code = apply_document_effects(img)
                    aug_codes.append(effect_code)
                except Exception as e:
                    print(f"⚠️ Document effects skipped: {e}")
                    aug_codes.append("E0")

                # Convert to array for OpenCV operations
                img_array = np.array(img)

                # Safe augmentations (less frequently for double words)
                if random.random() < 0.5:
                    img_array, aug_code = apply_safe_augmentations(img_array)
                    aug_codes.append(aug_code)
                else:
                    aug_codes.append("A0")

                # Add document noise
                try:
                    img_array, noise_code = add_document_noise(img_array)
                    aug_codes.append(noise_code)
                except Exception as e:
                    print(f"⚠️ Document noise skipped: {e}")
                    aug_codes.append("N0")

                # Combine all augmentation codes
                aug_string = "_".join(aug_codes)

                # Resize to final dimensions
                final_width, final_height = 320, 48
                img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

                # Create Tesseract-compatible filename
                base_filename = f"{prefix}_{single_word_count + i:09d}"
                image_filename = f"{base_filename}.png"
                gt_filename = f"{base_filename}.gt.txt"

                # Save image and ground truth
                cv2.imwrite(os.path.join(output_dir, image_filename), img_resized)
                with open(os.path.join(output_dir, gt_filename), 'w', encoding='utf-8') as f:
                    f.write(final_text)

                all_texts.append(final_text)

                if (i + 1) % 1000 == 0:
                    print(f"✅ {prefix} double-word: {i + 1}/{double_word_count}")

            except Exception as e:
                print(f"❌ {prefix} double-word gen error for words '{word1}', '{word2}': {e}")
                continue

        return all_texts

    print("🚀 Generating training data...")
    train_texts = generate_tesseract_images(train_words, args.train_number, dirs['ground_truth_dir'], "train")

    print("🧪 Generating validation data...")
    eval_texts = generate_tesseract_images(val_words, args.val_number, dirs['ground_truth_dir'], "eval")
    # Create aze.training_text file with all training texts
    training_text_path = os.path.join(dirs['data_dir'], "aze.training_text")
    with open(training_text_path, 'w', encoding='utf-8') as f:
        for text in train_texts + eval_texts:
            f.write(text + '\n')
    # Count generated files - ИСПРАВЛЕННАЯ ВЕРСИЯ
    ground_truth_files = [f for f in os.listdir(dirs['ground_truth_dir']) if f.endswith('.png')]
    train_files = len([f for f in ground_truth_files if f.startswith('train_')])
    eval_files = len([f for f in ground_truth_files if f.startswith('eval_')])

    print(f"\n🎉 Tesseract data generation completed!")
    print(f"📁 Output structure:")
    print(f"  - Training data: {dirs['ground_truth_dir']} ({train_files} images)")
    print(f"  - Validation data: {dirs['ground_truth_dir']} ({eval_files} images)")
    print(f"  - Training text: {training_text_path}")
    print(f"📊 Total texts: {len(train_texts + eval_texts)}")
    print(f"\n🚀 To train Tesseract, run:")
    print(f"make training MODEL_NAME=aze START_MODEL=eng TESSDATA=/usr/share/tesseract-ocr/5/tessdata/")


if __name__ == "__main__":
    generate_synthetic_data()
