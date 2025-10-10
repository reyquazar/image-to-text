# Запустите проверку данных
import os


def check_dataset():
    train_file = "./text/typed_text/pure_azerbaijani_cyrillic_dataset/train_list.txt"

    with open(train_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    print(f"📊 Всего примеров: {len(lines)}")
    print("🔍 Примеры разметки:")
    for i in range(min(5, len(lines))):
        print(f"  {lines[i].strip()}")

    # Проверка азербайджанских символов
    az_chars = set('əıüöğşç')
    found_chars = set()
    for line in lines:
        text = line.split('\t')[-1].strip()
        found_chars.update(set(text) & az_chars)

    print(f"✅ Найдены азербайджанские символы: {found_chars}")
    print(f"❌ Отсутствуют: {az_chars - found_chars}")


check_dataset()