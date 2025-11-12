import os
import cv2
import albumentations as A

# Пути
base_dir = "C:/Users/elsha/Downloads/image-to-text/text/typed_text/az_config_train"
train_list_path = os.path.join(base_dir, "train_list.txt")
val_list_path = os.path.join(base_dir, "val_list.txt")

# Создаем папки для аугментированных данных
augmented_dir = os.path.join(base_dir, "augmented_data")
augmented_train_dir = os.path.join(augmented_dir, "train")
augmented_val_dir = os.path.join(augmented_dir, "val")
os.makedirs(augmented_train_dir, exist_ok=True)
os.makedirs(augmented_val_dir, exist_ok=True)

# Читаем списки файлов и очищаем от лишних символов
with open(train_list_path, 'r', encoding='utf-8') as f:
    train_files = [line.strip().split('\t')[0] for line in f.readlines() if line.strip()]

with open(val_list_path, 'r', encoding='utf-8') as f:
    val_files = [line.strip().split('\t')[0] for line in f.readlines() if line.strip()]

# Исправленные трансформации для аугментации
transform = A.Compose([
    A.Affine(scale=(0.9, 1.1), rotate=(-5, 5), translate_percent=(-0.03, 0.03), p=0.7),
    A.GaussNoise(var_limit=(10.0, 30.0), p=0.4),
    A.MotionBlur(blur_limit=3, p=0.3),
    A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.15, p=0.5),
    A.ElasticTransform(alpha=1, sigma=30, p=0.2),
])

# Количество аугментированных копий для каждого изображения
AUGMENTATION_FACTOR = 5

# Создаем новые списки файлов
new_train_list = []
new_val_list = []

# Копируем валидационные данные БЕЗ изменений
for val_file in val_files:
    src_path = os.path.join(base_dir, val_file)
    dst_path = os.path.join(augmented_val_dir, val_file)

    image = cv2.imread(src_path)
    if image is not None:
        cv2.imwrite(dst_path, image)
        new_val_list.append(val_file)
    else:
        print(f"Пропущен валидационный файл: {val_file}")

# Аугментируем тренировочные данные
for train_file in train_files:
    src_path = os.path.join(base_dir, train_file)

    # Загружаем изображение
    image = cv2.imread(src_path)
    if image is None:
        print(f"Пропущен тренировочный файл: {train_file}")
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Сохраняем оригинал в аугментированную папку
    original_dst = os.path.join(augmented_train_dir, train_file)
    cv2.imwrite(original_dst, image)
    new_train_list.append(train_file)

    # Создаем аугментированные версии
    for i in range(AUGMENTATION_FACTOR):
        augmented = transform(image=image_rgb)
        augmented_image = augmented['image']

        # Создаем имя для аугментированного файла
        name, ext = os.path.splitext(train_file)
        aug_filename = f"{name}_aug{i}{ext}"
        aug_dst_path = os.path.join(augmented_train_dir, aug_filename)

        # Сохраняем аугментированное изображение
        cv2.imwrite(aug_dst_path, cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
        new_train_list.append(aug_filename)

# Сохраняем новые списки файлов
new_train_list_path = os.path.join(augmented_dir, "train_list.txt")
new_val_list_path = os.path.join(augmented_dir, "val_list.txt")

with open(new_train_list_path, 'w', encoding='utf-8') as f:
    for filename in new_train_list:
        f.write(filename + '\n')

with open(new_val_list_path, 'w', encoding='utf-8') as f:
    for filename in new_val_list:
        f.write(filename + '\n')

print("Аугментация завершена!")
print(f"Исходный train: {len(train_files)} файлов")
print(f"Новый train: {len(new_train_list)} файлов")
print(f"Val: {len(new_val_list)} файлов")
print(f"Аугментированные данные сохранены в: {augmented_dir}")