import os
from pathlib import Path


def create_image_list_txt(folder_path, output_file, labels):
    """
    Создает txt файл со списком изображений и соответствующими метками

    Args:
        folder_path: путь к папке с изображениями
        output_file: имя выходного txt файла
        labels: список меток для изображений
    """
    # Получаем список всех jpg файлов в папке
    image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')])

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, image_file in enumerate(image_files):
            # Формируем полный путь к изображению
            full_path = os.path.join(folder_path, image_file)

            # Берем метку из списка или используем заглушку
            label = labels[i] if i < len(labels) else f"Метка_{i}"

            # Записываем в файл
            f.write(f"{full_path}\t{label}\n")

    print(f"Файл {output_file} успешно создан с {len(image_files)} записями")


# Пример использования
folder_path = "crop_img"
output_file = "image_list.txt"
labels = ["Ады", "Имя", "2"]  # Ваши метки

create_image_list_txt(folder_path, output_file, labels)
