import os
import shutil

for i in range(400):
    if os.path.isfile(f'words_output/word_{i}.png'):
        print(f'word{i}')

        newDir = str(input())
        os.makedirs(f"words/{newDir}", exist_ok=True)

        source_file = f'words_output/word_{i}.png'
        destination_file = f"words/{newDir}/word_{i}.png"
        shutil.copy2(source_file, destination_file)
