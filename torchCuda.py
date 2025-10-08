print("=== ПРОВЕРКА СОВПАДЕНИЯ СИМВОЛОВ ===")

# Загрузи словарь
with open('./text/typed_text/pure_azerbaijani_cyrillic_dataset3/dict.txt', 'r', encoding='utf-8') as f:
    dict_chars = {line.strip() for line in f.readlines()}

print(f"Символов в словаре: {len(dict_chars)}")
print(f"Первые 10 символов: {list(dict_chars)[:10]}")

# Проверь символы из твоих лейблов
with open('./text/typed_text/pure_azerbaijani_cyrillic_dataset3/train_list.txt', 'r', encoding='utf-8') as f:
    missing_chars = set()
    for line in f.readlines()[:10]:
        _, label = line.strip().split('\t')
        for char in label:
            if char not in dict_chars:
                missing_chars.add(char)

    if missing_chars:
        print(f"🚨 ОТСУТСТВУЮТ СИМВОЛЫ В СЛОВАРЕ: {missing_chars}")
    else:
        print("✅ Все символы из лейблов есть в словаре")

# Проверь обратное - есть ли в словаре лишние символы
print(f"Пример символов из словаря: {''.join(list(dict_chars)[:20])}")