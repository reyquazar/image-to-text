import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import argparse
from io import BytesIO


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
    """Adds document-like noise with proper error handling"""
    if img_array is None or img_array.size == 0:
        return img_array

    h, w = img_array.shape[:2]

    # Ensure we're working with a copy
    result = img_array.copy()

    # Spots and stains (increased variety)
    if random.random() < 0.25:
        num_spots = random.randint(1, 8)
        for _ in range(num_spots):
            x, y = random.randint(0, w - 1), random.randint(0, h - 1)
            radius = random.randint(1, 15)
            intensity = random.randint(5, 25)
            try:
                cv2.circle(result, (x, y), radius, (intensity, intensity, intensity), -1)
            except Exception as e:
                continue  # Skip if circle drawing fails

    # Lines and scratches
    if random.random() < 0.2:
        num_lines = random.randint(1, 4)
        for _ in range(num_lines):
            x1, y1 = random.randint(0, w - 1), random.randint(0, h - 1)
            x2, y2 = random.randint(0, w - 1), random.randint(0, h - 1)
            thickness = random.randint(1, 3)
            intensity = random.randint(10, 40)
            try:
                cv2.line(result, (x1, y1), (x2, y2), (intensity, intensity, intensity), thickness)
            except Exception as e:
                continue

    # Edge shadows and gradients - FIXED VERSION
    if random.random() < 0.15:
        shadow_intensity = random.randint(5, 25)
        direction = random.choice(['top', 'bottom', 'left', 'right'])

        try:
            if direction == 'top':
                result[:h // 6, :] = np.clip(result[:h // 6, :].astype(np.int16) - shadow_intensity, 0, 255).astype(
                    np.uint8)
            elif direction == 'bottom':
                result[5 * h // 6:, :] = np.clip(result[5 * h // 6:, :].astype(np.int16) - shadow_intensity, 0,
                                                 255).astype(np.uint8)
            elif direction == 'left':
                result[:, :w // 6] = np.clip(result[:, :w // 6].astype(np.int16) - shadow_intensity, 0, 255).astype(
                    np.uint8)
            elif direction == 'right':
                result[:, 5 * w // 6:] = np.clip(result[:, 5 * w // 6:].astype(np.int16) - shadow_intensity, 0,
                                                 255).astype(np.uint8)
        except Exception as e:
            print(f"⚠️ Shadow effect skipped: {e}")

    # Paper texture overlay (light noise) - FIXED VERSION
    if random.random() < 0.3:
        try:
            # Ensure noise has same shape and type as image
            if len(result.shape) == 3:  # Color image
                texture = np.random.normal(0, random.randint(1, 4), (h, w, 3)).astype(np.uint8)
            else:  # Grayscale
                texture = np.random.normal(0, random.randint(1, 4), (h, w)).astype(np.uint8)
            result = cv2.add(result, texture)
        except Exception as e:
            print(f"⚠️ Texture noise skipped: {e}")

    return result


def apply_document_effects(img):
    """Applies document scanning effects with proper error handling"""
    if img is None:
        return img

    result = img.copy()

    # Enhanced blur effects - FIXED VERSION
    if random.random() < 0.35:
        blur_type = random.choice(['gaussian', 'defocus'])
        try:
            if blur_type == 'defocus':
                blur_radius = random.uniform(0.3, 1.2)
                result = result.filter(ImageFilter.GaussianBlur(blur_radius))
            else:
                blur_radius = random.uniform(0.2, 0.8)
                result = result.filter(ImageFilter.GaussianBlur(blur_radius))
        except Exception as e:
            print(f"⚠️ Blur effect skipped: {e}")

    # Compression artifacts
    if random.random() < 0.3:
        try:
            quality = random.randint(20, 90)
            format_type = 'JPEG'  # Use JPEG for better compression artifacts
            output = BytesIO()

            result.save(output, format=format_type, quality=quality, optimize=True)
            result = Image.open(output)
            result = result.copy()
            output.close()
        except Exception as e:
            print(f"⚠️ Compression error: {e}")

    # Geometric transformations - SIMPLIFIED VERSION
    if random.random() < 0.15:
        try:
            # Simple rotation instead of complex transformations
            rotation = random.uniform(-2, 2)
            if abs(rotation) > 0.5:
                result = result.rotate(rotation, expand=True, fillcolor='white')
        except Exception as e:
            print(f"⚠️ Geometric transformation skipped: {e}")

    # Brightness and contrast variations
    if random.random() < 0.25:
        try:
            # Brightness
            brightness_factor = random.uniform(0.8, 1.3)
            enhancer = ImageEnhance.Brightness(result)
            result = enhancer.enhance(brightness_factor)

            # Contrast
            contrast_factor = random.uniform(0.9, 1.4)
            enhancer = ImageEnhance.Contrast(result)
            result = enhancer.enhance(contrast_factor)
        except Exception as e:
            print(f"⚠️ Color adjustment error: {e}")

    return result


