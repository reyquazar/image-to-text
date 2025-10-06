import os
import shutil
import re


def create_pure_azerbaijani_cyrillic_dataset():
    """
    Создает ЧИСТЫЙ датасет только с азербайджанской кириллицей
    """
    rec_gt_path = "rec_gt.txt"
    base_dir = "."  # текущая директория где лежит rec_gt.txt
    output_dir = "pure_azerbaijani_cyrillic_dataset"

    # ТОЛЬКО азербайджанские кириллические символы
    AZERBAIJANI_CYRILLIC = set("әөһҹғүҝӘӨҺҸҒҮҜ")
    # РУССКИЕ символы (тоже разрешаем, так как часто используются вместе)
    RUSSIAN_CYRILLIC = set("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя")

    ALLOWED_CHARS = AZERBAIJANI_CYRILLIC | RUSSIAN_CYRILLIC | set(" '(),-.:;?0123456789")

    print("🔍 Поиск слов ТОЛЬКО с азербайджанской кириллицей...")

    # Чтение и фильтрация
    pure_data = []

    with open(rec_gt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) < 2:
                continue

            img_path, text = parts[0], parts[1]

            # Проверяем что текст содержит ТОЛЬКО разрешенные символы
            has_azerbaijani_cyrillic = any(char in AZERBAIJANI_CYRILLIC for char in text)
            has_only_allowed_chars = all(char in ALLOWED_CHARS for char in text)

            # Исключаем слова с латиницей
            has_latin = any(('A' <= char <= 'Z') or ('a' <= char <= 'z') for char in text)

            if has_azerbaijani_cyrillic and has_only_allowed_chars and not has_latin:
                pure_data.append((img_path, text))
                print(f"✅ Добавлен: {text}")

    print(f"📊 Найдено {len(pure_data)} ЧИСТЫХ примеров")

    if not pure_data:
        print("❌ Не найдено чистых данных")
        return

    # Создание папки
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Создание словаря из найденных символов
    all_chars = set()
    for _, text in pure_data:
        all_chars.update(text)

    # Сортировка символов
    sorted_chars = sorted(list(all_chars))

    # Создание словаря
    dict_path = os.path.join(output_dir, "dict.txt")
    with open(dict_path, 'w', encoding='utf-8') as f:
        for char in sorted_chars:
            f.write(char + '\n')

    print(f"📖 Создан словарь: {len(sorted_chars)} символов")
    print(f"Символы: {''.join(sorted_chars)}")

    # Копирование изображений и создание rec_gt.txt
    new_gt_path = os.path.join(output_dir, "rec_gt.txt")
    images_copied = 0
    images_missing = 0

    with open(new_gt_path, 'w', encoding='utf-8') as gt_file:
        for img_path, text in pure_data:
            # Пробуем разные возможные пути к изображениям
            possible_paths = [
                img_path,  # как в rec_gt.txt
                os.path.join("crop_img", os.path.basename(img_path)),
                os.path.join(".", img_path),
                os.path.join("text/typed_text", img_path)
            ]

            src_img_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    src_img_path = path
                    break

            if src_img_path and os.path.exists(src_img_path):
                dst_img_path = os.path.join(output_dir, os.path.basename(img_path))
                shutil.copy2(src_img_path, dst_img_path)
                gt_file.write(f"{os.path.basename(img_path)}\t{text}\n")
                images_copied += 1
                print(f"✅ Скопировано: {os.path.basename(img_path)}")
            else:
                print(f"❌ Не найдено: {img_path}")
                images_missing += 1

    # Создание train/val разделения
    create_train_val_split(output_dir)

    print(f"\n✅ ЧИСТЫЙ датасет создан!")
    print(f"📁 Папка: {output_dir}")
    print(f"📖 Словарь: {len(sorted_chars)} символов")
    print(f"🖼️  Изображений скопировано: {images_copied}")
    print(f"❌ Изображений не найдено: {images_missing}")


def create_train_val_split(dataset_dir):
    """Создает train/val разделение 80/20"""
    gt_path = os.path.join(dataset_dir, "rec_gt.txt")

    if not os.path.exists(gt_path):
        print(f"❌ Файл {gt_path} не найден!")
        return

    with open(gt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    if not lines:
        print("❌ Нет данных для разделения!")
        return

    import random
    random.shuffle(lines)

    split_idx = int(len(lines) * 0.8)
    train_lines = lines[:split_idx]
    val_lines = lines[split_idx:]

    with open(os.path.join(dataset_dir, "train_list.txt"), 'w', encoding='utf-8') as f:
        for line in train_lines:
            f.write(line)

    with open(os.path.join(dataset_dir, "val_list.txt"), 'w', encoding='utf-8') as f:
        for line in val_lines:
            f.write(line)

    print(f"📊 Разделение: {len(train_lines)} train, {len(val_lines)} val")


# Запуск
if __name__ == "__main__":
    create_pure_azerbaijani_cyrillic_dataset()