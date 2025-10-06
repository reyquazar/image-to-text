import os


def check_training_logs():
    print("=== АНАЛИЗ ЛОГОВ ОБУЧЕНИЯ ===")

    log_content = []
    log_content.append("=== АНАЛИЗ ПРОБЛЕМЫ ОБУЧЕНИЯ ===")
    log_content.append("Архитектура совместима, но ACC = 0.015")
    log_content.append("Возможные причины:")
    log_content.append("")

    # Проверка размера словаря
    dict_path = "./text/typed_text/azerbaijani_cyrillic_dataset/dict.txt"
    if os.path.exists(dict_path):
        with open(dict_path, 'r', encoding='utf-8') as f:
            dict_chars = [line.strip() for line in f]
        log_content.append(f"📊 Размер словаря: {len(dict_chars)} символов")

        # Сравнение с pretrained моделью
        pretrained_classes = 120  # из диагностики
        log_content.append(f"📊 Классов в pretrained модели: {pretrained_classes}")
        log_content.append(f"📊 Классов в вашем словаре: {len(dict_chars)}")

        if len(dict_chars) != pretrained_classes:
            log_content.append("❌ НЕСОВПАДЕНИЕ: Размер словаря не совпадает с pretrained моделью!")
            log_content.append("💡 Нужно изменить head для соответствия вашему словарю")
        else:
            log_content.append("✅ Размер словаря совпадает")

    # Проверка данных обучения
    train_list_path = "./text/typed_text/azerbaijani_cyrillic_dataset/train_list.txt"
    if os.path.exists(train_list_path):
        with open(train_list_path, 'r', encoding='utf-8') as f:
            train_lines = f.readlines()

        log_content.append("")
        log_content.append("=== АНАЛИЗ ДАННЫХ ===")
        log_content.append(f"📊 Примеров в train: {len(train_lines)}")

        # Анализ первых примеров
        log_content.append("Первые 3 примера:")
        for i, line in enumerate(train_lines[:3]):
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                img_path = parts[0]
                label = parts[1]
                full_img_path = f"./text/typed_text/azerbaijani_cyrillic_dataset/{img_path}"
                exists = os.path.exists(full_img_path)
                log_content.append(f"  {i + 1}. {img_path} -> '{label}' | Файл: {'✅' if exists else '❌'}")

    # Рекомендации
    log_content.append("")
    log_content.append("=== РЕКОМЕНДАЦИИ ===")
    log_content.append("1. ПРОВЕРЬТЕ РАЗМЕР СЛОВАРЯ - должен быть 120 символов")
    log_content.append("2. УБЕДИТЕСЬ ЧТО HEAD ПЕРЕОПРЕДЕЛЯЕТСЯ для вашего словаря")
    log_content.append("3. ПРОВЕРЬТЕ ЧТО ВЕСА HEAD НЕ ЗАМОРОЖЕНЫ")
    log_content.append("4. УМЕНЬШИТЕ LEARNING RATE до 0.0001")
    log_content.append("5. ПРОВЕРЬТЕ ЛОГИ ОБУЧЕНИЯ - есть ли ошибки при загрузке весов")

    # Сохраняем в файл
    with open("training_analysis_log.txt", 'w', encoding='utf-8') as f:
        for line in log_content:
            f.write(line + '\n')

    print("✅ Анализ сохранен в training_analysis_log.txt")


check_training_logs()