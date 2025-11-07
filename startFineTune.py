def remove_true_anomalies(input_file, output_file):
    """
    Удаляет только действительно проблемные слова
    """
    true_anomalies = [
        # Английские слова
        'All', 'Ann', 'Antenn', 'Azercell', 'Bakcell', 'Bill', 'Bonn', 'Buffett',
        'Bull', 'Constrktion', 'Crystal', 'Crystall', 'Martyrs', 'Oncorhynchus',
        'Psychiatry', 'Qualcomm', 'Shell', 'Zenqstşmid', 'kontrproduktivdir',
        # Технические термины
        'call', 'doll', 'off', 'pdf', 'playoff', 'xbox',
        # Слишком короткие иностранные
        'dj', 'ex', 'fm', 'jo', 'max', 'tv', 'ufo'
    ]

    removed_count = 0
    processed_words = []

    with open(input_file, 'r', encoding='utf-8') as infile:
        for line in infile:
            word = line.strip()

            if word and word not in true_anomalies:
                processed_words.append(word)
            else:
                removed_count += 1

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for word in processed_words:
            outfile.write(word + '\n')

    return removed_count, len(processed_words)


# Запуск
input_file = "train_cleaned_ocr_final.txt"
output_file = "train_cleaned_ocr_perfect.txt"

removed, kept = remove_true_anomalies(input_file, output_file)
print(f"✅ Удалено {removed} действительно проблемных слов")
print(f"📊 Сохранено {kept} чистых азербайджанских слов")