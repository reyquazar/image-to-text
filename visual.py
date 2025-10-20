import re
import matplotlib

matplotlib.use('Agg')  # Используем бэкенд без отображения в реальном времени
import matplotlib.pyplot as plt


def simple_training_plot(filename):
    """Упрощенная версия для быстрого просмотра обучения"""

    steps = []
    losses = []
    train_accs = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # Ищем строки с тренировочными данными
            if 'global_step:' in line and 'loss:' in line:
                try:
                    # Извлекаем основные метрики
                    step_match = re.search(r'global_step: (\d+)', line)
                    loss_match = re.search(r'loss: ([\d.]+)', line)
                    acc_match = re.search(r'acc: ([\d.]+)', line)

                    if step_match and loss_match and acc_match:
                        steps.append(int(step_match.group(1)))
                        losses.append(float(loss_match.group(1)))
                        train_accs.append(float(acc_match.group(1)))
                except:
                    continue

    if not steps:
        print("Не найдено данных обучения в файле")
        return

    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(steps, losses, 'r-', linewidth=2)
    plt.xlabel('Global Step')
    plt.ylabel('Loss')
    plt.title('Loss во время обучения')
    plt.grid(True, alpha=0.3)

    plt.subplot(1, 2, 2)
    plt.plot(steps, train_accs, 'g-', linewidth=2)
    plt.xlabel('Global Step')
    plt.ylabel('Accuracy')
    plt.title('Training Accuracy')
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('training_plot.png')
    print("График сохранен как 'training_plot.png'")

    # Анализ тренда
    if len(losses) > 10:
        recent_loss = losses[-10:]
        loss_trend = "снижается" if recent_loss[-1] < recent_loss[0] else "стабилизируется/растет"
        print(f"Тренд loss (последние 10 шагов): {loss_trend}")


# Использование
simple_training_plot('output/train.log')
