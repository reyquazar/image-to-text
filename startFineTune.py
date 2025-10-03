# Английский алфавит заглавные + прописные
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Вывод букв столбиком
with open("alphabet.txt", "w", encoding='utf-8') as f:
    for letter in alphabet:
        f.write(letter + '\n')
