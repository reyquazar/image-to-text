from doctr.io import DocumentFile
from doctr.models import ocr_predictor
from PIL import Image
import os
import matplotlib

matplotlib.use('TkAgg')

image_path = 'test10.png'
original_image = Image.open(image_path)

output_dir = 'words'
os.makedirs(output_dir, exist_ok=True)

model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)
image_doc = DocumentFile.from_images(image_path)
result = model(image_doc)



def extract_and_save_words_pil(result, original_image, output_dir):
    word_count = 0

    for page in result.pages:
        for block in page.blocks:
            for line in block.lines:
                for word in line.words:
                    bbox = word.geometry
                    x_min = int(bbox[0][0] * original_image.width)
                    y_min = int(bbox[0][1] * original_image.height)
                    x_max = int(bbox[1][0] * original_image.width)
                    y_max = int(bbox[1][1] * original_image.height)

                    word_image = original_image.crop((x_min, y_min, x_max, y_max))

                    padding = 10
                    padded_image = Image.new('RGB',
                                             (word_image.width + 2 * padding,
                                              word_image.height + 2 * padding),
                                             (255, 255, 255))
                    padded_image.paste(word_image, (padding, padding))

                    filename = f"image_{word_count:04d}.png"
                    output_path = os.path.join(output_dir, filename)
                    padded_image.save(output_path)

                    word_count += 1

    return word_count


total_words = extract_and_save_words_pil(result, original_image, output_dir)
print(f"Всего сохранено слов: {total_words}")
result.show()
