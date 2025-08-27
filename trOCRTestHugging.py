# from transformers import TrOCRProcessor, VisionEncoderDecoderModel
# from PIL import Image
# import requests
#
# # Load processor and model
# processor = TrOCRProcessor.from_pretrained("cyrillic-trocr/trocr-handwritten-cyrillic")
# model = VisionEncoderDecoderModel.from_pretrained("cyrillic-trocr/trocr-handwritten-cyrillic")
#
# # Load and prepare image
# image = Image.open("test10.png").convert("RGB")
# pixel_values = processor(images=image, return_tensors="pt").pixel_values
#
# # Generate prediction
# generated_ids = model.generate(pixel_values)
# predicted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
# print(predicted_text)
