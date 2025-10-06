import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont


def generate_synthetic_data():
    output_dir = "pure_azerbaijani_cyrillic_dataset"
    os.makedirs(output_dir, exist_ok=True)

    # Словарь азербайджанских кириллических слов
    azerbaijani_words = [
        # 1. Слова с уникальными диакритиками
        "şəhər", "kənd", "vilayət", "ölkə", "bölgü", "cəmiyyət", "muxtar",
        "əhali", "yaşayış", "yerləşmə", "qurutu", "dəyiş", "qədəbəy", "şağıl",
        "güzək", "təpə", "çələbi", "dəhə", "bəlgən", "cəbrail", "qubalı", "dəvəçi",
        "hacıqabul", "beyləqan", "göygöl", "daşkəsən", "qoca", "immet", "adam", "alma",

        # 2. Слова с редкими символами
        "ğəlb", "ğümüş", "ğızıl", "ğüdrət", "ğədir", "ğəzəb", "ğəfil", "ğəmir",
        "çəngəl", "çəpik", "çətin", "çəkir", "çəlik", "çəpər", "çətinə", "çəvən",
        "şəffaf", "şəkill", "şərab", "şərik", "şəhla", "şəms", "şəfəq", "şərq",
        "əcəb", "ədalət", "əfsanə", "əlbəttə", "əmanət", "əngəl", "əsr", "əvvəl",

        # 3. Слова с умлаутами
        "göz", "göl", "gün", "gür", "gəz", "gərək", "gəmir", "gəlin",
        "öz", "öl", "örək", "ötür", "ömür", "örgü", "öyüd", "övrət",
        "üç", "ülkə", "ürək", "üst", "ümid", "ünvan", "üzbəüz", "üşü",

        # 4. Слова с ç/ş/ğ комбинациями
        "çıraq", "çörək", "çiçək", "çəkmə", "çanta", "çimdik", "çevik", "çapıq",
        "şalvar", "şəkər", "şüur", "şəxsi", "şirin", "şərik", "şoul", "şəffaf",
        "qağayı", "qarğa", "ağac", "dağ", "yağış", "bağ", "çağ", "sağlam",

        # 5. Слова с редкими сочетаниями
        "müəllim", "müasir", "müəyyən", "müzakirə", "müqavimət", "müstəqil", "müraciət",
        "təhsil", "təbii", "təklif", "tərcümə", "təşkil", "təəssüf", "təbrik",
        "dərs", "dəyər", "dəqiqə", "dəvət", "dəyişik", "dəmir", "dəyirmi",
        "kitab", "külək", "kəpənək", "kəndir", "kərpic", "kəfgir", "kömək",

        # 6. Географические названия
        "Bakı", "Gəncə", "Sumqayıt", "Mingəçevir", "Naxçıvan", "Şəki", "Yevlax",
        "Lənkəran", "Şirvan", "Quba", "Xaçmaz", "Şamaxı", "Ağdam", "Cəbrayıl",
        "Füzuli", "Zəngilan", "Qazax", "Tovuz", "Balakən", "Zaqatala",

        # 7. Природные объекты
        "Xəzər", "Kür", "Araz", "Qanıx", "Tərtər", "Bazarçay", "Viləşçay",
        "Qafqaz", "BöyükQafqaz", "KiçikQafqaz", "Talış", "Naxçıvandağ",

        # 8. Культурные термины
        "muğam", "tar", "kamança", "balaban", "nəğmə", "rəqs", "xalça", "bədii",
        "şeir", "poeziya", "rəssam", "heykəl", "memar", "abidə", "mədəniyyət",

        # 9. Еда и напитки
        "plov", "dolma", "kebab", "lavash", "tendir", "çörək", "pendir", "bal",
        "çay", "qənd", "şərbət", "meyvə", "tərəvəz", "ət", "balıq", "düyü",

        # 10. Абстрактные понятия
        "sevgi", "dostluq", "sədaqət", "qəhrəman", "zəka", "hünər", "qüdrət",
        "sülh", "müharibə", "azadlıq", "müstəqillik", "inqilab", "tərəqqi",

        # 11. Профессии
        "həkim", "müəllim", "mühəndis", "işçi", "fermer", "tacir", "sənətkar",
        "rəssam", "yazıçı", "şair", "jurnalist", "aktyor", "rejissor",

        # 12. Семья и отношения
        "ata", "ana", "qardaş", "bacı", "oğul", "qız", "nəvə", "bala",
        "əmi", "dayı", "xala", "bibi", "yoldaş", "ər", "arvad", "sevgili",

        # 13. Время и дата
        "il", "ay", "həftə", "gün", "saat", "dəqiqə", "saniyə", "bu gün",
        "dünən", "sabah", "yaz", "yay", "payız", "qış", "fəsil", "əsr",

        # 14. Цвета
        "qırmızı", "yaşıl", "mavi", "sarı", "qara", "ağ", "boz", "tünd",
        "açıq", "təmiz", "parlaq", "tər", "rəng", "çalarlı", "alabalıq",

        # 15. Числа и количественные
        "bir", "iki", "üç", "dörd", "beş", "altı", "yeddi", "səkkiz",
        "doqquz", "on", "yüz", "min", "milyon", "çox", "az", "kifayət"
        # "әҹә",
        # "ҝүл",
        # "һәш",
        # "ҹым",
        # "ғыш",
        # "өҹүк",
        # "јыр",
        # "әһәң",
        # "ҹәң",
        # "шығ",
        # "ҝөј",
        # "һәңә",
        # "үчӘ",
        # "бәһә",
        # "ҝәш",
        # "јекән",
        # "ышлығ",
        # "өҹү",
        # "ҹәмә",
        # "әһән"

        # "шәһәр", "кәнд", "вилајәт", "өлкә",
        # "бөлгү", "ҹәмијјәт", "мухтар",
        # "әһали", "јашајыш", "јерлешмә", "гурту",
        # "дәјәш", "гәдәбәј", "шағыр", "гүзәк", "тәпә", "чәләби",
        # "дәһә", "гәдәбәј", "бәлгән", "ҹәбраил", "ғубалы", "дәвәчи",
        # "һаҹығabul", "бейләган", "гөйгөл", "дәшкәсән", "ғоҹа", "иммет", "Адам", "Алма", "Ана", "Арвад", "Аг", "Ачыш",
        # "Ашыг", "Ай",
        # "Бал", "Бара", "Баш", "Биз", "Бу", "Буллаг", "Банда", "Бизим",
        # "Вар", "Вәзир", "Ву", "Вә", "Вахт", "Вәсил", "Вәсит", "Вусгал",
        # "Гөз", "Галмаг", "Гапы", "Гара", "Гайгы", "Гызыл", "Гүн", "Гедж",
        # "Ғалиб", "Ғәм", "Ғейрәт", "Ғәрб", "Ғүм", "Ғыш", "Ғәләм", "Ғәрур",
        # "Дәрә", "Дүз", "Дәниз", "Дил", "Дөјүш", "Дәјә", "Дост", "Дүнја",
        # "Ел", "Ер", "Етир", "Ем", "Ешитмә", "Етишмә", "Ертә", "Ев",
        # "Әл", "Әр", "Әмә", "Әй", "Әдә", "Әзиз", "Әрәб", "Әввәл",
        # "Жан", "Жер", "Жейир", "Жүрәк", "Жәм", "Жәмијјәт", "Жәһәннәм", "Жәфәр",
        # "Зәр", "Зәм", "Зәриф", "Зәмән", "Зәһәр", "Зәка", "Зәмбил", "Зәфәр",
        # "Ики", "Ил", "Иш", "Идим", "Иј", "Ислам", "Ирәли", "Исти",
        # "Ый", "Ых", "Ышг", "Ышылдаг", "Ындагы", "Ылдыз", "Ыхлас", "Ыслам",
        # "Јан", "Јахшы", "Јалын", "Јат", "Јаман", "Јағыш", "Јашыл", "Јүз",
        # "Көл", "Кәл", "Кит", "Көрпә", "Күн", "Көк", "Кәнд", "Күч",
        # "Ҝүн", "Ҝәләм", "Ҝыймәт", "Ҝәнҹ", "Ҝәһрәман", "Ҝәдәк", "Ҝәрҹ", "Ҝәлб",
        # "Лалә", "Лев", "Ләззәт", "Лүтф", "Ләғәб", "Ләч", "Ләм", "Ләһҹә",
        # "Мән", "Мөһүббәт", "Мәктәб", "Мүаллим", "Мәсҹид", "Милләт", "Мәһәббәт", "Мөлк",
        # "Нәнә", "Нәғмә", "Нүш", "Нәсил", "Нәфәр", "Нәмә", "Нәшә", "Нүфус",
        # "Оҹаг", "Ов", "Ојун", "Оглан", "Одраг", "Од", "Олҹа", "Орта",
        # "Өј", "Өв", "Өз", "Өлкә", "Өјрән", "Өтүр", "Өмүр", "Өн",
        # "Пәнҹәрә", "Палты", "Пул", "Пәһләван", "Пәрдә", "Пишик", "Пәри", "Пак",
        # "Рәнг", "Руһ", "Рәсми", "Рәһбәр", "Рәқәм", "Рәсүл", "Рәһмәт", "Рәф",
        # "Сән", "Сөз", "Сүр", "Сәһәр", "Сәадәт", "Сәм", "Сәһифә", "Сәфәр",
        # "Тән", "Тәп", "Түт", "Тәк", "Тәсбир", "Тәрәф", "Тәһлүкә", "Тәкбир",
        # "Уч", "Уш", "Урәк", "Ушак", "Умум", "Ујур", "Улдуз", "Узун",
        # "Үз", "Үрәк", "Үч", "Үмүд", "Үзүн", "Үрүн", "Үрәк", "Үн",
        # "Фәл", "Фәһм", "Фәрз", "Фәна", "Фәрид", "Фәһл", "Фәсил", "Фәтһ",
        # "Хош", "Хал", "Хақ", "Ханым", "Хаһ", "Хәм", "Хошбәхт", "Хаҹ",
        # "Һәм", "Һә", "Һәр", "Һәмәр", "Һәјат", "Һәб", "Һәдис", "Һәмән",
        # "Чәј", "Чәк", "Чәтир", "Чәнаг", "Чәмән", "Чәһрә", "Чәләби", "Чәпәр",
        # "Ҹәм", "Ҹан", "Ҹәнг", "Ҹумһуријјәт", "Ҹәсд", "Ҹәми", "Ҹәһан", "Ҹүрә",
        # "Шәм", "Шәһәр", "Шәрг", "Шәрәф", "Шәмшәр", "Ширин", "Шәфәг", "Шәмс"
    ]

    # Шрифты (можно скачать дополнительные)
    fonts = ["arial.ttf", "times.ttf"]  # Добавьте больше шрифтов

    generated_count = 0
    labels = []

    for i in range(5000):  # Генерируем 500 примеров
        word = random.choice(azerbaijani_words)
        font_size = random.randint(20, 35)

        try:
            # Создаем изображение с текстом
            font = ImageFont.truetype(random.choice(fonts), font_size)

            # Вычисляем размер текста
            bbox = font.getbbox(word)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Создаем изображение
            img = Image.new('RGB', (text_width + 20, text_height + 20), color='white')
            draw = ImageDraw.Draw(img)

            # Добавляем текст
            text_color = (random.randint(0, 100), random.randint(0, 100), random.randint(0, 100))
            draw.text((10, 10), word, font=font, fill=text_color)

            # Добавляем шум
            img_array = np.array(img)
            noise = np.random.randint(0, 50, img_array.shape, dtype='uint8')
            img_array = cv2.add(img_array, noise)

            # Сохраняем
            filename = f"synthetic_{i:04d}.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), img_array)

            labels.append(f"{filename}\t{word}")
            generated_count += 1

            if generated_count % 50 == 0:
                print(f"Сгенерировано: {generated_count}")

        except Exception as e:
            print(f"Ошибка генерации: {e}")
            continue

    # Сохраняем labels
    with open(os.path.join(output_dir, "rec_gt.txt"), 'a', encoding='utf-8') as f:
        for label in labels:
            f.write(label + '\n')

    print(f"✅ Сгенерировано {generated_count} синтетических примеров")


generate_synthetic_data()
