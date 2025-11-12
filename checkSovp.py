images_path = './text/typed_text/az_config_train/'
train_path = './text/typed_text/az_config_train/train_list.txt'
val_path = './text/typed_text/az_config_train/val_list.txt'


def find_common_words_detailed(train_path, val_path):
    """
    Находит общие слова и показывает где они встречаются в обоих файлах
    """
    # Чтение слов из train файла с информацией о строках
    train_words = {}
    with open(train_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            parts = line.strip().split()
            if len(parts) >= 2:
                word = parts[1]
                if word not in train_words:
                    train_words[word] = []
                train_words[word].append(line_num)

    # Поиск общих слов в val файле
    common_words_info = []

    with open(val_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            parts = line.strip().split()
            if len(parts) >= 2:
                word = parts[1]
                if word in train_words:
                    common_words_info.append({
                        'word': word,
                        'val_line': line_num,
                        'val_full_line': line.strip(),
                        'train_lines': train_words[word]
                    })

    return common_words_info, len(train_words)


# Запуск проверки
common_words_info, train_words_count = find_common_words_detailed(train_path, val_path)

print("=" * 70)
print("ДЕТАЛЬНАЯ ПРОВЕРКА ОБЩИХ СЛОВ МЕЖДУ TRAIN И VAL")
print("=" * 70)

if common_words_info:
    print(f"❌ ДА: Найдены общие слова между train и val")
    print(f"\n📊 Статистика:")
    print(f"   Всего уникальных слов в train: {train_words_count}")
    print(f"   Найдено общих слов: {len(common_words_info)}")

    print(f"\n🔍 Подробная информация об общих словах:")
    print("=" * 70)

    for i, info in enumerate(common_words_info, 1):
        print(f"\n{i:2d}. Слово: '{info['word']}'")
        print(f"    ├─ В VAL файле (строка {info['val_line']}):")
        print(f"    │   {info['val_full_line']}")
        print(f"    └─ В TRAIN файле (строки {info['train_lines']})")

else:
    print(f"✅ НЕТ: Общих слов между train и val не найдено")
    print(f"   Всего уникальных слов в train: {train_words_count}")

print("=" * 70)