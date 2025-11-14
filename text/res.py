import re
import os
import glob
from datetime import datetime


def analyze_log_file(file_path):
    """
    Анализирует файл лога и извлекает ключевые метрики
    """
    print(f"\n{'=' * 80}")
    print(f"АНАЛИЗ ФАЙЛА: {file_path}")
    print(f"{'=' * 80}")

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Инициализация переменных
    results = {
        'file': file_path,
        'best_accuracy': 0,
        'best_epoch': 0,
        'best_norm_edit_dis': 0,
        'final_metrics': {},
        'epoch_data': [],
        'training_stats': [],
        'convergence_epochs': []
    }

    # Регулярные выражения для поиска метрик
    patterns = {
        'cur_metric': r'cur metric, acc: ([\d.]+), norm_edit_dis: ([\d.]+)',
        'best_metric': r'best metric, acc: ([\d.]+).*?best_epoch: (\d+)',
        'epoch_data': r'epoch: \[(\d+)/(\d+)\].*?lr: ([\d.]+), acc: ([\d.]+), norm_edit_dis: ([\d.]+), CTCLoss: ([\d.]+), NRTRLoss: ([\d.]+), loss: ([\d.]+)',
        'final_metrics_full': r'best metric, acc: ([\d.]+),.*?norm_edit_dis: ([\d.]+), fps: ([\d.]+), best_epoch: (\d+)'
    }

    # Поиск всех метрик валидации
    cur_metrics = re.findall(patterns['cur_metric'], content)
    best_metrics = re.findall(patterns['best_metric'], content)
    epoch_records = re.findall(patterns['epoch_data'], content)

    # Обработка лучших метрик
    if best_metrics:
        best_acc, best_epoch = best_metrics[-1]
        results['best_accuracy'] = float(best_acc)
        results['best_epoch'] = int(best_epoch)

        # Поиск полной информации о лучших метриках
        final_metrics = re.findall(patterns['final_metrics_full'], content)
        if final_metrics:
            best_acc_full, best_norm_edit, fps, best_ep = final_metrics[-1]
            results['final_metrics'] = {
                'accuracy': float(best_acc_full),
                'norm_edit_dis': float(best_norm_edit),
                'fps': float(fps),
                'best_epoch': int(best_ep)
            }

    # Обработка метрик валидации
    if cur_metrics:
        results['convergence_epochs'] = []
        for i, (acc, norm_edit) in enumerate(cur_metrics):
            results['convergence_epochs'].append({
                'epoch': i + 1,
                'accuracy': float(acc),
                'norm_edit_dis': float(norm_edit)
            })

    # Обработка данных обучения по эпохам
    if epoch_records:
        for record in epoch_records:
            epoch, total_epochs, lr, acc, norm_edit, ctcloss, nrtrloss, loss = record
            results['epoch_data'].append({
                'epoch': int(epoch),
                'total_epochs': int(total_epochs),
                'lr': float(lr),
                'accuracy': float(acc),
                'norm_edit_dis': float(norm_edit),
                'CTCLoss': float(ctcloss),
                'NRTRLoss': float(nrtrloss),
                'loss': float(loss)
            })

    # Анализ трендов
    if results['epoch_data']:
        last_epoch = results['epoch_data'][-1]
        first_epoch_data = [x for x in results['epoch_data'] if x['epoch'] == 1]

        if first_epoch_data:
            results['training_stats'] = {
                'start_lr': first_epoch_data[0]['lr'],
                'final_lr': last_epoch['lr'],
                'final_training_acc': last_epoch['accuracy'],
                'final_loss': last_epoch['loss'],
                'final_CTCLoss': last_epoch['CTCLoss'],
                'final_NRTRLoss': last_epoch['NRTRLoss'],
                'total_epochs_trained': last_epoch['total_epochs']
            }

    return results


