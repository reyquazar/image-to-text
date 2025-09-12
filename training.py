def create_vocabulary(input_file, output_file):
    unique_chars = set()

    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                text = parts[1]
                unique_chars.update(text)

    sorted_chars = sorted(unique_chars)

    with open(output_file, 'w', encoding='utf-8') as f:
        for char in sorted_chars:
            f.write(char + '\n')

    print(f"Создан словарь: {output_file}")
    print(f"Найдено уникальных символов: {len(sorted_chars)}")
    print("Символы:", ''.join(sorted_chars))
#

input_file = 'text/test/rec_gt.txt'  # Ваш файл с разметкой
output_file = 'text/test/dict.txt'  # Выходной файл словаря
create_vocabulary(input_file, output_file)
#
# import os
#
#
# def check_images_exist():
#     with open('./text/typed_text/train_list.txt', 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#
#     for i, line in enumerate(lines):  # проверяем первые 10
#         parts = line.strip().split('\t')
#         if len(parts) >= 2:
#             img_path = os.path.join('./text/typed_text', parts[0])
#             if os.path.exists(img_path):
#                 print(f"✓ {img_path}")
#             else:
#                 print(f"✗ {img_path} - НЕ СУЩЕСТВУЕТ!")
#         else:
#             print(f"✗ Неправильный формат: {line}")
#
#
# check_images_exist()

import paddle
import cv2
import numpy as np

# # Проверка одного примера
# sample_line = "путь/к/изображению.jpg\tтекст"
# img_path, true_label = sample_line.split('\t')
#
# # Проверка изображения
# img = cv2.imread(img_path)
# print(f"Image shape: {img.shape}")
# print(f"True label: {true_label}")
#
# # Проверка словаря
# with open('./text/typed_text/az_ru_dict.txt', 'r', encoding='utf-8') as f:
#     chars = [line.strip() for line in f]
# print(f"Chars in dict: {len(chars)}")
# print(f"First 10 chars: {chars[:10]}")