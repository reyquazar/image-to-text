import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


def add_document_noise(img_array):
    """Adds document-like noise"""
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
    """Applies document scanning effects"""
    if random.random() < 0.3:
        blur_type = random.choice(['gaussian', 'defocus'])
        if blur_type == 'defocus':
            img = img.filter(ImageFilter.GaussianBlur(random.uniform(0.3, 0.8)))
        else:
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


def apply_safe_augmentations(img_array):
    """Applies safe augmentations that won't destroy the image"""
    h, w = img_array.shape[:2]

    # Light Gaussian noise
    if random.random() < 0.3:
        noise = np.random.normal(0, random.randint(1, 3), img_array.shape).astype('uint8')
        img_array = cv2.add(img_array, noise)

    # Light blur
    if random.random() < 0.2:
        img_array = cv2.GaussianBlur(img_array, (3, 3), 0)

    # Color variations (safer version)
    if random.random() < 0.2:
        try:
            # Small brightness adjustment
            brightness = random.uniform(0.9, 1.1)
            img_array = np.clip(img_array.astype(np.float32) * brightness, 0, 255).astype(np.uint8)

            # Small contrast adjustment
            contrast = random.uniform(0.95, 1.05)
            mean = np.mean(img_array)
            img_array = np.clip((img_array.astype(np.float32) - mean) * contrast + mean, 0, 255).astype(np.uint8)
        except Exception as e:
            print(f"⚠️ Color adjustment error: {e}")

    return img_array


def create_text_image(word, is_double_word=False):
    """Creates basic text image with proper text rendering"""
    # Document backgrounds
    document_backgrounds = [
        'white', '#f8f8f8', '#f0f0f0', '#f5f5f5', '#fafafa',
        '#fffaf0', '#fdf5e6', '#fff8dc',
        '#f0fff0', '#f5fffa', '#f0f8ff'
    ]

    fonts_dir = "./text/typed_text/fonts/3"

    font_size = random.randint(20, 28) if not is_double_word else random.randint(18, 24)
    bg_color = random.choice(document_backgrounds)

    text_color_variants = [
        (0, 0, 0), (20, 20, 20), (30, 30, 30),
        (10, 10, 10), (15, 15, 15)
    ]
    text_color = random.choice(text_color_variants)

    try:
        # Get available fonts
        available_fonts = []
        if os.path.exists(fonts_dir):
            for file in os.listdir(fonts_dir):
                if file.lower().endswith('.ttf'):
                    font_path = os.path.join(fonts_dir, file)
                    available_fonts.append(font_path)

        if not available_fonts:
            print("❌ No fonts available!")
            return None, None

        font_path = random.choice(available_fonts)
        font = ImageFont.truetype(font_path, font_size)

        text_width = 320
        text_height = 48

        img = Image.new('RGB', (text_width, text_height), color=bg_color)
        draw = ImageDraw.Draw(img)

        # Simple gradient background (occasionally)
        if random.random() < 0.05:
            for y in range(img.height):
                shade = 245 + int(10 * (y / img.height))
                for x in range(img.width):
                    img.putpixel((x, y), (shade, shade, shade))

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
        y_offset = max(5, y_offset)

        draw.text((x_offset, y_offset), word, font=font, fill=text_color)

        return img, word

    except Exception as e:
        print(f"❌ Error creating text image for '{word}': {e}")
        return None, None


def augment_single_word():
    """Main function - performs augmentation on a single word entered by user"""
    output_dir = "./augmented_words"
    os.makedirs(output_dir, exist_ok=True)

    # Get word from user input
    word = input("📝 Enter the word to augment: ").strip()

    if not word:
        print("❌ No word entered!")
        return

    print(f"🎯 Augmenting word: '{word}'")

    num_variations = input("🔄 How many variations to generate? (default: 10): ").strip()
    try:
        num_variations = int(num_variations) if num_variations else 10
    except ValueError:
        num_variations = 10

    print(f"🔄 Generating {num_variations} variations...")

    for i in range(num_variations):
        try:
            # Create base image
            img, final_text = create_text_image(word, is_double_word=False)
            if img is None:
                continue

            # Basic rotation
            rotation = random.randint(-3, 3)
            if rotation != 0:
                img = img.rotate(rotation, expand=True, fillcolor=random.choice([
                    'white', '#f8f8f8', '#f0f0f0', '#f5f5f5'
                ]))

            # Apply document effects
            try:
                img = apply_document_effects(img)
            except Exception as e:
                print(f"⚠️ Document effects skipped: {e}")

            # Convert to array for OpenCV operations
            img_array = np.array(img)

            # Safe augmentations
            img_array = apply_safe_augmentations(img_array)

            # Add document noise
            try:
                img_array = add_document_noise(img_array)
            except Exception as e:
                print(f"⚠️ Document noise skipped: {e}")

            # Resize to final dimensions
            final_width, final_height = 320, 48
            img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

            # Save image
            filename = f"augmented_{i + 1:03d}.png"
            filepath = os.path.join(output_dir, filename)
            cv2.imwrite(filepath, img_resized)

            print(f"✅ Saved: {filename}")

        except Exception as e:
            print(f"❌ Error generating variation {i + 1}: {e}")
            continue

    print(f"\n🎉 Augmentation completed!")
    print(f"📁 Output directory: {output_dir}")
    print(f"📊 Generated {num_variations} variations of word '{word}'")


if __name__ == "__main__":
    augment_single_word()