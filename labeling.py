def replace_symbols_in_file(filename):
    """
    Заменяет специальные символы на буквы в указанном файле
    """

    replacements = {
        '~': 'ü', '`': 'ı', '!': 'ö', '@': 'ğ', '#': 'ə', '$': 'ş', '%': 'ç',
        '^': 'Ü', '&': 'İ', '*': 'Ö', '_': 'Ğ', '-': 'Ə', '+': 'Ş', '=': 'Ç'
    }

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()

        for symbol, letter in replacements.items():
            content = content.replace(symbol, letter)

        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Файл '{filename}' успешно обработан!")

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден!")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# Использование
replace_symbols_in_file('./text/typed_text/az_config_train/Label.txt')