def apply_safe_augmentations(img_array):
    """Applies safe augmentations with proper error handling"""
    if img_array is None or img_array.size == 0:
        return img_array

    result = img_array.copy()
    h, w = result.shape[:2]

    # Enhanced Gaussian noise
    if random.random() < 0.35:
        try:
            noise_std = random.randint(1, 5)
            # Ensure noise has correct shape
            if len(result.shape) == 3:
                noise = np.random.normal(0, noise_std, (h, w, 3)).astype('uint8')
            else:
                noise = np.random.normal(0, noise_std, (h, w)).astype('uint8')
            result = cv2.add(result, noise)
        except Exception as e:
            print(f"⚠️ Noise augmentation skipped: {e}")

    # Various blur types - FIXED VERSION
    if random.random() < 0.25:
        blur_type = random.choice(['gaussian', 'median'])
        try:
            if blur_type == 'gaussian':
                # Ensure kernel size is odd
                result = cv2.GaussianBlur(result, (3, 3), 0)
            else:  # median
                # Ensure kernel size is odd and positive
                result = cv2.medianBlur(result, 3)
        except Exception as e:
            print(f"⚠️ Blur augmentation skipped: {e}")

    # Advanced color variations - SIMPLIFIED VERSION
    if random.random() < 0.25:
        try:
            # Simple brightness/contrast in RGB space
            brightness = random.uniform(0.9, 1.1)
            result = np.clip(result.astype(np.float32) * brightness, 0, 255).astype(np.uint8)

            # Simple contrast
            contrast = random.uniform(0.95, 1.05)
            mean = np.mean(result)
            result = np.clip((result.astype(np.float32) - mean) * contrast + mean, 0, 255).astype(np.uint8)
        except Exception as e:
            print(f"⚠️ Color adjustment error: {e}")

    return result


