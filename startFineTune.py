import os


def check_images_from_list(list_file, base_dir):
    """Проверяет наличие всех изображений из списка"""
    print(f"🔍 Проверяем {list_file}...")

    if not os.path.exists(list_file):
        print(f"❌ Файл {list_file} не найден!")
        return

    missing_count = 0
    total_count = 0

    with open(list_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Разделяем имя файла и текст
            parts = line.split('\t')
            if len(parts) >= 1:
                filename = parts[0]
                image_path = os.path.join(base_dir, filename)

                total_count += 1

                if not os.path.exists(image_path):
                    print(f"❌ Отсутствует: {filename}")
                    missing_count += 1

    print(f"📊 Результат для {list_file}:")
    print(f"   Всего записей: {total_count}")
    print(f"   Отсутствует: {missing_count}")
    print(f"   Присутствует: {total_count - missing_count}")

    if missing_count == 0:
        print("✅ Все файлы на месте!")
    else:
        print("⚠️  Некоторые файлы отсутствуют!")

    print()
    return missing_count


def main():
    # Укажите путь к папке с изображениями
    base_dir = "./text/typed_text/az_config_train"

    # Проверяем train_list.txt
    train_missing = check_images_from_list(
        os.path.join(base_dir, "train_list.txt"),
        base_dir
    )

    # Проверяем val_list.txt
    val_missing = check_images_from_list(
        os.path.join(base_dir, "val_list.txt"),
        base_dir
    )

    # Итог
    total_missing = train_missing + val_missing
    if total_missing == 0:
        print("🎉 Все файлы на месте! Можно начинать обучение.")
    else:
        print(f"⚠️  Всего отсутствует файлов: {total_missing}")


if __name__ == "__main__":
    main()