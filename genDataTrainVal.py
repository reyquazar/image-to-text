import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import argparse


def generate_synthetic_data():
    output_dir = "./text/typed_text/pure_azerbaijani_cyrillic_dataset"
    os.makedirs(output_dir, exist_ok=True)

    fonts_dir = "./text/typed_text/pure_azerbaijani_cyrillic_dataset/fonts/3"

    print(f"🔍 Find fonts: {fonts_dir}")

    azerbaijani_words = ["şəğıl", "ölkə", "ğümüş"
                         # # 1. Слова с уникальными диакритиками
                         # "şəhər", "kənd", "vilayət", "ölkə", "bölgü", "cəmiyyət", "muxtar",
                         # "əhali", "yaşayış", "yerləşmə", "qurutu", "dəyiş", "qədəbəy", "şağıl",
                         # "güzək", "təpə", "çələbi", "dəhə", "bəlgən", "cəbrail", "qubalı", "dəvəçi",
                         # "hacıqabul", "beyləqan", "göygöl", "daşkəsən", "qoca", "immet", "adam", "alma",
                         #
                         # # 2. Слова с редкими символами
                         # "ğəlb", "ğümüş", "ğızıl", "ğüdrət", "ğədir", "ğəzəb", "ğəfil", "ğəmir",
                         # "çəngəl", "çəpik", "çətin", "çəkir", "çəlik", "çəpər", "çətinə", "çəvən",
                         # "şəffaf", "şəkill", "şərab", "şərik", "şəhla", "şəms", "şəfəq", "şərq",
                         # "əcəb", "ədalət", "əfsanə", "əlbəttə", "əmanət", "əngəl", "əsr", "əvvəl",
                         #
                         # # 3. Слова с умлаутами
                         # "göz", "göl", "gün", "gür", "gəz", "gərək", "gəmir", "gəlin",
                         # "öz", "öl", "örək", "ötür", "ömür", "örgü", "öyüd", "övrət",
                         # "üç", "ülkə", "ürək", "üst", "ümid", "ünvan", "üzbəüz", "üşü",
                         #
                         # # 4. Слова с ç/ş/ğ комбинациями
                         # "çıraq", "çörək", "çiçək", "çəkmə", "çanta", "çimdik", "çevik", "çapıq",
                         # "şalvar", "şəkər", "şüur", "şəxsi", "şirin", "şərik", "şoul", "şəffaf",
                         # "qağayı", "qarğa", "ağac", "dağ", "yağış", "bağ", "çağ", "sağlam",
                         #
                         # # 5. Слова с редкими сочетаниями
                         # "müəllim", "müasir", "müəyyən", "müzakirə", "müqavimət", "müstəqil", "müraciət",
                         # "təhsil", "təbii", "təklif", "tərcümə", "təşkil", "təəssüf", "təbrik",
                         # "dərs", "dəyər", "dəqiqə", "dəvət", "dəyişik", "dəmir", "dəyirmi",
                         # "kitab", "külək", "kəpənək", "kəndir", "kərpic", "kəfgir", "kömək",
                         #
                         # # 6. Географические названия
                         # "Bakı", "Gəncə", "Sumqayıt", "Mingəçevir", "Naxçıvan", "Şəki", "Yevlax",
                         # "Lənkəran", "Şirvan", "Quba", "Xaçmaz", "Şamaxı", "Ağdam", "Cəbrayıl",
                         # "Füzuli", "Zəngilan", "Qazax", "Tovuz", "Balakən", "Zaqatala",
                         #
                         # # 7. Природные объекты
                         # "Xəzər", "Kür", "Araz", "Qanıx", "Tərtər", "Bazarçay", "Viləşçay",
                         # "Qafqaz", "BöyükQafqaz", "KiçikQafqaz", "Talış", "Naxçıvandağ",
                         #
                         # # 8. Культурные термины
                         # "muğam", "tar", "kamança", "balaban", "nəğmə", "rəqs", "xalça", "bədii",
                         # "şeir", "poeziya", "rəssam", "heykəl", "memar", "abidə", "mədəniyyət",
                         #
                         # # 9. Еда и напитки
                         # "plov", "dolma", "kebab", "lavash", "tendir", "çörək", "pendir", "bal",
                         # "çay", "qənd", "şərbət", "meyvə", "tərəvəz", "ət", "balıq", "düyü",
                         #
                         # # 10. Абстрактные понятия
                         # "sevgi", "dostluq", "sədaqət", "qəhrəman", "zəka", "hünər", "qüdrət",
                         # "sülh", "müharibə", "azadlıq", "müstəqillik", "inqilab", "tərəqqi",
                         #
                         # # 11. Профессии
                         # "həkim", "müəllim", "mühəndis", "işçi", "fermer", "tacir", "sənətkar",
                         # "rəssam", "yazıçı", "şair", "jurnalist", "aktyor", "rejissor",
                         #
                         # # 12. Семья и отношения
                         # "ata", "ana", "qardaş", "bacı", "oğul", "qız", "nəvə", "bala",
                         # "əmi", "dayı", "xala", "bibi", "yoldaş", "ər", "arvad", "sevgili",
                         #
                         # # 13. Время и дата
                         # "il", "ay", "həftə", "gün", "saat", "dəqiqə", "saniyə", "bu gün",
                         # "dünən", "sabah", "yaz", "yay", "payız", "qış", "fəsil", "əsr",
                         #
                         # # 14. Цвета
                         # "qırmızı", "yaşıl", "mavi", "sarı", "qara", "ağ", "boz", "tünd",
                         # "açıq", "təmiz", "parlaq", "tər", "rəng", "çalarlı", "alabalıq",
                         #
                         # # 15. Числа и количественные
                         # "bir", "iki", "üç", "dörd", "beş", "altı", "yeddi", "səkkiz",
                         # "doqquz", "on", "yüz", "min", "milyon", "çox", "az", "kifayət"
                         # "әҹә", "ҝүл", "һәш", "ҹым", "ғыш", "өҹүк", "јыр", "әһәң", "ҹәң", "шығ", "ҝөј",
                         # "һәңә", "үчӘ", "бәһә", "ҝәш", "јекән", "ышлығ", "өҹү", "ҹәмә", "әһән"

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
    available_fonts = []
    if os.path.exists(fonts_dir):
        for file in os.listdir(fonts_dir):
            if file.lower().endswith('.ttf'):
                font_path = os.path.join(fonts_dir, file)
                try:
                    test_font = ImageFont.truetype(font_path, 20)
                    available_fonts.append(font_path)
                    print(f"✅ Font loaded: {file}")
                except Exception as e:
                    print(f"❌ Error font load: {file}: {e}")
    else:
        print(f"❌ Dir with fonts: {fonts_dir}")
        return

    if not available_fonts:
        print("❌ Not available fonts!")
        return

    print(f"🎯 Used {len(available_fonts)} fonts")

    backgrounds = ['white', 'lightgray', 'aliceblue', 'seashell']

    generated_count = 0
    labels = []
    parser = argparse.ArgumentParser()
    parser.add_argument('number', type=int)
    args = parser.parse_args()

    for i in range(args.number):
        word = random.choice(azerbaijani_words)

        font_size = random.randint(22, 32)
        bg_color = random.choice(backgrounds)
        text_color = (
            random.randint(0, 80),
            random.randint(0, 80),
            random.randint(0, 80)
        )

        rotation = random.randint(-3, 3)
        blur_radius = random.uniform(0, 0.3)
        contrast = random.uniform(0.9, 1.2)
        brightness = random.uniform(0.9, 1.1)

        try:
            word_to_draw = word

            font_path = random.choice(available_fonts)
            font = ImageFont.truetype(font_path, font_size)

            bbox = font.getbbox(word_to_draw)
            text_width = bbox[2] - bbox[0] + 40
            text_height = bbox[3] - bbox[1] + 40

            img = Image.new('RGB', (text_width, text_height), color=bg_color)
            draw = ImageDraw.Draw(img)

            if random.random() < 0.1:  # Только 10% случаев
                for y in range(img.height):
                    shade = 240 + int(10 * (y / img.height))
                    for x in range(img.width):
                        img.putpixel((x, y), (shade, shade, shade))

            x_offset = (img.width - (bbox[2] - bbox[0])) // 2
            y_offset = (img.height - (bbox[3] - bbox[1])) // 2
            draw.text((x_offset, y_offset), word_to_draw, font=font, fill=text_color)

            if rotation != 0:
                img = img.rotate(rotation, expand=True, fillcolor=bg_color)

            if blur_radius > 0.05:
                img = img.filter(ImageFilter.GaussianBlur(blur_radius))

            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(contrast)

            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(brightness)

            img_array = np.array(img)

            if random.random() < 0.3:
                noise_type = random.choice(['gaussian', 'none'])
                if noise_type == 'gaussian':
                    noise = np.random.normal(0, random.randint(1, 5), img_array.shape).astype('uint8')
                    img_array = cv2.add(img_array, noise)

            final_width, final_height = 320, 48

            img_resized = cv2.resize(img_array, (final_width, final_height), interpolation=cv2.INTER_LINEAR)

            filename = f"synthetic_{i:05d}.jpg"
            cv2.imwrite(os.path.join(output_dir, filename), img_resized)

            labels.append(f"{filename}\t{word}")
            generated_count += 1

            if generated_count % 10 == 0:
                print(f"Generated: {generated_count}")

        except Exception as e:
            print(f"Gen error: {e}")
            continue

    random.shuffle(labels)
    split_idx = int(0.9 * len(labels))

    with open(os.path.join(output_dir, "train_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels[:split_idx]:
            f.write(label + '\n')

    with open(os.path.join(output_dir, "val_list.txt"), 'w', encoding='utf-8') as f:
        for label in labels[split_idx:]:
            f.write(label + '\n')

    print(f"✅ Generated {generated_count} synt data")
    print(f"📊 Train: {split_idx}, Val: {len(labels) - split_idx}")


generate_synthetic_data()
