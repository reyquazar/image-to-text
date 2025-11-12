def find_max_length_simple(filename):
    """Простая версия для нахождения максимальной длины"""
    max_length = 0
    max_line = ""

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Разделяем строку после .jpg
            if '.jpg' in line:
                parts = line.split('.jpg', 1)
                if len(parts) > 1:
                    right_part = parts[1].strip()
                    # Убираем начальные табуляции/пробелы
                    right_part = right_part.lstrip('\t ')
                    current_length = len(right_part)

                    if current_length > max_length:
                        max_length = current_length
                        max_line = right_part

    return max_length, max_line


# Использование
filename = "text/typed_text/fortrain/rec_gt.txt"  # Укажите путь к вашему файлу
max_len, max_text = find_max_length_simple(filename)

print(f"Максимальная длина строки: {max_len} символов")
print(f"Самая длинная строка: '{max_text}'")
