import os
import cv2
import numpy as np
from pathlib import Path

# ================== КОНФИГУРАЦИЯ ==================
# Путь к вашему train_list.txt или val_list.txt
label_file_path = './text/test/train_list.txt'
# Базовый директорий, где лежат изображения
base_data_dir = './text/test/'


# ==================================================

def analyze_dataset_simple(label_file_path, base_data_dir):
    """
    Быстрый анализ размеров изображений с выводом в консоль.
    """
    with open(label_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    widths, heights, ratios = [], [], []
    missing_files = []

    print(f"Анализирую {len(lines)} изображений...\n")

    for i, line in enumerate(lines):
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue

        img_rel_path = parts[0]
        img_full_path = os.path.join(base_data_dir, img_rel_path)

        if not os.path.exists(img_full_path):
            missing_files.append(img_rel_path)
            continue

        img = cv2.imread(img_full_path)
        if img is None:
            continue

        height, width = img.shape[:2]
        aspect_ratio = width / height if height > 0 else 0

        widths.append(width)
        heights.append(height)
        ratios.append(aspect_ratio)

    # Вывод статистики
    print("=" * 60)
    print("СТАТИСТИКА РАЗМЕРОВ ИЗОБРАЖЕНИЙ")
    print("=" * 60)
    print(f"Успешно проанализировано: {len(widths)} изображений")
    print(f"Отсутствуют: {len(missing_files)} файлов")

    if not widths:
        print("Нет данных для анализа!")
        return

    print(f"\n--- ШИРИНА ---")
    print(f"Средняя: {np.mean(widths):.1f} px")
    print(f"Медиана:  {np.median(widths):.1f} px")
    print(f"Min:      {np.min(widths):.1f} px")
    print(f"Max:      {np.max(widths):.1f} px")

    print(f"\n--- ВЫСОТА ---")
    print(f"Средняя: {np.mean(heights):.1f} px")
    print(f"Медиана:  {np.median(heights):.1f} px")
    print(f"Min:      {np.min(heights):.1f} px")
    print(f"Max:      {np.max(heights):.1f} px")

    print(f"\n--- СООТНОШЕНИЕ СТОРОН (ширина/высота) ---")
    print(f"Среднее:   {np.mean(ratios):.2f}")
    print(f"Медиана:   {np.median(ratios):.2f}")
    print(f"Min:       {np.min(ratios):.2f}")
    print(f"Max:       {np.max(ratios):.2f}")

    # Анализ распределения соотношений сторон
    print(f"\n--- РАСПРЕДЕЛЕНИЕ СООТНОШЕНИЙ ---")
    ratios_arr = np.array(ratios)
    for category, (min_val, max_val) in {
        "Очень узкие (вертикальные)": (0, 0.5),
        "Узкие": (0.5, 1.0),
        "Квадратные": (1.0, 1.5),
        "Широкие": (1.5, 3.0),
        "Очень широкие (горизонтальные)": (3.0, 10.0),
        "Экстремально широкие": (10.0, 1000.0)
    }.items():
        count = np.sum((ratios_arr >= min_val) & (ratios_arr < max_val))
        percent = (count / len(ratios)) * 100
        print(f"{category:<35}: {count:>4} images ({percent:5.1f}%)")

    # Покажем несколько примеров для каждой категории
    print(f"\n--- ПРИМЕРЫ ИЗОБРАЖЕНИЙ ---")
    sample_categories = {
        "Узкое (вертикальное)": (0, 0.5),
        "Стандартное": (1.5, 3.0),
        "Широкое (горизонтальное)": (3.0, 10.0)
    }

    for category, (min_ratio, max_ratio) in sample_categories.items():
        indices = [i for i, ratio in enumerate(ratios) if min_ratio <= ratio < max_ratio]
        if indices:
            sample_idx = indices[0]
            sample_path = lines[sample_idx].split('\t')[0]
            sample_ratio = ratios[sample_idx]
            print(f"{category}: {sample_path} (ratio: {sample_ratio:.2f})")

    # Анализ пригодности стандартного размера 320x48
    target_ratio = 320 / 48  # ≈ 6.67
    deviation = np.abs(ratios_arr - target_ratio)
    close_count = np.sum(deviation < 2.0)  # В пределах ±2 от целевого соотношения
    close_percent = (close_count / len(ratios)) * 100

    print(f"\n--- СООТВЕТСТВИЕ СТАНДАРТНОМУ ФОРМАТУ 320x48 ---")
    print(f"Целевое соотношение сторон: {target_ratio:.2f}")
    print(f"Изображений в пределах ±2.0: {close_count} ({close_percent:.1f}%)")

    if close_percent < 50:
        print("⚠️  ВНИМАНИЕ: Большинство изображений имеют нестандартное соотношение сторон!")
        print("   Это может быть причиной низкого качества обучения.")
        print("   Рекомендуется:")
        print("   1. Добавить аугментацию RecConAug в конфиг")
        print("   2. Рассмотреть изменение image_shape в конфиге")


# Запускаем анализ
if __name__ == "__main__":
    analyze_dataset_simple(label_file_path, base_data_dir)