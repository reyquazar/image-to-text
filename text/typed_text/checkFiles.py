import os
import cv2
import numpy as np
from pathlib import Path


def check_directory_contents(directory):
    print("=" * 50)
    print(f"ПРОВЕРКА КАТАЛОГА: {directory}")
    print("=" * 50)

    # Проверка dict.txt
    print("\n1. dict.txt:")
    dict_path = os.path.join(directory, 'dict.txt')
    if os.path.exists(dict_path):
        with open(dict_path, 'r', encoding='utf-8') as f:
            chars = [line.strip() for line in f.readlines()]
            print(f"   Символов: {len(chars)}")
            print(f"   Содержимое: {''.join(chars)}")
    else:
        print("   Файл не найден!")

    # Проверка train_list.txt
    print("\n2. train_list.txt:")
    train_list_path = os.path.join(directory, 'train_list.txt')
    if os.path.exists(train_list_path):
        with open(train_list_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   Строк: {len(lines)}")
            for i, line in enumerate(lines[:5]):  # первые 5 строк
                print(f"   Строка {i + 1}: {repr(line.strip())}")
    else:
        print("   Файл не найден!")

    # Проверка val_list.txt
    print("\n3. val_list.txt:")
    val_list_path = os.path.join(directory, 'val_list.txt')
    if os.path.exists(val_list_path):
        with open(val_list_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   Строк: {len(lines)}")
            for i, line in enumerate(lines[:5]):
                print(f"   Строка {i + 1}: {repr(line.strip())}")
    else:
        print("   Файл не найден!")

    # Проверка rec_gt.txt
    print("\n4. rec_gt.txt:")
    rec_gt_path = os.path.join(directory, 'rec_gt.txt')
    if os.path.exists(rec_gt_path):
        with open(rec_gt_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"   Строк: {len(lines)}")
            for i, line in enumerate(lines[:5]):
                print(f"   Строка {i + 1}: {repr(line.strip())}")
    else:
        print("   Файл не найден!")

    # Проверка изображений
    print("\n5. ИЗОБРАЖЕНИЯ:")
    image_files = ['img1.jpg', 'img2.jpg', 'img3.jpg']
    for img_file in image_files:
        img_path = os.path.join(directory, img_file)
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            if img is not None:
                print(f"   {img_file}: {img.shape} (HxWxC), пиксели [{img.min()}-{img.max()}]")
            else:
                print(f"   {img_file}: НЕ ЧИТАЕТСЯ!")
        else:
            print(f"   {img_file}: НЕ НАЙДЕН!")

    # Проверка совпадения символов
    print("\n6. СОВПАДЕНИЕ СИМВОЛОВ:")
    if os.path.exists(dict_path) and os.path.exists(train_list_path):
        with open(dict_path, 'r', encoding='utf-8') as f:
            dict_chars = {line.strip() for line in f.readlines()}

        with open(train_list_path, 'r', encoding='utf-8') as f:
            missing_chars = set()
            for line in f.readlines():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    label = parts[1]
                    for char in label:
                        if char not in dict_chars:
                            missing_chars.add(char)

            if missing_chars:
                print(f"   🚨 Отсутствуют символы: {missing_chars}")
            else:
                print(f"   ✅ Все символы есть в словаре")


# Запуск проверки
directory = r"C:\Users\elsha\Downloads\image-to-text\text\debug"
check_directory_contents(directory)
