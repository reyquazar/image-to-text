import paddle
import os


def check_pretrained_model():
    print("=== ПРОВЕРКА PRETRAINED МОДЕЛИ ===")

    model_path = "./text/typed_text/pretrain_models/PP-OCRv5_server_rec_pretrained.pdparams"

    # Проверка существования файла
    if not os.path.exists(model_path):
        print(f"❌ Файл не существует: {model_path}")
        return

    # Проверка размера файла
    file_size = os.path.getsize(model_path) / (1024 * 1024)  # в MB
    print(f"✅ Файл существует: {model_path}")
    print(f"📏 Размер файла: {file_size:.1f} MB")

    # Попытка загрузки весов
    try:
        weights = paddle.load(model_path)
        print(f"✅ Веса успешно загружены")
        print(f"📊 Ключи в весах: {len(weights.keys())}")
        print(f"📋 Пример ключей: {list(weights.keys())[:5]}")
    except Exception as e:
        print(f"❌ Ошибка загрузки весов: {e}")


check_pretrained_model()