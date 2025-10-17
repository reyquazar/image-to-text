import paddle
import yaml
import os
from collections import defaultdict


def comprehensive_model_analysis(model_path):
    """
    Комплексный анализ модели PP-OCRv5
    """
    print("🔍 Начинаем анализ модели PP-OCRv5...")
    print("🔍 Начинаем анализ модели PP-OCRv5...")

    # Проверка существования файла
    if not os.path.exists(model_path):
        print(f"❌ Файл {model_path} не найден!")
        return

    # Загрузка state_dict
    try:
        state_dict = paddle.load(model_path)
        print(f"✅ Модель успешно загружена")
    except Exception as e:
        print(f"❌ Ошибка загрузки модели: {e}")
        return

    # Основная информация
    print(f"\n📊 Основная информация:")
    print(f"   Всего тензоров: {len(state_dict)}")

    # Анализ параметров
    total_params = 0
    param_stats = defaultdict(int)

    for key, tensor in state_dict.items():
        # ИСПРАВЛЕНИЕ: используем свойство size, а не метод
        num_params = tensor.size
        total_params += num_params
        param_stats[key.split('.')[-1]] += num_params

    print(f"   Общее количество параметров: {total_params:,}")

    # Анализ структуры
    print(f"\n🏗️  Структура модели:")
    layers = defaultdict(list)

    for key, tensor in state_dict.items():
        parts = key.split('.')
        if len(parts) > 1:
            layer_name = parts[-2]
            param_type = parts[-1]
            layers[layer_name].append((param_type, tensor.shape))

    # Выводим только первые 20 слоев для краткости
    for i, (layer_name, params) in enumerate(layers.items()):
        if i >= 20:  # Ограничиваем вывод
            remaining = len(layers) - 20
            print(f"\n   ... и еще {remaining} слоев")
            break
        print(f"\n   📍 {layer_name}:")
        for param_type, shape in params[:5]:  # Ограничиваем параметры на слой
            print(f"      {param_type}: {shape}")
        if len(params) > 5:
            print(f"      ... и еще {len(params) - 5} параметров")

    # Поиск конфигурации
    print(f"\n⚙️  Поиск конфигурации...")
    model_dir = os.path.dirname(model_path) if os.path.dirname(model_path) else '.'

    # Ищем конфигурационные файлы
    config_files = []
    for f in os.listdir(model_dir):
        if f.endswith('.yml') or f.endswith('.yaml'):
            config_files.append(f)

    if config_files:
        for config_file in config_files:
            config_path = os.path.join(model_dir, config_file)
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                print(f"✅ Найдена конфигурация: {config_file}")

                # Вывод важных параметров архитектуры
                if 'Architecture' in config:
                    print(f"\n📐 Архитектура:")
                    arch = config['Architecture']
                    for key, value in arch.items():
                        if isinstance(value, dict) and 'name' in value:
                            print(f"   {key}: {value['name']}")
                        else:
                            print(f"   {key}: {value}")

            except Exception as e:
                print(f"❌ Ошибка чтения конфигурации {config_file}: {e}")
    else:
        print("❌ Конфигурационные файлы не найдены")
        print("Попробуем определить архитектуру по именам параметров...")
        analyze_architecture_from_params(state_dict)


def analyze_architecture_from_params(state_dict):
    """
    Анализ архитектуры на основе имен параметров
    """
    print(f"\n🔍 Анализ архитектуры по именам параметров:")

    # Собираем статистику по типам слоев
    layer_types = defaultdict(int)

    for key in state_dict.keys():
        parts = key.split('.')
        if len(parts) > 1:
            layer_name = parts[-2]
            # Определяем тип слоя по имени
            if 'conv' in layer_name:
                layer_types['conv'] += 1
            elif 'bn' in layer_name or 'batch_norm' in layer_name:
                layer_types['batch_norm'] += 1
            elif 'fc' in layer_name or 'linear' in layer_name:
                layer_types['linear'] += 1
            elif 'lstm' in layer_name:
                layer_types['lstm'] += 1
            elif 'attention' in layer_name:
                layer_types['attention'] += 1
            else:
                layer_types['other'] += 1

    print("📈 Статистика по типам слоев:")
    for layer_type, count in layer_types.items():
        print(f"   {layer_type}: {count}")

    # Анализируем размеры выходных признаков
    print(f"\n📏 Анализ размерностей:")
    feature_sizes = set()
    for key, tensor in state_dict.items():
        if 'weight' in key and len(tensor.shape) == 4:  # Conv weights
            in_ch, out_ch, h, w = tensor.shape
            feature_sizes.add((in_ch, out_ch))

    if feature_sizes:
        print("   Размеры сверточных слоев (in_ch, out_ch):")
        for size in sorted(feature_sizes)[:10]:  # Показываем первые 10
            print(f"      {size}")


# Дополнительная функция для детального анализа конкретных слоев
def detailed_layer_analysis(model_path):
    """
    Детальный анализ конкретных слоев модели
    """
    state_dict = paddle.load(model_path)

    print(f"\n🎯 Детальный анализ ключевых слоев:")

    # Ищем backbone слои
    backbone_layers = []
    for key in state_dict.keys():
        if 'backbone' in key.lower() or 'conv' in key:
            backbone_layers.append(key)

    print(f"   Слои backbone (первые 10):")
    for layer in backbone_layers[:10]:
        tensor = state_dict[layer]
        print(f"      {layer}: shape={tensor.shape}, params={tensor.size:,}")

    # Ищем LSTM/RNN слои
    rnn_layers = []
    for key in state_dict.keys():
        if 'lstm' in key.lower() or 'rnn' in key.lower():
            rnn_layers.append(key)

    if rnn_layers:
        print(f"\n   RNN/LSTM слои:")
        for layer in rnn_layers:
            tensor = state_dict[layer]
            print(f"      {layer}: shape={tensor.shape}, params={tensor.size:,}")


# Запуск комплексного анализа
if __name__ == "__main__":
    model_path = './PP-OCRv5_server_rec_pretrained.pdparams'
    comprehensive_model_analysis(model_path)

    # Дополнительный детальный анализ
    detailed_layer_analysis(model_path)

    # Дополнительная информация о модели
    print(f"\n💡 Дополнительная информация:")
    print(f"   Размер файла модели: {os.path.getsize(model_path) / (1024 * 1024):.2f} MB")