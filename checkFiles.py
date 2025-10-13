import cv2
import os
import numpy as np
from collections import Counter


def analyze_all_image_sizes():
    """Анализирует ВСЕ изображения в датасете"""
    print("=" * 60)
    print("COMPLETE IMAGE SIZE ANALYSIS")
    print("=" * 60)

    label_files = [
        './text/typed_text/az_config_train/train_list.txt',
        './text/typed_text/az_config_train/val_list.txt'
    ]

    all_sizes = []

    for label_file in label_files:
        with open(label_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        print(f"\nАнализирую {len(lines)} изображений из {os.path.basename(label_file)}...")

        for i, line in enumerate(lines):
            parts = line.strip().split('\t')
            if len(parts) >= 1:
                img_path = os.path.join('./text/typed_text/az_config_train', parts[0])
                if os.path.exists(img_path):
                    img = cv2.imread(img_path)
                    if img is not None:
                        h, w, c = img.shape
                        all_sizes.append((h, w))

            # Прогресс
            if (i + 1) % 50 == 0:
                print(f"  Обработано {i + 1}/{len(lines)}")

    # Анализируем статистику
    if all_sizes:
        heights = [h for h, w in all_sizes]
        widths = [w for h, w in all_sizes]

        print(f"\nСТАТИСТИКА ПО ВСЕМУ ДАТАСЕТУ ({len(all_sizes)} изображений):")
        print(f"Высота: min={min(heights)}, max={max(heights)}")
        print(f"Ширина: min={min(widths)}, max={max(widths)}")

        # Самые частые размеры
        size_counter = Counter(all_sizes)
        common_sizes = size_counter.most_common(5)

        print(f"\nСАМЫЕ ЧАСТЫЕ РАЗМЕРЫ:")
        for size, count in common_sizes:
            print(f"  {size[0]}x{size[1]}: {count} изображений ({count / len(all_sizes) * 100:.1f}%)")

        # Рекомендация
        most_common_size = common_sizes[0][0]
        print(f"\nРЕКОМЕНДАЦИЯ:")
        print(f"  image_shape: [3, {most_common_size[0]}, {most_common_size[1]}]")

        # Проверяем разнообразие размеров
        if len(common_sizes) == 1:
            print("✅ Все изображения одного размера - ОТЛИЧНО!")
        else:
            unique_sizes = len(set(all_sizes))
            print(f"⚠️  {unique_sizes} разных размеров - нужен паддинг/ресайз")


def check_current_training_issue():
    """Проверяет текущую проблему обучения"""
    print("\n" + "=" * 60)
    print("CURRENT TRAINING PROBLEM DIAGNOSIS")
    print("=" * 60)

    print("ПОЧЕМУ LOSS=25+ С ТВОИМ КОНФИГОМ:")
    print("1. image_shape: [3, 48, 400] - но реальные изображения 48x320")
    print("2. RecResizeImg растягивает 320→400 пикселей")
    print("3. Искаженные данные → модель не может учиться")
    print("4. Без NormalizeImage - значения пикселей [0,255] вместо [0,1]")


def generate_fixed_config():
    """Генерирует исправленный конфиг"""
    print("\n" + "=" * 60)
    print("FIXED CONFIG RECOMMENDATION")
    print("=" * 60)

    print("ДВА ВАРИАНТА ИСПРАВЛЕНИЯ:")

    print("\nВАРИАНТ 1: Под реальные размеры (если все изображения ~48x320)")
    print("RecResizeImg:")
    print("  image_shape: [3, 48, 320]  # Реальные размеры")
    print("  padding: true")

    print("\nВАРИАНТ 2: С нормализацией и паддингом")
    print("RecResizeImg:")
    print("  image_shape: [3, 48, 400]  # Оригинальный размер")
    print("  padding: true")
    print("ДОБАВИТЬ в transforms:")
    print("- NormalizeImage:")
    print("    scale: 1.0/255.0")
    print("    mean: [0.5, 0.5, 0.5]")
    print("    std: [0.5, 0.5, 0.5]")


if __name__ == "__main__":
    analyze_all_image_sizes()
    check_current_training_issue()
    generate_fixed_config()