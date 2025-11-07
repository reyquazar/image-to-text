import os
import random


def split_dataset(input_file, output_dir, train_ratio=0.8):
    """
    Разделяет файл с разметкой на train и val
    """
    # Читаем все строки из файла
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Очищаем строки от лишних пробелов
    lines = [line.strip() for line in lines if line.strip()]

    # Перемешиваем данные для случайного разделения
    random.shuffle(lines)

    # Разделяем на train и val
    split_index = int(len(lines) * train_ratio)
    train_lines = lines[:split_index]
    val_lines = lines[split_index:]

    # Создаем директорию если не существует
    os.makedirs(output_dir, exist_ok=True)

    # Записываем train файл
    train_file = os.path.join(output_dir, 'train_list.txt')
    with open(train_file, 'w', encoding='utf-8') as f:
        for line in train_lines:
            f.write(line + '\n')

    # Записываем val файл
    val_file = os.path.join(output_dir, 'val_list.txt')
    with open(val_file, 'w', encoding='utf-8') as f:
        for line in val_lines:
            f.write(line + '\n')

    print(f"✅ Разделение завершено!")
    print(f"📊 Всего примеров: {len(lines)}")
    print(f"🚂 Train: {len(train_lines)} примеров")
    print(f"🧪 Val: {len(val_lines)} примеров")
    print(f"📁 Train файл: {train_file}")
    print(f"📁 Val файл: {val_file}")

    return train_file, val_file


# Использование
if __name__ == "__main__":
    # input_file = './text/debug/rec_gt.txt'
    # output_dir = './text/debug/'

    input_file = './text/typed_text/rec_gt.txt'
    output_dir = './text/typed_text/'

    train_file, val_file = split_dataset(input_file, output_dir)

# import os
# from sklearn.model_selection import train_test_split
#
#
# def split_dataset_sklearn(input_file, output_dir, train_ratio=0.8, random_seed=42):
#     """
#     Разделяет файл с разметкой на train и val используя sklearn
#     """
#     # Читаем все строки из файла
#     with open(input_file, 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#
#     # Очищаем строки от лишних пробелов
#     lines = [line.strip() for line in lines if line.strip()]
#
#     # Разделяем на train и val с помощью sklearn
#     train_lines, val_lines = train_test_split(
#         lines,
#         train_size=train_ratio,
#         random_state=random_seed,
#         shuffle=True
#     )
#
#     # Создаем директорию если не существует
#     os.makedirs(output_dir, exist_ok=True)
#
#     # Записываем train файл
#     train_file = os.path.join(output_dir, 'train_list.txt')
#     with open(train_file, 'w', encoding='utf-8') as f:
#         for line in train_lines:
#             f.write(line + '\n')
#
#     # Записываем val файл
#     val_file = os.path.join(output_dir, 'val_list.txt')
#     with open(val_file, 'w', encoding='utf-8') as f:
#         for line in val_lines:
#             f.write(line + '\n')
#
#     print(f"✅ Разделение завершено (sklearn)!")
#     print(f"📊 Всего примеров: {len(lines)}")
#     print(f"🚂 Train: {len(train_lines)} примеров")
#     print(f"🧪 Val: {len(val_lines)} примеров")
#     print(f"📁 Train файл: {train_file}")
#     print(f"📁 Val файл: {val_file}")
#
#     return train_file, val_file
#
#
# # Использование
# if __name__ == "__main__":
#     input_file = './text/typed_text/rec_gt.txt'
#     output_dir = './text/typed_text/python/'
#
#     train_file, val_file = split_dataset_sklearn(input_file, output_dir)
