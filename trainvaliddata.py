import os
from sklearn.model_selection import train_test_split


rec_gt_txt = "text/typed_text/rec_gt.txt"
train_output_file = "text/typed_text/train_list.txt"
val_output_file = "text/typed_text/val_list.txt"


with open(rec_gt_txt, 'r', encoding='utf-8') as f:
    lines = f.readlines()

cleaned_lines = [line.strip() for line in lines if line.strip()]

train_lines, val_lines = train_test_split(
    cleaned_lines,
    test_size=0.1,
    random_state=42,
    shuffle=True
)

with open(train_output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(train_lines))

with open(val_output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(val_lines))

print(f"Всего samples: {len(cleaned_lines)}")
print(f"Тренировочных samples: {len(train_lines)}")
print(f"Валидационных samples: {len(val_lines)}")
print(f"Соотношение: {len(train_lines)/len(cleaned_lines):.1%} / {len(val_lines)/len(cleaned_lines):.1%}")