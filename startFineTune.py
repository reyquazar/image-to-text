import os
import subprocess
import sys


def run_training():
    """
    Скрипт для запуска fine-tuning PaddleOCR
    """
    # Пути к файлам (ваши правильные пути)
    config_path = "./text/typed_text/az_ru_rec_config.yaml"

    # Базовая команда
    command = f"python ../PaddleOCR/tools/train.py -c {config_path}"

    print("🚀 Запуск fine-tuning PaddleOCR")
    print("=" * 50)
    print(f"Конфиг: {config_path}")
    print(f"Команда: {command}")
    print("=" * 50)

    # Проверка существования конфига
    if not os.path.exists(config_path):
        print(f"❌ ОШИБКА: Конфиг не найден: {config_path}")
        print("Проверьте путь к az_ru_rec_config.yaml")
        return False

    # Запуск обучения
    try:
        print("⏳ Запускаю обучение...")
        print("ℹ️  Логи будут выводиться ниже:")
        print("-" * 50)

        # Запускаем процесс с выводом в реальном времени
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )

        # Выводим логи в реальном времени
        for line in process.stdout:
            print(line, end='')

        # Ждем завершения
        process.wait()

        if process.returncode == 0:
            print("✅ Обучение успешно завершено!")
            return True
        else:
            print(f"❌ Ошибка при обучении (код: {process.returncode})")
            return False

    except Exception as e:
        print(f"❌ Ошибка при запуске: {e}")
        return False


def check_environment():
    """
    Проверка окружения
    """
    print("🔍 Проверка окружения...")

    # Проверяем основные файлы (ВАШИ ПРАВИЛЬНЫЕ ПУТИ)
    required_files = [
        "./text/typed_text/az_ru_rec_config.yaml",
        "./text/typed_text/python/train_list.txt",
        "./text/typed_text/python/val_list.txt",
        "./text/typed_text/python/dict.txt"
    ]

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - НЕ НАЙДЕН!")

    print("-" * 50)


if __name__ == "__main__":
    print("PaddleOCR Fine-tuning Script")
    print("Сначала проверим окружение...")

    # Проверка окружения
    check_environment()

    # Спросим пользователя
    response = input("Запустить обучение? (y/n): ")
    if response.lower() in ['y', 'yes', 'д', 'да']:
        success = run_training()
        if success:
            print("🎉 Обучение завершено успешно!")
        else:
            print("💥 Обучение завершилось с ошибками")
    else:
        print("Обучение отменено")