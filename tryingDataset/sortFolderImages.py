import os
import re


def rename_images_sequentially(folder_path):
    png_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

    def extract_number(filename):
        match = re.search(r'word_(\d+)\.png', filename)
        return int(match.group(1)) if match else 0

    png_files.sort(key=extract_number)

    for i, filename in enumerate(png_files, 1):
        old_path = os.path.join(folder_path, filename)
        new_filename = f"word_{i}.png"
        new_path = os.path.join(folder_path, new_filename)

        if old_path != new_path and not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"Переименован: {filename} -> {new_filename}")


rename_images_sequentially('dataset')
