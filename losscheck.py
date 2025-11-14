import re
import numpy as np
from pathlib import Path


def analyze_train_log(log_file_path):
    """
    Анализирует train.log и выдает сводку по loss
    """
    # Регулярные выражения для извлечения loss
    loss_pattern = r"loss: ([\d]+\.[\d]+)"
    epoch_loss_pattern = r"epoch:.*?loss: ([\d]+\.[\d]+)"
    batch_pattern = r"batch:.*?loss: ([\d]+\.[\d]+)"

    losses = []
    epoch_losses = []
    batch_losses = []

    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Извлекаем все loss значения
        losses = [float(x) for x in re.findall(loss_pattern, content)]

        # Извлекаем epoch losses
        epoch_losses = [float(x) for x in re.findall(epoch_loss_pattern, content)]

        # Извлекаем batch losses (последние 50 для анализа колебаний)
        batch_losses = [float(x) for x in re.findall(batch_pattern, content)][-50:]

    except Exception as e:
        print(f"❌ Ошибка чтения файла: {e}")
        return

    if not losses:
        print("❌ Не найдены значения loss в логе")
        return

    print("📊 СВОДКА ПО TRAIN.LOG")
    print("=" * 50)

    # Общая статистика
    print(f"📈 Всего значений loss: {len(losses)}")
    print(f"📅 Epoch losses: {len(epoch_losses)}")
    print(f"🔢 Batch losses (последние 50): {len(batch_losses)}")
    print()

    # Статистика по всем loss
    if losses:
        print("📋 ОБЩАЯ СТАТИСТИКА:")
        print(f"   Минимальный loss: {min(losses):.4f}")
        print(f"   Максимальный loss: {max(losses):.4f}")
        print(f"   Средний loss: {np.mean(losses):.4f}")
        print(f"   Медианный loss: {np.median(losses):.4f}")
        print()

    # Анализ тренда
    if len(losses) >= 10:
        first_10 = losses[:10]
        last_10 = losses[-10:]
        trend = np.mean(last_10) - np.mean(first_10)

        print("📉 ТРЕНД:")
        print(f"   Первые 10 loss: {np.mean(first_10):.4f}")
        print(f"   Последние 10 loss: {np.mean(last_10):.4f}")
        print(f"   Изменение: {trend:+.4f}")

        if trend < -0.1:
            print("   ✅ Тренд: УЛУЧШЕНИЕ (loss уменьшается)")
        elif trend > 0.1:
            print("   ❌ Тренд: УХУДШЕНИЕ (loss растет)")
        else:
            print("   ⚠️  Тренд: СТАГНАЦИЯ (loss не меняется)")
        print()

    # Анализ колебаний batch loss
    if batch_losses:
        print("🎯 АНАЛИЗ КОЛЕБАНИЙ (последние 50 батчей):")
        loss_range = max(batch_losses) - min(batch_losses)
        std_dev = np.std(batch_losses)

        print(f"   Разброс (max-min): {loss_range:.4f}")
        print(f"   Стандартное отклонение: {std_dev:.4f}")

        if loss_range > 2.0:
            print("   ❌ СИЛЬНЫЕ КОЛЕБАНИЯ - УМЕНЬШИТЬ Learning Rate!")
        elif loss_range > 1.0:
            print("   ⚠️  УМЕРЕННЫЕ КОЛЕБАНИЯ - наблюдать")
        else:
            print("   ✅ СТАБИЛЬНО - хороший Learning Rate")
        print()

    # Анализ по эпохам
    if epoch_losses:
        print("🔄 ПОСЛЕДНИЕ EPOCH LOSSES:")
        for i, loss in enumerate(epoch_losses[-5:], 1):
            epoch_num = len(epoch_losses) - 5 + i
            print(f"   Epoch {epoch_num}: {loss:.4f}")

        if len(epoch_losses) >= 2:
            last_improvement = epoch_losses[-2] - epoch_losses[-1]
            if last_improvement > 0:
                print(f"   📈 Последнее улучшение: -{last_improvement:.4f}")
            else:
                print(f"   📉 Последнее ухудшение: +{abs(last_improvement):.4f}")
        print()

    # Рекомендации
    print("💡 РЕКОМЕНДАЦИИ:")

    if batch_losses and (max(batch_losses) - min(batch_losses)) > 2.0:
        print("   🔽 УМЕНЬШИТЬ Learning Rate в 3-5 раз")
    elif losses and len(losses) > 20 and abs(np.mean(losses[-10:]) - np.mean(losses[-20:-10])) < 0.05:
        print("   🔼 УВЕЛИЧИТЬ Learning Rate в 2-3 раза")
    elif losses and losses[-1] < 0.5:
        print("   ✅ Loss хороший - продолжать обучение")
    else:
        print("   ⏳ Продолжать наблюдение")

    print("=" * 50)


# Использование
if __name__ == "__main__":
    log_file = "./text/train9.log"  # Укажите путь к вашему train.log
    analyze_train_log(log_file)