def print_detailed_summary(results):
    """Выводит подробную сводку по анализу"""

    print(f"\n📊 ПОДРОБНАЯ СВОДКА ДЛЯ: {os.path.basename(results['file'])}")
    print("-" * 60)

    # Лучшие метрики
    if results['final_metrics']:
        fm = results['final_metrics']
        print(f"🏆 ЛУЧШИЕ ПОКАЗАТЕЛИ:")
        print(f"   • Accuracy: {fm['accuracy']:.4f}")
        print(f"   • Norm Edit Distance: {fm['norm_edit_dis']:.4f}")
        print(f"   • FPS: {fm['fps']:.1f}")
        print(f"   • Лучшая эпоха: {fm['best_epoch']}")

    # Статистика обучения
    if results['training_stats']:
        ts = results['training_stats']
        print(f"\n📈 СТАТИСТИКА ОБУЧЕНИЯ:")
        print(f"   • Learning Rate: {ts['start_lr']:.6f} → {ts['final_lr']:.6f}")
        print(f"   • Final Training Accuracy: {ts['final_training_acc']:.4f}")
        print(f"   • Final Loss: {ts['final_loss']:.4f}")
        print(f"   • Final CTCLoss: {ts['final_CTCLoss']:.4f}")
        print(f"   • Final NRTRLoss: {ts['final_NRTRLoss']:.4f}")
        print(f"   • Всего эпох: {ts['total_epochs_trained']}")

    # Анализ сходимости
    if results['convergence_epochs']:
        print(f"\n📅 ДИНАМИКА СХОДИМОСТИ:")
        for metric in results['convergence_epochs']:
            trend = "↑" if metric['accuracy'] >= results['best_accuracy'] else "↓"
            print(f"   Эпоха {metric['epoch']}: acc={metric['accuracy']:.4f} {trend}")

    # Анализ стабильности
    if results['epoch_data']:
        last_epoch_data = [x for x in results['epoch_data'] if x['epoch'] == results.get('best_epoch', 1)]
        if last_epoch_data:
            print(f"\n⚡ СТАТИСТИКА ПОСЛЕДНЕЙ ЭПОХИ:")
            acc_values = [x['accuracy'] for x in last_epoch_data]
            loss_values = [x['loss'] for x in last_epoch_data]
            print(
                f"   • Accuracy: min={min(acc_values):.4f}, max={max(acc_values):.4f}, avg={sum(acc_values) / len(acc_values):.4f}")
            print(
                f"   • Loss: min={min(loss_values):.4f}, max={max(loss_values):.4f}, avg={sum(loss_values) / len(loss_values):.4f}")

    # Оценка качества обучения
    print(f"\n🎯 ОЦЕНКА КАЧЕСТВА ОБУЧЕНИЯ:")
    if results['best_accuracy'] > 0.75:
        print("   ✅ Отличный результат! Модель хорошо обучилась.")
    elif results['best_accuracy'] > 0.65:
        print("   ⚠️  Хороший результат, но есть потенциал для улучшения.")
    else:
        print("   ❌ Требуется донастройка гиперпараметров.")

    if results['training_stats'] and results['training_stats']['final_loss'] < 2.0:
        print("   ✅ Loss стабильно низкий, обучение прошло успешно.")
    else:
        print("   ⚠️  Loss偏高, возможно требуется регулировка learning rate.")


def compare_all_logs(log_files):
    """Сравнивает все лог файлы и выводит сравнительную таблицу"""
    print(f"\n{'=' * 100}")
    print(f"СРАВНИТЕЛЬНАЯ ТАБЛИЦА ВСЕХ ЭКСПЕРИМЕНТОВ")
    print(f"{'=' * 100}")

    all_results = []

    for log_file in log_files:
        results = analyze_log_file(log_file)
        all_results.append(results)

    # Вывод сравнительной таблицы
    print(f"\n{'Название файла':<30} {'Лучший acc':<12} {'Лучшая эпоха':<12} {'Final LR':<10} {'Final Loss':<12}")
    print("-" * 80)

    for result in all_results:
        filename = os.path.basename(result['file'])
        best_acc = result.get('best_accuracy', 0)
        best_epoch = result.get('best_epoch', 0)
        final_lr = result.get('training_stats', {}).get('final_lr', 0)
        final_loss = result.get('training_stats', {}).get('final_loss', 0)

        print(f"{filename:<30} {best_acc:<12.4f} {best_epoch:<12} {final_lr:<10.6f} {final_loss:<12.4f}")


def main():
    """Основная функция"""
    # Поиск всех log файлов в текущей директории
    log_files = glob.glob("*.log") + glob.glob("train*.log") + glob.glob("*.txt")

    if not log_files:
        print("❌ Лог файлы не найдены!")
        print("Убедитесь, что файлы с расширением .log находятся в текущей директории.")
        return

    print(f"📁 Найдено файлов: {len(log_files)}")

    # Анализ каждого файла
    all_results = []
    for log_file in log_files:
        try:
            results = analyze_log_file(log_file)
            print_detailed_summary(results)
            all_results.append(results)
        except Exception as e:
            print(f"❌ Ошибка при анализе файла {log_file}: {e}")

    # Сравнительная таблица
    if len(all_results) > 1:
        compare_all_logs(log_files)

    # Нахождение лучшего эксперимента
    if all_results:
        best_result = max(all_results, key=lambda x: x.get('best_accuracy', 0))
        print(f"\n🎉 ЛУЧШИЙ ЭКСПЕРИМЕНТ: {os.path.basename(best_result['file'])}")
        print(f"   Accuracy: {best_result['best_accuracy']:.4f}")


if __name__ == "__main__":
    main()
