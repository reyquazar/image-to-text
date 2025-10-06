import os
import shutil
import re


def create_azerbaijani_cyrillic_dataset():
    # Пути к файлам (измените при необходимости)
    rec_gt_path = "rec_gt.txt"
    dict_path = "dict.txt"
    images_dir = "crop_img"  # текущая директория с изображениями
    output_dir = "azerbaijani_cyrillic_dataset"

    # Азербайджанские кириллические символы
    AZERBAIJANI_CYRILLIC = set("әөһҹғүҝӘӨҺҸҒҮҜ")

    print("🔍 Поиск слов с азербайджанской кириллицей...")

    # Чтение rec_gt.txt и фильтрация
    azerbaijani_data = []
    all_chars = set()

    if not os.path.exists(rec_gt_path):
        print(f"❌ Файл {rec_gt_path} не найден!")
        return

    with open(rec_gt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Разделяем путь к изображению и текст
            parts = line.split('\t')
            if len(parts) < 2:
                continue

            img_path, text = parts[0], parts[1]

            # Проверяем наличие азербайджанских кириллических символов
            if any(char in AZERBAIJANI_CYRILLIC for char in text):
                azerbaijani_data.append((img_path, text))
                all_chars.update(text)

    print(f"📊 Найдено {len(azerbaijani_data)} примеров с азербайджанской кириллицей")
    print(f"📝 Уникальных символов: {len(all_chars)}")

    if not azerbaijani_data:
        print("❌ Не найдено данных с азербайджанской кириллицей")
        return

    # Создание словаря
    print("\n📖 Создание словаря...")

    # Базовый набор символов (можно расширить при необходимости)
    base_chars = set(" '(),-.:;?ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    base_chars.update("ÇçƏəĞğİıÖöŞşÜü")  # латинские азербайджанские
    base_chars.update("АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя")  # русские
    base_chars.update(all_chars)  # добавляем найденные символы

    # Сортируем символы для удобства
    sorted_chars = sorted(list(base_chars))

    print(f"📚 Словарь будет содержать {len(sorted_chars)} символов")
    print("Первые 50 символов:", ''.join(sorted_chars[:50]))

    # Запрос подтверждения
    print(f"\n⚠️  Будет создана папка '{output_dir}' и перенесено {len(azerbaijani_data)} изображений")
    confirmation = input("Продолжить? (y/n): ").strip().lower()

    if confirmation not in ['y', 'yes', 'д', 'да']:
        print("❌ Операция отменена")
        return

    # Создание папки
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Создание словаря
    with open(os.path.join(output_dir, dict_path), 'w', encoding='utf-8') as f:
        for char in sorted_chars:
            f.write(char + '\n')

    # Создание нового rec_gt.txt и копирование изображений
    new_gt_path = os.path.join(output_dir, "rec_gt.txt")
    images_copied = 0
    images_missing = 0

    with open(new_gt_path, 'w', encoding='utf-8') as gt_file:
        for img_path, text in azerbaijani_data:
            # Проверяем существование исходного изображения
            if os.path.exists(img_path):
                # Копируем изображение
                new_img_path = os.path.join(output_dir, os.path.basename(img_path))
                shutil.copy2(img_path, new_img_path)

                # Записываем в новый rec_gt.txt
                gt_file.write(f"{os.path.basename(img_path)}\t{text}\n")
                images_copied += 1
            else:
                print(f"⚠️  Изображение не найдено: {img_path}")
                images_missing += 1

    # Создание train/val разделения (80/20)
    create_train_val_split(output_dir)

    print(f"\n✅ Готово!")
    print(f"📁 Создана папка: {output_dir}")
    print(f"📖 Создан словарь: {dict_path} ({len(sorted_chars)} символов)")
    print(f"🖼️  Скопировано изображений: {images_copied}")
    print(f"❌ Отсутствовало изображений: {images_missing}")
    print(f"📊 Созданы train_list.txt и val_list.txt")


def create_train_val_split(dataset_dir):
    """Создает train/val разделение 80/20"""
    gt_path = os.path.join(dataset_dir, "rec_gt.txt")

    if not os.path.exists(gt_path):
        print("❌ Файл rec_gt.txt не найден для разделения")
        return

    # Читаем все данные
    with open(gt_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Перемешиваем для случайного разделения
    import random
    random.shuffle(lines)

    # Разделяем 80/20
    split_idx = int(len(lines) * 0.8)
    train_lines = lines[:split_idx]
    val_lines = lines[split_idx:]

    # Записываем train_list.txt
    with open(os.path.join(dataset_dir, "train_list.txt"), 'w', encoding='utf-8') as f:
        for line in train_lines:
            f.write(line)

    # Записываем val_list.txt
    with open(os.path.join(dataset_dir, "val_list.txt"), 'w', encoding='utf-8') as f:
        for line in val_lines:
            f.write(line)

    print(f"📊 Разделение: {len(train_lines)} train, {len(val_lines)} val")


def analyze_dataset():
    """Анализ текущего датасета"""
    rec_gt_path = "rec_gt.txt"
    AZERBAIJANI_CYRILLIC = set("әөһҹғүҝӘӨҺҸҒҮҜ")

    if not os.path.exists(rec_gt_path):
        print(f"❌ Файл {rec_gt_path} не найден!")
        return

    stats = {
        'total': 0,
        'azerbaijani_cyrillic': 0,
        'russian_only': 0,
        'latin_only': 0,
        'mixed': 0
    }

    with open(rec_gt_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            parts = line.split('\t')
            if len(parts) < 2:
                continue

            text = parts[1]
            stats['total'] += 1

            has_cyrillic = any(char in AZERBAIJANI_CYRILLIC for char in text)
            has_russian = any('А' <= char <= 'я' for char in text)
            has_latin = any('A' <= char <= 'z' for char in text)

            if has_cyrillic:
                stats['azerbaijani_cyrillic'] += 1
            elif has_russian and not has_latin:
                stats['russian_only'] += 1
            elif has_latin and not has_russian:
                stats['latin_only'] += 1
            else:
                stats['mixed'] += 1

    print("\n📊 Анализ датасета:")
    print(f"Всего примеров: {stats['total']}")
    print(f"Азербайджанская кириллица: {stats['azerbaijani_cyrillic']}")
    print(f"Только русские: {stats['russian_only']}")
    print(f"Только латиница: {stats['latin_only']}")
    print(f"Смешанные: {stats['mixed']}")


if __name__ == "__main__":
    print("🎯 Создание датасета с азербайджанской кириллицей")
    print("=" * 50)

    # Сначала покажем анализ
    analyze_dataset()
    print("\n" + "=" * 50)

    # Затем предложим создать датасет
    create_azerbaijani_cyrillic_dataset()