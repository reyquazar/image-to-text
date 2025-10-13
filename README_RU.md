# Отчет по выполнению задачи по созданию OCR расширения для браузера

## Выполненные работы:

### 1. Настройка окружения и выбор технологии
- Выбран PaddleOCR как более мощная альтернатива TesseractOCR
- Создан репозиторий: ```git clone https://github.com/reyquazar/image-to-text.git``` (ветка develop)
- Установка зависимостей:
```
python -m pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
python -m pip install "paddleocr[all]"
python -m pip install albumentations  RapidFuzz lmdb scikit-image PyYAML
```

### 2. Разметка данных
- Запущена разметка данных через Python скрипт: ```python .\PPOCRLabel.py --lang en```
- Размечено 8 изображений для обучения модели
- Размеченные изображения сохранены в ```./text/typed_text/crop_image```
- Файл разметки: ```rec_gt.txt```

### 3. Подготовка к обучению модели
- Изучена документация PaddleOCR по fine-tuning
- Создан рабочий конфигурационный файл: ```./text/typed_text/az_rec_config.yaml```
- Подготовлен словарь для аугментации: ```./text/typed_text/az_config_train/dict.txt```
- Скачаны дополнительные шрифты для обучения

### 4. Генерация синтетических данных
- Создана программа ```genDataTrainVal.py``` для генерации синтетических данных
- Реализована поддержка параметра количества данных (пример: ```python .\genDataTrainVal.py 25000```)
- Создана альтернативная программа ```TrainVal.py``` для использования оригинальных данных из ```crop_img```
- Сгенерированы файлы ```train_list.txt``` и ```val_list.txt```

### 5. Обучение модели
- Скачан репозиторий PaddleOCR: ```git clone https://github.com/PaddlePaddle/PaddleOCR.git```
- Загружена предобученная модель: ```wget https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-OCRv5_server_rec_pretrained -P ./text/typed_text/pretrain_models```
- Запущен процесс обучения: ```python ../PaddleOCR/tools/train.py -c ./text/typed_text/az_rec_config.yaml```
- Достигнута точность (accuracy) выше 90%

### 6. Экспорт модели
- Создана inference модель: ```python ../PaddleOCR/tools/export_model.py -c ./text/typed_text/az_rec_config.yaml -o Global.pretrained_model=output/best_accuracy.pdparams Global.save_inference_dir=output```
- Выполнена модификация конфигурационного файла: удалить параметр ```- CTCLABELENCODE: null```
```
vim output/inference.yml
```

### 7. Тестирование модели
- Реализован скрипт тестирования: ```python .\testFast.py .\text\typed_text\text20.png```
- Сравнение результатов между оригинальной и дообученной моделью

### 8. Разработка расширения для браузера
- Создана серверная архитектура для интеграции PaddleOCR в браузерное расширение
- Реализован функционал в папке ```./image-to-text/ExtensionServerPaddleOCR```
- Проведена работа с JavaScript для создания интерфейса
- Основной функционал расширения работает