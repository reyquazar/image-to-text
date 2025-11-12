import os
import cv2
import albumentations as A

# Пути
base_dir = "C:/Users/elsha/Downloads/image-to-text/text/typed_text/fortrain"
train_list_path = os.path.join(base_dir, "train_list.txt")
val_list_path = os.path.join(base_dir, "val_list.txt")

# Создаем папки для аугментированных данных
augmented_dir = os.path.join(base_dir, "augmented_data")
augmented_train_dir = os.path.join(augmented_dir, "train")
augmented_val_dir = os.path.join(augmented_dir, "val")
os.makedirs(augmented_train_dir, exist_ok=True)
os.makedirs(augmented_val_dir, exist_ok=True)

# Читаем списки файлов с сохранением разметки
with open(train_list_path, 'r', encoding='utf-8') as f:
    train_lines = [line.strip() for line in f.readlines() if line.strip()]

with open(val_list_path, 'r', encoding='utf-8') as f:
    val_lines = [line.strip() for line in f.readlines() if line.strip()]

# Разделяем на имена файлов и разметку
train_data = []
for line in train_lines:
    parts = line.split('\t')
    if len(parts) >= 2:
        filename = parts[0]
        annotation = parts[1]  # сохраняем всю остальную часть как разметку
        train_data.append((filename, annotation))

val_data = []
for line in val_lines:
    parts = line.split('\t')
    if len(parts) >= 2:
        filename = parts[0]
        annotation = parts[1]  # сохраняем всю остальную часть как разметку
        val_data.append((filename, annotation))

print(f"Найдено {len(train_data)} train записей с разметкой")
print(f"Найдено {len(val_data)} val записей с разметкой")

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

# Создаем новые списки файлов С РАЗМЕТКОЙ
new_train_lines = []
new_val_lines = []

# Копируем валидационные данные БЕЗ изменений (с разметкой)
for filename, annotation in val_data:
    src_path = os.path.join(base_dir, filename)
    dst_path = os.path.join(augmented_val_dir, filename)

    image = cv2.imread(src_path)
    if image is not None:
        cv2.imwrite(dst_path, image)
        # Сохраняем путь и разметку
        new_val_lines.append(f"{filename}\t{annotation}")
    else:
        print(f"Пропущен валидационный файл: {filename}")

# Аугментируем тренировочные данные (с разметкой)
for filename, annotation in train_data:
    src_path = os.path.join(base_dir, filename)

    # Загружаем изображение
    image = cv2.imread(src_path)
    if image is None:
        print(f"Пропущен тренировочный файл: {filename}")
        continue

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Сохраняем оригинал в аугментированную папку
    original_dst = os.path.join(augmented_train_dir, filename)
    cv2.imwrite(original_dst, image)
    # Сохраняем оригинал с разметкой
    new_train_lines.append(f"{filename}\t{annotation}")

    # Создаем аугментированные версии
    for i in range(AUGMENTATION_FACTOR):
        augmented = transform(image=image_rgb)
        augmented_image = augmented['image']

        # Создаем имя для аугментированного файла
        name, ext = os.path.splitext(filename)
        aug_filename = f"{name}_aug{i}{ext}"
        aug_dst_path = os.path.join(augmented_train_dir, aug_filename)

        # Сохраняем аугментированное изображение
        cv2.imwrite(aug_dst_path, cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR))
        # Сохраняем аугментированный файл с ТОЙ ЖЕ РАЗМЕТКОЙ
        new_train_lines.append(f"{aug_filename}\t{annotation}")

# Сохраняем новые списки файлов С РАЗМЕТКОЙ
new_train_list_path = os.path.join(augmented_dir, "train_list.txt")
new_val_list_path = os.path.join(augmented_dir, "val_list.txt")

with open(new_train_list_path, 'w', encoding='utf-8') as f:
    for line in new_train_lines:
        f.write(line + '\n')

with open(new_val_list_path, 'w', encoding='utf-8') as f:
    for line in new_val_lines:
        f.write(line + '\n')

print("Аугментация завершена!")
print(f"Исходный train: {len(train_data)} файлов")
print(f"Новый train: {len(new_train_lines)} файлов")
print(f"Val: {len(new_val_lines)} файлов")
print(f"Аугментированные данные сохранены в: {augmented_dir}")