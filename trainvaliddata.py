import os
import random
from sklearn.model_selection import train_test_split


def create_mixed_dataset(real_gt_path, synthetic_gt_path, output_dir, val_ratio=0.2, random_seed=42):
    """
    Создает перемешанный датасет с train/val разделением из реальных и синтетических данных

    Args:
        real_gt_path: путь к файлу с реальными данными
        synthetic_gt_path: путь к файлу с синтетическими данными
        output_dir: директория для выходных файлов
        val_ratio: доля данных для validation (0.0-1.0)
        random_seed: seed для воспроизводимости
    """

    # Создаем выходную директорию
    os.makedirs(output_dir, exist_ok=True)

    # Загружаем данные
    real_data = []
    synthetic_data = []

    # Загрузка реальных данных
    if os.path.exists(real_gt_path):
        with open(real_gt_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '\t' in line:
                    real_data.append(line)
        print(f"Загружено реальных данных: {len(real_data)}")
    else:
        print(f"Файл с реальными данными не найден: {real_gt_path}")

    # Загрузка синтетических данных
    if os.path.exists(synthetic_gt_path):
        with open(synthetic_gt_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and '\t' in line:
                    synthetic_data.append(line)
        print(f"Загружено синтетических данных: {len(synthetic_data)}")
    else:
        print(f"Файл с синтетическими данными не найден: {synthetic_gt_path}")

    if not real_data and not synthetic_data:
        print("Нет данных для обработки!")
        return

    # Объединяем и перемешиваем данные
    all_data = real_data + synthetic_data
    random.seed(random_seed)
    random.shuffle(all_data)

    print(f"Всего данных после объединения: {len(all_data)}")
    print(f"Реальных: {len(real_data)} ({len(real_data) / len(all_data) * 100:.1f}%)")
    print(f"Синтетических: {len(synthetic_data)} ({len(synthetic_data) / len(all_data) * 100:.1f}%)")

    # Разделяем на train/val
    train_data, val_data = train_test_split(
        all_data,
        test_size=val_ratio,
        random_state=random_seed,
        shuffle=True
    )

    # Сохраняем train файл
    train_file_path = os.path.join(output_dir, "train_mixed.txt")
    with open(train_file_path, 'w', encoding='utf-8') as f:
        for line in train_data:
            f.write(line + '\n')

    # Сохраняем val файл
    val_file_path = os.path.join(output_dir, "val_mixed.txt")
    with open(val_file_path, 'w', encoding='utf-8') as f:
        for line in val_data:
            f.write(line + '\n')

    # Сохраняем полный файл (опционально)
    full_file_path = os.path.join(output_dir, "full_mixed.txt")
    with open(full_file_path, 'w', encoding='utf-8') as f:
        for line in all_data:
            f.write(line + '\n')

    print(f"\nРезультаты разделения:")
    print(f"Train samples: {len(train_data)}")
    print(f"Val samples: {len(val_data)}")
    print(f"Val ratio: {val_ratio * 100:.1f}%")
    print(f"\nФайлы сохранены в: {output_dir}")
    print(f"  - Train: {train_file_path}")
    print(f"  - Val: {val_file_path}")
    print(f"  - Full: {full_file_path}")


def analyze_dataset(gt_file_path):
    """Анализирует датасет и выводит статистику"""
    if not os.path.exists(gt_file_path):
        print(f"Файл не найден: {gt_file_path}")
        return

    data = []
    with open(gt_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and '\t' in line:
                data.append(line)

    print(f"\nАнализ файла: {gt_file_path}")
    print(f"Всего строк: {len(data)}")

    # Анализ длины текстов
    text_lengths = []
    for line in data:
        parts = line.split('\t')
        if len(parts) >= 2:
            text_lengths.append(len(parts[1]))

    if text_lengths:
        print(f"Средняя длина текста: {sum(text_lengths) / len(text_lengths):.1f} символов")
        print(f"Мин. длина: {min(text_lengths)}")
        print(f"Макс. длина: {max(text_lengths)}")


# Основное выполнение
if __name__ == "__main__":
    # Настройки
    REAL_GT_PATH = "text/typed_text/train_list.txt"  # ваши реальные данные
    SYNTHETIC_GT_PATH = "text/typed_text/synthetic_data/synthetic_gt.txt"  # синтетические данные
    OUTPUT_DIR = "text/typed_text/mixed_data"  # выходная директория
    VAL_RATIO = 0.15  # 15% на validation (можно изменить)
    RANDOM_SEED = 42  # для воспроизводимости

    # Анализируем исходные данные
    print("=== АНАЛИЗ ИСХОДНЫХ ДАННЫХ ===")
    analyze_dataset(REAL_GT_PATH)
    analyze_dataset(SYNTHETIC_GT_PATH)

    # Создаем перемешанный датасет
    print("\n=== СОЗДАНИЕ ПЕРЕМЕШАННОГО ДАТАСЕТА ===")
    create_mixed_dataset(
        real_gt_path=REAL_GT_PATH,
        synthetic_gt_path=SYNTHETIC_GT_PATH,
        output_dir=OUTPUT_DIR,
        val_ratio=VAL_RATIO,
        random_seed=RANDOM_SEED
    )

    # Анализируем результат
    print("\n=== АНАЛИЗ РЕЗУЛЬТАТОВ ===")
    analyze_dataset(os.path.join(OUTPUT_DIR, "train_mixed.txt"))
    analyze_dataset(os.path.join(OUTPUT_DIR, "val_mixed.txt"))

    print("\n=== ИНСТРУКЦИЯ ===")
    print("Обновите конфиг PaddleOCR:")
    print("Train:")
    print("  label_file_list: [\"text/typed_text/mixed_data/train_mixed.txt\"]")
    print("Eval:")
    print("  label_file_list: [\"text/typed_text/mixed_data/val_mixed.txt\"]")