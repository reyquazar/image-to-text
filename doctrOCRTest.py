from doctr.io import DocumentFile
import matplotlib

matplotlib.use('TkAgg')
image_path = 'test10.png'

image_doc = DocumentFile.from_images(image_path)

from doctr.models import *

model = ocr_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)

# model = kie_predictor(det_arch='db_resnet50', reco_arch='crnn_vgg16_bn', pretrained=True)


result = model(image_doc)

result.show()