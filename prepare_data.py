# prepare_paddleocr_data.py
import os
import ast


def convert_rec_gt():
    """Convert last_rec_gt.txt to PaddleOCR format"""
    input_file = "newData/last_rec_gt.txt"
    output_file = "newData/rec_gt_train.txt"

    print(f"Converting {input_file}...")

    with open(input_file, 'r', encoding='utf-8') as f_in, \
            open(output_file, 'w', encoding='utf-8') as f_out:

        for line in f_in:
            line = line.strip()
            if '\t' in line:
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    image_path, text = parts
                    # Исправляем путь к изображениям
                    if image_path.startswith('crop_img/'):
                        image_path = image_path.replace('crop_img/', 'newData/lastCropImg/')
                    f_out.write(f"{image_path}\t{text}\n")

    print(f"Converted to {output_file}")
    return output_file


def convert_lastlabel():
    """Convert lastLabel.txt to PaddleOCR format"""
    input_file = "newData/lastLabel.txt"
    output_file = "newData/det_gt_train.txt"

    print(f"Converting {input_file}...")

    def parse_points(points):
        """Convert points to PaddleOCR format"""
        if isinstance(points, list) and len(points) >= 4:
            coords = []
            for point in points[:4]:
                if isinstance(point, list) and len(point) >= 2:
                    coords.extend([str(point[0]), str(point[1])])
            return coords
        return []

    with open(input_file, 'r', encoding='utf-8') as f_in, \
            open(output_file, 'w', encoding='utf-8') as f_out:

        line_count = 0
        success_count = 0

        for line in f_in:
            line = line.strip()
            line_count += 1

            if '\t' in line:
                image_path, json_str = line.split('\t', 1)

                try:
                    # Пытаемся распарсить JSON-like строку
                    data = ast.literal_eval(json_str)

                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                transcription = item.get('transcription', '')
                                points = item.get('points', [])

                                if transcription and points:
                                    points_str = parse_points(points)
                                    if points_str:
                                        points_line = ','.join(points_str)
                                        f_out.write(f"{image_path}\t[{points_line}]\t{transcription}\n")
                                        success_count += 1

                except (SyntaxError, ValueError, IndexError) as e:
                    print(f"Error parsing line {line_count}: {e}")
                    continue

    print(f"Converted {success_count} annotations to {output_file}")
    return output_file


def merge_data(rec_file, det_file):
    """Merge both files into final training data"""
    output_file = "newData/final_train_list.txt"

    print("Merging data files...")

    total_lines = 0
    with open(output_file, 'w', encoding='utf-8') as out_f:
        # Добавляем данные из rec файла
        if os.path.exists(rec_file):
            with open(rec_file, 'r', encoding='utf-8') as f:
                content = f.read()
                out_f.write(content)
                total_lines += content.count('\n')

        # Добавляем данные из det файла
        if os.path.exists(det_file):
            with open(det_file, 'r', encoding='utf-8') as f:
                content = f.read()
                out_f.write(content)
                total_lines += content.count('\n')

    print(f"Merged {total_lines} lines into {output_file}")
    return output_file


def create_character_dict():
    """Create character dictionary for Azerbaijani and Russian"""
    chars_file = "ppocr_keys_v1.txt"

    # Все символы азербайджанского, русского и специальные символы
    azeri_latin = "ABCÇDEƏFGĞHXIİJKQLMNOÖPRSŞTUÜVYZabcçdeəfgğhxıijklmnoöprsştuüvyz"
    azeri_cyrillic = "АаБбВвГгДдЕеЁёЖжЗзИиЙйКкЛлМмНнОоПпРрСсТтУуФфХхЦцЧчШшЩщЪъЫыЬьЭэЮюЯяәөүғңһҹієїўґ"
    russian = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    digits = "0123456789"
    symbols = " !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"

    all_chars = set()
    all_chars.update(azeri_latin)
    all_chars.update(azeri_cyrillic)
    all_chars.update(russian)
    all_chars.update(digits)
    all_chars.update(symbols)

    # Сортируем символы
    sorted_chars = sorted(all_chars)

    with open(chars_file, 'w', encoding='utf-8') as f:
        f.write("blank\n")
        for char in sorted_chars:
            f.write(f"{char}\n")

    print(f"Created character dictionary with {len(sorted_chars)} characters in {chars_file}")
    return chars_file


def main():
    """Main function to prepare all data"""
    print("Starting PaddleOCR data preparation...")

    # Создаем директории если нужно
    os.makedirs("newData", exist_ok=True)

    # Конвертируем данные
    rec_file = convert_rec_gt()
    det_file = convert_lastlabel()

    # Объединяем данные
    final_file = merge_data(rec_file, det_file)

    # Создаем словарь символов
    chars_file = create_character_dict()

    print("\n" + "=" * 50)
    print("DATA PREPARATION COMPLETED!")
    print("=" * 50)
    print(f"Final training file: {final_file}")
    print(f"Character dictionary: {chars_file}")
    print("\nNext steps:")
    print("1. Download pretrained model:")
    print("   wget https://paddleocr.bj.bcebos.com/PP-OCRv3/russian/ch_PP-OCRv3_rec_train.tar")
    print("   tar xf ch_PP-OCRv3_rec_train.tar")
    print("2. Run training:")
    print("   python3 tools/train.py -c config.yml -o Global.pretrained_model=./ch_PP-OCRv3_rec_train/best_accuracy")


if __name__ == "__main__":
    main()