import os
import cv2
import albumentations as A
import numpy as np
from tqdm import tqdm


def augment_dataset():
    # Пути
    base_dir = "C:/Users/elsha/Downloads/image-to-text/text/typed_text/fortrain"
    train_list_path = os.path.join(base_dir, "train_list.txt")
    val_list_path = os.path.join(base_dir, "val_list.txt")

    # Создаем папки для аугментированных данных
    augmented_dir = os.path.join(base_dir, "augmented_data")
    augmented_train_dir = os.path.join(augmented_dir, "train")
    augmented_val_dir = os.path.join(augmented_dir, "val")
    os.makedirs(augmented_train_dir, exist_ok=True)
    os.makedirs(augmented_val_dir, exist_ok=True)

    # Читаем списки файлов с сохранением разметки
    def read_annotation_file(file_path):
        data = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) < 2:
                    print(f"Предупреждение: строка {line_num} пропущена - неправильный формат: {line}")
                    continue
                filename = parts[0].strip()
                annotation = '\t'.join(parts[1:]).strip()
                data.append((filename, annotation))
        return data

    train_data = read_annotation_file(train_list_path)
    val_data = read_annotation_file(val_list_path)

    print(f"Найдено {len(train_data)} train записей с разметкой")
    print(f"Найдено {len(val_data)} val записей с разметкой")

    if not train_data:
        print("Ошибка: тренировочные данные не найдены!")
        return

    # ФИНАЛЬНЫЕ ИСПРАВЛЕННЫЕ трансформации
    transform = A.Compose([
        # Геометрические трансформации
        A.Affine(
            scale=(0.95, 1.05),
            rotate=(-2, 2),
            translate_percent=(-0.02, 0.02),
            shear=(-2, 2),
            p=0.6
        ),

        # Шумы и размытия (ПОЛНОСТЬЮ ИСПРАВЛЕННЫЕ)
        A.GaussNoise(var_limit=(10.0, 30.0), mean=0, p=0.3),  # добавлен mean параметр
        A.MotionBlur(blur_limit=3, p=0.2),
        A.MedianBlur(blur_limit=3, p=0.1),

        # Цветовые трансформации
        A.RandomBrightnessContrast(
            brightness_limit=0.1,
            contrast_limit=0.1,
            brightness_by_max=True,
            p=0.4
        ),
        A.ColorJitter(
            brightness=0.1,
            contrast=0.1,
            saturation=0.05,
            hue=0.01,
            p=0.3
        ),

        # Искажения
        A.ElasticTransform(
            alpha=0.5,
            sigma=20,
            p=0.1
        ),

        # Дополнительные трансформации для OCR
        A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.3), p=0.2),
        A.RandomGamma(gamma_limit=(80, 120), p=0.2),

        # Улучшенные трансформации для текста (ИСПРАВЛЕННЫЕ)
        A.OpticalDistortion(distort_limit=0.05, p=0.1),  # убран shift_limit
        A.GridDistortion(distort_limit=0.05, p=0.1),
    ])

    # Количество аугментированных копий для каждого изображения
    AUGMENTATION_FACTOR = 3

    # Создаем новые списки файлов С РАЗМЕТКОЙ
    new_train_lines = []
    new_val_lines = []

    # Функция для безопасной загрузки изображения
    def load_image_safe(image_path):
        try:
            image = cv2.imread(image_path)
            if image is None:
                print(f"Ошибка: не удалось загрузить {image_path}")
                return None
            return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        except Exception as e:
            print(f"Ошибка загрузки {image_path}: {e}")
            return None

    # Функция для проверки качества изображения после аугментации
    def is_image_quality_good(image):
        """Проверяет, что изображение не испорчено после аугментации"""
        if image is None:
            return False

        # Проверяем среднюю яркость
        mean_brightness = image.mean()
        if mean_brightness < 20 or mean_brightness > 235:
            return False

        # Проверяем контрастность
        std_dev = image.std()
        if std_dev < 15:
            return False

        return True

    # Копируем валидационные данные БЕЗ изменений (с разметкой)
    print("\nКопируем валидационные данные...")
    val_skipped = 0
    for filename, annotation in tqdm(val_data, desc="Validation"):
        src_path = os.path.join(base_dir, filename)
        dst_path = os.path.join(augmented_val_dir, filename)

        image = load_image_safe(src_path)
        if image is not None:
            cv2.imwrite(dst_path, cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
            new_val_lines.append(f"{filename}\t{annotation}")
        else:
            print(f"Пропущен валидационный файл: {filename}")
            val_skipped += 1

    # Аугментируем тренировочные данные (с разметкой)
    print("\nАугментируем тренировочные данные...")
    successful_augmentations = 0
    failed_augmentations = 0
    suspicious_images = 0

    for filename, annotation in tqdm(train_data, desc="Training"):
        src_path = os.path.join(base_dir, filename)

        # Загружаем изображение
        original_image = load_image_safe(src_path)
        if original_image is None:
            print(f"Пропущен тренировочный файл: {filename}")
            failed_augmentations += 1
            continue

        # Сохраняем оригинал в аугментированную папку
        original_dst = os.path.join(augmented_train_dir, filename)
        cv2.imwrite(original_dst, cv2.cvtColor(original_image, cv2.COLOR_RGB2BGR))
        new_train_lines.append(f"{filename}\t{annotation}")
        successful_augmentations += 1

        # Создаем аугментированные версии
        for i in range(AUGMENTATION_FACTOR):
            try:
                augmented = transform(image=original_image)
                augmented_image = augmented['image']

                # Проверяем качество аугментированного изображения
                if not is_image_quality_good(augmented_image):
                    suspicious_images += 1
                    continue

                # Создаем имя для аугментированного файла
                name, ext = os.path.splitext(filename)
                aug_filename = f"{name}_aug{i}{ext}"
                aug_dst_path = os.path.join(augmented_train_dir, aug_filename)

                # Сохраняем аугментированное изображение
                cv2.imwrite(aug_dst_path, cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
                new_train_lines.append(f"{aug_filename}\t{annotation}")
                successful_augmentations += 1

            except Exception as e:
                print(f"Ошибка аугментации {filename}_aug{i}: {e}")
                failed_augmentations += 1

    # Сохраняем новые списки файлов
    new_train_list_path = os.path.join(augmented_dir, "train_list.txt")
    new_val_list_path = os.path.join(augmented_dir, "val_list.txt")

    with open(new_train_list_path, 'w', encoding='utf-8') as f:
        for line in new_train_lines:
            f.write(line + '\n')

    with open(new_val_list_path, 'w', encoding='utf-8') as f:
        for line in new_val_lines:
            f.write(line + '\n')

    print("\n" + "=" * 50)
    print("АУГМЕНТАЦИЯ ЗАВЕРШЕНА!")
    print("=" * 50)
    print(f"Исходный train: {len(train_data)} файлов")
    print(f"Новый train: {len(new_train_lines)} файлов")
    print(f"Val: {len(new_val_lines)} файлов")
    print(f"Коэффициент увеличения: {len(new_train_lines) / len(train_data):.1f}x")
    print(f"Успешных аугментаций: {successful_augmentations}")
    print(f"Неудачных аугментаций: {failed_augmentations}")
    print(f"Пропущено валидационных: {val_skipped}")
    print(f"Отфильтровано подозрительных: {suspicious_images}")
    print(f"Аугментированные данные сохранены в: {augmented_dir}")

    # Статистика по классам
    if new_train_lines:
        first_chars = {}
        for line in new_train_lines:
            parts = line.split('\t')
            if len(parts) >= 2 and parts[1]:
                first_char = parts[1][0]
                first_chars[first_char] = first_chars.get(first_char, 0) + 1

        print(f"\nРаспределение первых символов в train (топ-15):")
        for char, count in sorted(first_chars.items(), key=lambda x: x[1], reverse=True)[:15]:
            print(f"  '{char}': {count}")

    # Создаем файл с общей статистикой
    stats_path = os.path.join(augmented_dir, "augmentation_stats.txt")
    with open(stats_path, 'w', encoding='utf-8') as f:
        f.write("Статистика аугментации:\n")
        f.write("=" * 30 + "\n")
        f.write(f"Исходный train: {len(train_data)} файлов\n")
        f.write(f"Новый train: {len(new_train_lines)} файлов\n")
        f.write(f"Val: {len(new_val_lines)} файлов\n")
        f.write(f"Коэффициент увеличения: {len(new_train_lines) / len(train_data):.1f}x\n")
        f.write(f"Успешных аугментаций: {successful_augmentations}\n")
        f.write(f"Неудачных аугментаций: {failed_augmentations}\n")
        f.write(f"Отфильтровано подозрительных: {suspicious_images}\n")

    print(f"\nСтатистика сохранена в: {stats_path}")


if __name__ == "__main__":
    augment_dataset()