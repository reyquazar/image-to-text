def length(txtFile):
    max_len = 0
    with open(txtFile, 'r', encoding='utf-8') as f:
        for line in f:
            # Предполагается формат: path/to/image.jpg\tтекст
            label = line.strip().split('\t')[1]
            if len(label) > max_len:
                max_len = len(label)
                longest_text = label
    print(f"Максимальная длина текста в train: {max_len}")
    print(f"Самый длинный текст: '{longest_text}'")


def lengthArray(txtFile):
    array = {}
    with open(txtFile, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.split('.jpg', 1)
            # print(parts[1])
            label = parts[1].strip()
            # print(label)
            # if len(label) > 15:
            array[label] = parts[0]
    # print(len(array))
    i = 1
    for key, value in array.items():
        print(f"{i}. {key}\t{value}")
        i += 1


rec_gt_path = "./text/typed_text/rec_gt.txt"
# val_path = "./text/typed_text/.txt"

lengthArray(rec_gt_path)
