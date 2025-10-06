import paddle
import os


def debug_architecture_compatibility():
    print("=== РЕАЛЬНАЯ ДИАГНОСТИКА СОВМЕСТИМОСТИ ===")

    # 1. Загружаем pretrained веса
    weights_path = "./text/typed_text/pretrain_models/PP-OCRv5_server_rec_pretrained.pdparams"
    weights = paddle.load(weights_path)

    # 2. Анализируем структуру pretrained весов
    print("Ключи в pretrained весах:")
    backbone_keys = [k for k in weights.keys() if 'backbone' in k]
    neck_keys = [k for k in weights.keys() if 'neck' in k]
    head_keys = [k for k in weights.keys() if 'head' in k]

    print(f"Backbone ключи ({len(backbone_keys)}): {backbone_keys[:5]}...")
    print(f"Neck ключи ({len(neck_keys)}): {neck_keys[:5]}...")
    print(f"Head ключи ({len(head_keys)}): {head_keys[:5]}...")

    # 3. Определяем какая архитектура используется в pretrained модели
    if any('svtr' in k.lower() for k in weights.keys()):
        print("✅ Pretrained модель использует SVTR архитектуру")
        recommended_backbone = "PPLCNetV3"
    elif any('resnet' in k.lower() for k in weights.keys()):
        print("✅ Pretrained модель использует ResNet архитектуру")
        recommended_backbone = "ResNet"
    elif any('mobilenet' in k.lower() for k in weights.keys()):
        print("✅ Pretrained модель использует MobileNet архитектуру")
        recommended_backbone = "MobileNetV3"
    else:
        print("❓ Не удалось определить архитектуру pretrained модели")
        # Анализируем по шаблонам ключей
        if any('conv' in k and 'weight' in k for k in backbone_keys):
            print("📊 Похоже на CNN-based архитектуру")
        recommended_backbone = "ResNet"  # fallback

    # 4. Проверяем совместимость с текущей конфигурацией
    current_backbone = "PPLCNetV3"
    current_neck = "SVTR"

    print(f"\nТекущая конфигурация: {current_backbone} + {current_neck}")
    print(f"Рекомендуемая конфигурация: {recommended_backbone} + соответствующий neck")

    # 5. Проверяем размеры выходных слоев
    print(f"\nРазмеры весов в head:")
    head_weight_shapes = {k: weights[k].shape for k in head_keys if 'weight' in k}
    for k, shape in list(head_weight_shapes.items())[:3]:
        print(f"  {k}: {shape}")


debug_architecture_compatibility()