def load_paper_textures(textures_dir):
    """Load paper texture images for backgrounds"""
    textures = []
    if os.path.exists(textures_dir):
        for file in os.listdir(textures_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                try:
                    texture_path = os.path.join(textures_dir, file)
                    texture = Image.open(texture_path)
                    textures.append(texture)
                    print(f"✅ Loaded paper texture: {file}")
                except Exception as e:
                    print(f"❌ Error loading texture {file}: {e}")
    else:
        print(f"⚠️ Textures directory not found: {textures_dir}")

    return textures


def create_complex_background(width, height, paper_textures):
    """Creates realistic document backgrounds with textures"""
    bg_type = random.choices(
        ['solid', 'gradient', 'texture', 'noisy'],
        weights=[0.5, 0.2, 0.2, 0.1]  # Increased solid color probability
    )[0]

    try:
        if bg_type == 'solid':
            colors = [
                'white', '#f8f8f8', '#f0f0f0', '#f5f5f5', '#fafafa',
                '#fffaf0', '#fdf5e6', '#fff8dc', '#f0fff0', '#f5fffa', '#f0f8ff',
                '#faf0e6', '#fff5ee', '#f8f8ff'
            ]
            bg_color = random.choice(colors)
            bg = Image.new('RGB', (width, height), color=bg_color)

        elif bg_type == 'gradient':
            # Simple gradient implementation
            base_color = random.choice([240, 245, 250, 255])
            bg = Image.new('RGB', (width, height), color='white')
            draw = ImageDraw.Draw(bg)

            # Draw simple gradient
            for i in range(height):
                shade = base_color - int((i / height) * 20)
                shade = max(200, shade)
                draw.line([(0, i), (width, i)], fill=(shade, shade, shade))

        elif bg_type == 'texture' and paper_textures:
            # Use paper texture
            texture = random.choice(paper_textures)
            # Resize texture to fit
            texture = texture.resize((width, height), Image.Resampling.LANCZOS)
            bg = texture.copy()

            # Lighten the texture
            enhancer = ImageEnhance.Brightness(bg)
            bg = enhancer.enhance(random.uniform(1.1, 1.4))

        else:  # noisy
            bg = Image.new('RGB', (width, height), color='white')
            # Convert to array for noise addition
            bg_array = np.array(bg)
            # Add subtle noise
            noise = np.random.normal(0, random.randint(2, 8), (height, width, 3)).astype(np.uint8)
            bg_array = np.clip(bg_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
            bg = Image.fromarray(bg_array)

    except Exception as e:
        print(f"⚠️ Background creation error, using solid white: {e}")
        bg = Image.new('RGB', (width, height), color='white')

    return bg


def generate_synthetic_data():
    """Main function - generates synthetic text images with document-like appearance"""
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
    textures_dir = "./text/typed_text/paper_textures"

    print(f"🔍 Find fonts: {fonts_dir}")
    print(f"📊 Total unique words: {len(azerbaijani_words)}")

    # Load paper textures
    paper_textures = load_paper_textures(textures_dir)

    random.shuffle(azerbaijani_words)
    split_idx = int(0.8 * len(azerbaijani_words))

    train_words = azerbaijani_words[:split_idx]
    val_words = azerbaijani_words[split_idx:]

    print(f"📊 Words split: Train - {len(train_words)}, val - {len(val_words)}")

    available_fonts = []
    if os.path.exists(fonts_dir):
        for file in os.listdir(fonts_dir):
            if file.lower().endswith(('.ttf', '.otf')):
                font_path = os.path.join(fonts_dir, file)
                try:
                    # Test if font can be loaded
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
    print(f"🎨 Loaded {len(paper_textures)} paper textures")

    def apply_case_variation(text):
        """Apply random case variations to text"""
        if random.random() < 0.15:  # 15% chance for uppercase
            return text.upper()
        elif random.random() < 0.1:  # 10% chance for lowercase
            return text.lower()
        elif random.random() < 0.05:  # 5% chance for title case
            return text.title()
        else:
            return text  # Keep original case

    def create_text_image(word, is_double_word=False, is_sentence=False):
        """Creates advanced text image with proper text rendering"""
        if is_sentence:
            font_size = random.randint(16, 22)
        elif is_double_word:
            font_size = random.randint(18, 24)
        else:
            font_size = random.randint(20, 28)

        # Apply case variation
        word = apply_case_variation(word)

        text_color_variants = [
            (0, 0, 0), (20, 20, 20), (30, 30, 30),
            (10, 10, 10), (15, 15, 15), (25, 25, 25),
            (5, 5, 5), (35, 35, 35)
        ]
        text_color = random.choice(text_color_variants)

        try:
            font_path = random.choice(available_fonts)
            font = ImageFont.truetype(font_path, font_size)

            text_width = 320
            text_height = 48 if not is_sentence else 64

            # Create advanced background
            bg = create_complex_background(text_width, text_height, paper_textures)
            img = bg.copy()
            draw = ImageDraw.Draw(img)

            # Get text bounding box
            try:
                bbox = font.getbbox(word)
                text_actual_width = bbox[2] - bbox[0]
                text_actual_height = bbox[3] - bbox[1]
            except:
                # Fallback for older PIL versions
                left, top, right, bottom = draw.textbbox((0, 0), word, font=font)
                text_actual_width = right - left
                text_actual_height = bottom - top

            # Ensure text fits with better handling
            max_width = text_width - 40
            if text_actual_width > max_width:
                reduction_factor = max_width / text_actual_width
                font_size = max(12, int(font_size * reduction_factor * 0.95))
                font = ImageFont.truetype(font_path, font_size)
                try:
                    bbox = font.getbbox(word)
                    text_actual_width = bbox[2] - bbox[0]
                    text_actual_height = bbox[3] - bbox[1]
                except:
                    left, top, right, bottom = draw.textbbox((0, 0), word, font=font)
                    text_actual_width = right - left
                    text_actual_height = bottom - top

            # Text positioning
            alignment = random.choices(
                ['center', 'left', 'right'],
                weights=[0.7, 0.15, 0.15]
            )[0]

            if alignment == 'center':
                x_offset = (text_width - text_actual_width) // 2
            elif alignment == 'left':
                x_offset = random.randint(10, 20)
            else:  # right
                x_offset = text_width - text_actual_width - random.randint(10, 20)

            y_offset = (text_height - text_actual_height) // 2

            # Ensure offsets are positive and within bounds
            x_offset = max(5, min(x_offset, text_width - text_actual_width - 5))
            y_offset = max(5, min(y_offset, text_height - text_actual_height - 5))

            # Add text shadow occasionally
            if random.random() < 0.1:
                shadow_color = (50, 50, 50)
                shadow_offset = (1, 1)
                draw.text((x_offset + shadow_offset[0], y_offset + shadow_offset[1]),
                          word, font=font, fill=shadow_color)

            draw.text((x_offset, y_offset), word, font=font, fill=text_color)

            return img, word

        except Exception as e:
            print(f"❌ Error creating text image for '{word}': {e}")
            return None, None

    def create_sentence(words_list, max_words=7):
        """Creates a sentence from random words"""
        num_words = random.randint(3, min(max_words, len(words_list)))
        sentence_words = random.sample(words_list, num_words)

        # Add punctuation occasionally
        if random.random() < 0.3:
            sentence_words[-1] += random.choice(['.', '!', '?'])

        # Add commas occasionally
        if len(sentence_words) > 3 and random.random() < 0.2:
            comma_pos = random.randint(1, len(sentence_words) - 2)
            sentence_words[comma_pos] += ','

        return ' '.join(sentence_words)

    def generate_images(word_list, count, prefix):
        """Generates images for given word list"""
        labels = []
        single_word_count = int(count * 0.5)
        double_word_count = int(count * 0.3)
        sentence_count = count - single_word_count - double_word_count

        print(
            f"📝 Generating {single_word_count} single-word, {double_word_count} double-word, and {sentence_count} sentence images for {prefix}")

        # Generate single word images
        for i in range(single_word_count):
            word = random.choice(word_list)

            try:
                img, final_text = create_text_image(word, is_double_word=False)
                if img is None:
                    continue

                # Enhanced rotation
                rotation = random.randint(-4, 4)
                if rotation != 0:
                    expand = random.random() < 0.3
                    img = img.rotate(rotation, expand=expand,
                                     fillcolor=random.choice(['white', '#f8f8f8', '#f0f0f0']))

                # Apply document effects
                img = apply_document_effects(img)

                # Convert to array for OpenCV operations
                img_array = np.array(img)

                # Safe augmentations
                img_array = apply_safe_augmentations(img_array)

                # Add document noise
                img_array = add_document_noise(img_array)

                # Resize to final dimensions
                final_width, final_height = 320, 48
                img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

                filename = f"{prefix}_{i:09d}.png"
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

            # Combine words with separator
            separators = [' ', '  ', '   ', ' - ', ' • ']
            separator = random.choice(separators)
            combined_text = word1 + separator + word2

            try:
                img, final_text = create_text_image(combined_text, is_double_word=True)
                if img is None:
                    continue

                # Moderate rotation for double words
                rotation = random.randint(-3, 3)
                if rotation != 0:
                    img = img.rotate(rotation, expand=True, fillcolor=random.choice(['white', '#f8f8f8']))

                # Apply document effects
                img = apply_document_effects(img)

                # Convert to array for OpenCV operations
                img_array = np.array(img)

                # Safe augmentations (less frequently for double words)
                if random.random() < 0.6:
                    img_array = apply_safe_augmentations(img_array)

                # Add document noise
                img_array = add_document_noise(img_array)

                # Resize to final dimensions
                final_width, final_height = 320, 48
                img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

                filename = f"{prefix}_{single_word_count + i:09d}.png"
                cv2.imwrite(os.path.join(output_dir, filename), img_resized)

                labels.append(f"{filename}\t{final_text}")

                if (i + 1) % 1000 == 0:
                    print(f"✅ {prefix} double-word: {i + 1}/{double_word_count}")

            except Exception as e:
                print(f"❌ {prefix} double-word gen error for words '{word1}', '{word2}': {e}")
                continue

        # Generate sentence images
        for i in range(sentence_count):
            sentence = create_sentence(word_list)

            try:
                img, final_text = create_text_image(sentence, is_sentence=True)
                if img is None:
                    continue

                # Minimal rotation for sentences
                rotation = random.randint(-2, 2)
                if rotation != 0:
                    img = img.rotate(rotation, expand=True, fillcolor='white')

                # Apply document effects (lightly for sentences)
                if random.random() < 0.7:
                    img = apply_document_effects(img)

                # Convert to array for OpenCV operations
                img_array = np.array(img)

                # Safe augmentations (less frequently for sentences)
                if random.random() < 0.4:
                    img_array = apply_safe_augmentations(img_array)

                # Add document noise (lightly for sentences)
                if random.random() < 0.6:
                    img_array = add_document_noise(img_array)

                # Resize to final dimensions
                final_width, final_height = 320, 48
                img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

                filename = f"{prefix}_{single_word_count + double_word_count + i:09d}.png"
                cv2.imwrite(os.path.join(output_dir, filename), img_resized)

                labels.append(f"{filename}\t{final_text}")

                if (i + 1) % 500 == 0:
                    print(f"✅ {prefix} sentence: {i + 1}/{sentence_count}")

            except Exception as e:
                print(f"❌ {prefix} sentence gen error for sentence '{sentence}': {e}")
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
    print(f"📁 Output directory: {output_dir}")


if __name__ == "__main__":
    generate_synthetic_data()
