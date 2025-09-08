# create_dict.py
def create_vocabulary(input_file, output_file):
    unique_chars = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                text = parts[1]  # Берем текст после табуляции
                unique_chars.update(text)  # Добавляем все символы текста

    sorted_chars = sorted(unique_chars)

    with open(output_file, 'w', encoding='utf-8') as f:
        for char in sorted_chars:
            f.write(char + '\n')

    print(f"Создан словарь: {output_file}")
    print(f"Найдено уникальных символов: {len(sorted_chars)}")
    print("Символы:", ''.join(sorted_chars))


input_file = 'text/typed_text/rec_gt.txt'  # Ваш файл с разметкой
output_file = 'text/typed_text/az_ru_dict.txt'  # Выходной файл словаря
create_vocabulary(input_file, output_file)