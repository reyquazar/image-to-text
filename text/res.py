import re
import os


def parse_log_files():
    results = []

    for i in range(1, 11):
        log_file = f'train{i}.log'
        if not os.path.exists(log_file):
            print(f"Файл {log_file} не найден")
            continue

        print(f"Анализирую {log_file}...")

        with open(log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        best_epoch = None
        best_acc = None
        best_val_acc = None
        loss = None

        # Парсим построчно
        for line in lines:
            # Ищем строку с best metric
            if 'best metric' in line and 'best_epoch' in line:
                # Извлекаем best_epoch
                epoch_match = re.search(r'best_epoch: (\d+)', line)
                if epoch_match:
                    best_epoch = int(epoch_match.group(1))

                # Извлекаем best_acc
                acc_match = re.search(r'acc: ([\d.]+)', line)
                if acc_match:
                    acc_val = float(acc_match.group(1))
                    # Если значение меньше 1, умножаем на 100 для процентов
                    if acc_val < 1.0:
                        best_acc = acc_val * 100
                    else:
                        best_acc = min(acc_val, 100.0)

            # Ищем строки с cur metric для val_acc
            elif 'cur metric, acc:' in line:
                acc_match = re.search(r'acc: ([\d.]+)', line)
                if acc_match:
                    acc_val = float(acc_match.group(1))
                    # Если значение меньше 1, умножаем на 100 для процентов
                    if acc_val < 1.0:
                        val_acc = acc_val * 100
                    else:
                        val_acc = min(acc_val, 100.0)

                    # Сохраняем максимальное val_acc
                    if best_val_acc is None or val_acc > best_val_acc:
                        best_val_acc = val_acc

        # Если не нашли best_acc в best metric, ищем максимальное значение из cur metric
        if best_acc is None and best_val_acc is not None:
            best_acc = best_val_acc

        # Ищем loss для best_epoch
        if best_epoch:
            for line in lines:
                if f'epoch: [{best_epoch}/' in line and 'loss:' in line:
                    loss_match = re.search(r'loss: ([\d.]+)', line)
                    if loss_match:
                        loss = float(loss_match.group(1))
                        break

        results.append({
            'train_file': f'train{i}',
            'best_epoch': best_epoch,
            'best_acc': best_acc,
            'best_val_acc': best_val_acc,
            'loss': loss
        })

        print(f"  Best epoch: {best_epoch}")
        print(f"  Best acc: {best_acc:.2f}%" if best_acc is not None else "  Best acc: N/A")
        print(f"  Best val acc: {best_val_acc:.2f}%" if best_val_acc is not None else "  Best val acc: N/A")
        print(f"  Loss: {loss:.4f}" if loss is not None else "  Loss: N/A")

    return results


def create_table(results):
    print("\n" + "=" * 60)
    print("ФИНАЛЬНАЯ ТАБЛИЦА ДЛЯ ПРЕЗЕНТАЦИИ")
    print("=" * 60)
    print("| Train File | Best Epoch | Best Acc % | Val Acc % | Loss |")
    print("|------------|------------|------------|-----------|------|")

    for result in results:
        train_file = result['train_file']
        best_epoch = result['best_epoch'] or "N/A"
        best_acc = f"{result['best_acc']:.2f}" if result['best_acc'] is not None else "N/A"
        best_val_acc = f"{result['best_val_acc']:.2f}" if result['best_val_acc'] is not None else "N/A"
        loss = f"{result['loss']:.4f}" if result['loss'] is not None else "N/A"

        print(f"| {train_file} | {best_epoch} | {best_acc} | {best_val_acc} | {loss} |")


# Запускаем анализ
print("Анализ лог-файлов...")
results = parse_log_files()

create_table(results)

# Дополнительная статистика
if results:
    acc_values = [r['best_acc'] for r in results if r['best_acc'] is not None]
    val_acc_values = [r['best_val_acc'] for r in results if r['best_val_acc'] is not None]

    if acc_values:
        print(f"\nСтатистика:")
        print(f"Средний Best Acc: {sum(acc_values) / len(acc_values):.2f}%")
        print(f"Максимальный Best Acc: {max(acc_values):.2f}%")
        print(f"Минимальный Best Acc: {min(acc_values):.2f}%")

    if val_acc_values:
        print(f"Средний Val Acc: {sum(val_acc_values) / len(val_acc_values):.2f}%")
        print(f"Максимальный Val Acc: {max(val_acc_values):.2f}%")
        print(f"Минимальный Val Acc: {min(val_acc_values):.2f}%")