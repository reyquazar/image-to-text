import os
import cv2
from collections import defaultdict


def analyze_image_sizes(folder_path):
    """
    Анализирует размеры всех изображений в папке
    """
    # Словарь для хранения статистики
    sizes_dict = defaultdict(int)
    size_details = []

    # Поддерживаемые форматы изображений
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}

    print("Анализ размеров изображений...")
    print("-" * 50)

    # Проходим по всем файлам в папке
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Проверяем, что это файл и имеет правильное расширение
        if os.path.isfile(file_path) and any(filename.lower().endswith(ext) for ext in valid_extensions):
            try:
                # Загружаем изображение
                img = cv2.imread(file_path)
                if img is not None:
                    height, width = img.shape[:2]

                    # Сохраняем размер
                    size_key = (width, height)
                    sizes_dict[size_key] += 1
                    size_details.append({
                        'filename': filename,
                        'width': width,
                        'height': height,
                        'aspect_ratio': round(width / height, 2)
                    })

                    print(f"{filename:.<30} {width} x {height} (соотношение: {width / height:.2f})")
                else:
                    print(f"Ошибка загрузки: {filename}")

            except Exception as e:
                print(f"Ошибка обработки {filename}: {e}")

    return sizes_dict, size_details


def print_statistics(sizes_dict, size_details):
    """
    Выводит статистику по размерам изображений
    """
    print("\n" + "=" * 50)
    print("СТАТИСТИКА РАЗМЕРОВ ИЗОБРАЖЕНИЙ")
    print("=" * 50)

    if not sizes_dict:
        print("Не найдено изображений для анализа")
        return

    # Общее количество изображений
    total_images = len(size_details)
    print(f"Всего изображений: {total_images}")

    # Статистика по размерам
    print(f"\nУникальные размеры: {len(sizes_dict)}")
    print("\nРаспределение по размерам:")
    print("-" * 30)

    # Сортируем по частоте встречаемости
    sorted_sizes = sorted(sizes_dict.items(), key=lambda x: x[1], reverse=True)

    for (width, height), count in sorted_sizes:
        percentage = (count / total_images) * 100
        print(f"{width} x {height}: {count} шт. ({percentage:.1f}%)")

    # Находим минимальные и максимальные размеры
    widths = [detail['width'] for detail in size_details]
    heights = [detail['height'] for detail in size_details]
    aspect_ratios = [detail['aspect_ratio'] for detail in size_details]

    print(f"\nМинимальная ширина: {min(widths)}")
    print(f"Максимальная ширина: {max(widths)}")
    print(f"Средняя ширина: {sum(widths) / len(widths):.1f}")

    print(f"\nМинимальная высота: {min(heights)}")
    print(f"Максимальная высота: {max(heights)}")
    print(f"Средняя высота: {sum(heights) / len(heights):.1f}")

    print(f"\nМинимальное соотношение сторон: {min(aspect_ratios):.2f}")
    print(f"Максимальное соотношение сторон: {max(aspect_ratios):.2f}")
    print(f"Среднее соотношение сторон: {sum(aspect_ratios) / len(aspect_ratios):.2f}")

    # Самые частые соотношения сторон
    aspect_ratio_counts = defaultdict(int)
    for ar in aspect_ratios:
        aspect_ratio_counts[ar] += 1

    print(f"\nСамые частые соотношения сторон:")
    for ar, count in sorted(aspect_ratio_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
        percentage = (count / total_images) * 100
        print(f"  {ar}: {count} шт. ({percentage:.1f}%)")


def save_results_to_file(size_details, output_file="image_sizes_report.txt"):
    """
    Сохраняет детальный отчет в файл
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("ОТЧЕТ ПО РАЗМЕРАМ ИЗОБРАЖЕНИЙ\n")
        f.write("=" * 50 + "\n\n")

        f.write("Детальный список:\n")
        f.write("-" * 50 + "\n")
        for detail in size_details:
            f.write(f"{detail['filename']}: {detail['width']} x {detail['height']} "
                    f"(соотношение: {detail['aspect_ratio']})\n")


def main():
    # Укажите путь к вашей папке с изображениями
    folder_path = "C:/Users/elsha/Downloads/image-to-text/text/typed_text/az_config_train"

    # Проверяем существование папки
    if not os.path.exists(folder_path):
        print(f"Ошибка: Папка {folder_path} не существует!")
        return

    # Анализируем размеры
    sizes_dict, size_details = analyze_image_sizes(folder_path)

    # Выводим статистику
    print_statistics(sizes_dict, size_details)

    # Сохраняем отчет в файл
    save_results_to_file(size_details)
    print(f"\nДетальный отчет сохранен в файл: image_sizes_report.txt")


if __name__ == "__main__":
    main()