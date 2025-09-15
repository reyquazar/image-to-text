import albumentations as A
import cv2
import os
from pathlib import Path


def augment_text_images(input_dir, output_dir, augmentations_per_image=5):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Определяем аугментации специфичные для текста
    transform = A.Compose([
        A.OneOf([
            A.GaussianBlur(blur_limit=(1, 3), p=0.5),
            A.MotionBlur(blur_limit=(3, 5), p=0.3),
            A.MedianBlur(blur_limit=3, p=0.2),
        ], p=0.5),
        A.GaussNoise(p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.2, contrast_limit=0.2, p=0.5),
        A.Perspective(scale=(0.05, 0.1), p=0.3),
        A.Affine(shear=(-5, 5), p=0.3),
        A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=0.3),
        A.RandomGamma(gamma_limit=(80, 120), p=0.3),
    ])

    image_files = list(input_path.glob('*.jpg')) + list(input_path.glob('*.png')) + list(input_path.glob('*.jpeg'))

    for img_path in image_files:
        image = cv2.imread(str(img_path))
        if image is None:
            continue

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        for i in range(augmentations_per_image):
            augmented = transform(image=image)
            augmented_image = augmented['image']

            output_filename = f"{img_path.stem}_aug_{i}{img_path.suffix}"
            output_filepath = output_path / output_filename

            augmented_image_bgr = cv2.cvtColor(augmented_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(output_filepath), augmented_image_bgr)

    print(f"Аугментация завершена. Создано {len(image_files) * augmentations_per_image} изображений")


# Использование
augment_text_images(
    input_dir='crop_img',
    output_dir='output_img',
    augmentations_per_image=5
)