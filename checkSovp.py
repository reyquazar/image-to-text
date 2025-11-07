images_path = './text/typed_text/az_config_train/'
train_path = './text/typed_text/az_config_train/train_list.txt'
val_path = './text/typed_text/az_config_train/val_list.txt'

# Чтение слов из train файла
train_words = set()
with open(train_path, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            train_words.add(parts[1])  # Вторая часть - слово

# Чтение слов из val файла и проверка
with open(val_path, 'r', encoding='utf-8') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) >= 2:
            word = parts[1]
            if word in train_words:
                print("ДА: Найдены общие слова между train и val")
                break
    else:
        print("НЕТ: Общих слов между train и val не найдено")