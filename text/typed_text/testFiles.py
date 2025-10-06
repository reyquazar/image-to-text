import paddle
import os
from datetime import datetime


def debug_architecture_compatibility():
    print("=== РЕАЛЬНАЯ ДИАГНОСТИКА СОВМЕСТИМОСТИ ===")

    log_content = []
    log_content.append("=== ДИАГНОСТИКА СОВМЕСТИМОСТИ АРХИТЕКТУРЫ ===")
    log_content.append(f"Время проверки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    log_content.append("")

    try:
        # 1. Загружаем pretrained веса
        weights_path = "./text/typed_text/pretrain_models/PP-OCRv5_server_rec_pretrained.pdparams"
        log_content.append(f"Путь к pretrained модели: {weights_path}")

        if not os.path.exists(weights_path):
            log_content.append("❌ Файл pretrained модели не существует!")
            write_log_to_file(log_content)
            return

        weights = paddle.load(weights_path)
        log_content.append(f"✅ Pretrained модель успешно загружена")
        log_content.append(f"📊 Всего ключей в весах: {len(weights.keys())}")
        log_content.append("")

        # 2. Анализируем структуру pretrained весов
        log_content.append("=== АНАЛИЗ СТРУКТУРЫ PRETRAINED ВЕСОВ ===")

        backbone_keys = [k for k in weights.keys() if 'backbone' in k]
        neck_keys = [k for k in weights.keys() if 'neck' in k]
        head_keys = [k for k in weights.keys() if 'head' in k]

        log_content.append(f"Backbone ключи ({len(backbone_keys)}):")
        for key in backbone_keys[:10]:
            shape = str(weights[key].shape) if hasattr(weights[key], 'shape') else 'N/A'
            log_content.append(f"  - {key} : {shape}")
        if len(backbone_keys) > 10:
            log_content.append(f"  ... и еще {len(backbone_keys) - 10} ключей")
        log_content.append("")

        log_content.append(f"Neck ключи ({len(neck_keys)}):")
        for key in neck_keys[:10]:
            shape = str(weights[key].shape) if hasattr(weights[key], 'shape') else 'N/A'
            log_content.append(f"  - {key} : {shape}")
        if len(neck_keys) > 10:
            log_content.append(f"  ... и еще {len(neck_keys) - 10} ключей")
        log_content.append("")

        log_content.append(f"Head ключи ({len(head_keys)}):")
        for key in head_keys[:10]:
            shape = str(weights[key].shape) if hasattr(weights[key], 'shape') else 'N/A'
            log_content.append(f"  - {key} : {shape}")
        if len(head_keys) > 10:
            log_content.append(f"  ... и еще {len(head_keys) - 10} ключей")
        log_content.append("")

        # 3. Определяем какая архитектура используется в pretrained модели
        log_content.append("=== ОПРЕДЕЛЕНИЕ АРХИТЕКТУРЫ PRETRAINED МОДЕЛИ ===")

        all_keys = ' '.join(weights.keys()).lower()

        if any('svtr' in k.lower() for k in weights.keys()):
            log_content.append("✅ Pretrained модель использует SVTR архитектуру")
            recommended_backbone = "PPLCNetV3"
            recommended_neck = "SVTR"
        elif any('resnet' in k.lower() for k in weights.keys()):
            log_content.append("✅ Pretrained модель использует ResNet архитектуру")
            recommended_backbone = "ResNet"
            recommended_neck = "SequenceEncoder(rnn)"
        elif any('mobilenet' in k.lower() for k in weights.keys()):
            log_content.append("✅ Pretrained модель использует MobileNet архитектуру")
            recommended_backbone = "MobileNetV3"
            recommended_neck = "SequenceEncoder(rnn)"
        elif any('pplcnet' in k.lower() for k in weights.keys()):
            log_content.append("✅ Pretrained модель использует PPLCNet архитектуру")
            recommended_backbone = "PPLCNetV3"
            recommended_neck = "SequenceEncoder(svtr)"
        else:
            log_content.append("❓ Не удалось определить архитектуру по ключам")
            # Анализируем по шаблонам
            if any('conv' in k and 'weight' in k for k in backbone_keys):
                log_content.append("📊 Похоже на CNN-based архитектуру (ResNet/MobileNet)")
                recommended_backbone = "ResNet"
                recommended_neck = "SequenceEncoder(rnn)"
            else:
                log_content.append("❌ Нестандартная архитектура")
                recommended_backbone = "ResNet"
                recommended_neck = "SequenceEncoder(rnn)"

        # 4. Проверяем совместимость с текущей конфигурацией
        log_content.append("")
        log_content.append("=== РЕКОМЕНДАЦИИ ПО КОНФИГУРАЦИИ ===")
        current_backbone = "PPLCNetV3"
        current_neck = "SVTR"

        log_content.append(f"Текущая конфигурация: Backbone={current_backbone}, Neck={current_neck}")
        log_content.append(f"Рекомендуемая конфигурация: Backbone={recommended_backbone}, Neck={recommended_neck}")

        if current_backbone == recommended_backbone and current_neck == recommended_neck:
            log_content.append("✅ Текущая конфигурация СОВМЕСТИМА с pretrained моделью")
        else:
            log_content.append("❌ Текущая конфигурация НЕ СОВМЕСТИМА с pretrained моделью")
            log_content.append("💡 Рекомендуется изменить конфиг на рекомендуемую архитектуру")

        # 5. Дополнительная информация о размерах
        log_content.append("")
        log_content.append("=== ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ ===")

        # Размеры выходных слоев
        fc_weights = [k for k in head_keys if 'fc' in k and 'weight' in k]
        if fc_weights:
            for key in fc_weights[:3]:
                shape = weights[key].shape
                log_content.append(f"FC слой {key}: размерность {shape}")
                log_content.append(f"  - Предполагаемое количество классов: {shape[0]}")

        # Проверка наличия batch norm слоев
        bn_layers = [k for k in weights.keys() if 'batch_norm' in k or 'bn' in k]
        log_content.append(f"BatchNorm слоев в модели: {len(bn_layers)}")

    except Exception as e:
        log_content.append(f"❌ Ошибка при анализе: {str(e)}")

    write_log_to_file(log_content)


def write_log_to_file(log_content):
    log_file = "architecture_compatibility_log.txt"
    with open(log_file, 'w', encoding='utf-8') as f:
        for line in log_content:
            f.write(line + '\n')
    print(f"✅ Лог сохранен в файл: {log_file}")


if __name__ == "__main__":
    debug_architecture_compatibility()