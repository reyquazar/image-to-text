import lmdb
import pickle
import cv2
import numpy as np
import os


def verify_lmdb_dataset(lmdb_path):
    """Проверяет целостность LMDB датасета"""
    print(f"🔍 Проверка LMDB датасета: {lmdb_path}")

    if not os.path.exists(lmdb_path):
        print(f"❌ LMDB датасет не найден: {lmdb_path}")
        return False

    try:
        env = lmdb.open(lmdb_path, readonly=True, lock=False)
    except Exception as e:
        print(f"❌ Ошибка открытия LMDB: {e}")
        return False

    stats = {
        'total_samples': 0,
        'corrupted_images': 0,
        'empty_labels': 0,
    }

    # Проверяем все записи
    with env.begin() as txn:
        cursor = txn.cursor()

        for key, value in cursor:
            stats['total_samples'] += 1

            try:
                # Декодируем данные
                data = pickle.loads(value)
                image_data = data['image']
                label = data['label']

                # Проверяем метку
                if not label or len(label.strip()) == 0:
                    stats['empty_labels'] += 1
                    print(f"⚠️ Пустая метка у ключа: {key.decode()}")
                    continue

                # Проверяем изображение
                try:
                    nparr = np.frombuffer(image_data, np.uint8)
                    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if img is None:
                        stats['corrupted_images'] += 1
                        print(f"⚠️ Поврежденное изображение у ключа: {key.decode()}")
                        continue

                    if img.shape[0] == 0 or img.shape[1] == 0:
                        stats['corrupted_images'] += 1
                        print(f"⚠️ Нулевые размеры у ключа: {key.decode()}")
                        continue

                except Exception as img_e:
                    stats['corrupted_images'] += 1
                    print(f"⚠️ Ошибка декодирования изображения {key.decode()}: {img_e}")
                    continue

            except Exception as e:
                print(f"❌ Ошибка обработки записи {key.decode()}: {e}")
                continue

    env.close()

    # Выводим статистику
    print(f"📊 Всего samples: {stats['total_samples']}")
    print(f"📊 Поврежденные изображения: {stats['corrupted_images']}")
    print(f"📊 Пустые метки: {stats['empty_labels']}")

    # Валидируем результат
    is_valid = (stats['total_samples'] > 0 and
                stats['corrupted_images'] == 0 and
                stats['empty_labels'] == 0)

    if is_valid:
        print(f"✅ LMDB датасет валиден!")
    else:
        print(f"❌ LMDB датасет содержит ошибки!")

    # Показываем несколько примеров
    if stats['total_samples'] > 0:
        show_samples(lmdb_path, min(3, stats['total_samples']))

    print("")  # пустая строка для разделения
    return is_valid


def show_samples(lmdb_path, num_samples=3):
    """Показывает примеры из датасета"""
    print(f"🖼️  Показ {num_samples} примеров:")

    env = lmdb.open(lmdb_path, readonly=True, lock=False)

    with env.begin() as txn:
        cursor = txn.cursor()
        samples_shown = 0

        for key, value in cursor:
            if samples_shown >= num_samples:
                break

            try:
                data = pickle.loads(value)
                image_data = data['image']
                label = data['label']

                # Декодируем изображение
                nparr = np.frombuffer(image_data, np.uint8)
                img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if img is not None:
                    print(f"   {samples_shown + 1}. '{label}' | Размер: {img.shape[1]}x{img.shape[0]}")
                    samples_shown += 1

            except Exception as e:
                print(f"⚠️ Ошибка при показе примера: {e}")
                continue

    env.close()


def main():
    print("🧪 ПРОВЕРКА LMDB ДАТАСЕТОВ")
    print("=" * 40)

    base_dir = "./text/typed_text/az_config_train"

    # Проверяем train.lmdb
    train_lmdb_path = os.path.join(base_dir, "train.lmdb")
    lmdb_train_valid = verify_lmdb_dataset(train_lmdb_path)

    # Проверяем val.lmdb
    val_lmdb_path = os.path.join(base_dir, "val.lmdb")
    lmdb_val_valid = verify_lmdb_dataset(val_lmdb_path)

    print("=" * 40)
    print("🎯 ИТОГИ ПРОВЕРКИ:")
    print(f"   train.lmdb: {'✅ VALID' if lmdb_train_valid else '❌ INVALID'}")
    print(f"   val.lmdb: {'✅ VALID' if lmdb_val_valid else '❌ INVALID'}")

    if lmdb_train_valid and lmdb_val_valid:
        print("🎉 ВСЕ LMDB ДАТАСЕТЫ ВАЛИДНЫ!")
    else:
        print("⚠️ Некоторые LMDB датасеты содержат ошибки!")


if __name__ == "__main__":
    main()