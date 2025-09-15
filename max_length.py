max_len = 0
with open('./text/typed_text/rec_gt.txt', 'r', encoding='utf-8') as f:
    for line in f:
        # Предполагается формат: path/to/image.jpg\tтекст
        label = line.strip().split('\t')[1]
        if len(label) > max_len:
            max_len = len(label)
            longest_text = label

print(f"Максимальная длина текста в train: {max_len}")
print(f"Самый длинный текст: '{longest_text}'")

# Сделайте то же самое для val_list.txt