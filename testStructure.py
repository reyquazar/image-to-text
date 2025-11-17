# import argparse
# from paddleocr import PPStructureV3
#
#
# def PRec(image):
#     ocr = PPStructureV3()
#     result = ocr.predict(image)
#     if result and len(result) > 0:
#         page = result[0]
#         texts = page.get('rec_texts', [])
#         combined_text = ' '.join(texts)
#     print("=" * 100)
#     print("PaddleModel")
#     print("=" * 100)
#     print(combined_text)
#     print("=" * 100)
#
#
# def printL(model, image, text):
#     ocr = PPStructureV3(
#         text_recognition_model_dir=f"./{model}/inference/",
#         use_doc_orientation_classify=False,
#         use_textline_orientation=False,
#     )
#     result = ocr.predict(image)
#     if result and len(result) > 0:
#         page = result[0]
#         texts = page.get('rec_texts', [])
#         combined_text = ' '.join(texts)
#     print("=" * 150)
#     print(model, text)
#     print("=" * 150)
#     print(combined_text)
#     print("=" * 150)
#
#
# def main():
#     parser = argparse.ArgumentParser()
#     parser.add_argument('image_path', type=str)
#     args = parser.parse_args()
#     image_path = args.image_path
#     # image_path = './text/typed_text/testWords.png'
#
#     PRec(image_path)  # default paddle model
#     printL("output1", image_path, "synt data gDTV2Words.py Train 100k Val 10k")  # synt data with gDTV2Words.py
#     printL("output2", image_path, "synt data gDTV2Words.py Train 100k Val 10k")  # synt data with gDTV2Words.py
#     printL("output3", image_path, "synt data gDTV2Words2.py  Train 200k Val 20k")  # synt data with gDTV2Words2.py
#     printL("output4", image_path, "synt data gDTV2Words2.py Train 200k Val 20k")  # synt data with gDTV2Words2.py
#     printL("output5", image_path, "synt data gDTV2Words3.py Train 100k Val 10k")  # synt data with gDTV2Words3.py
#     printL("output6", image_path, "synt data gDTV2Words3.py Train 100k Val 10k")  # synt data with gDTV2Words3.py
#     printL("output7", image_path, "hw original test1-18.png")  # hw + copy do 18.png
#     printL("output8", image_path, "hw original test1-18.png")  # hw + copy all.png
#     printL("output", image_path, "latest output Train 100k Val 10k")
#
#
# if __name__ == "__main__":
#     main()


from paddleocr import PPStructureV3

# pipeline = PPStructureV3()
# pipeline = PPStructureV3(lang="en") # Set the lang parameter to use the English text recognition model. For other supported languages, see Section 5: Appendix. By default, both Chinese and English text recognition models are enabled.
# pipeline = PPStructureV3(use_doc_orientation_classify=True) # Use use_doc_orientation_classify to enable/disable document orientation classification model
# pipeline = PPStructureV3(use_doc_unwarping=True) # Use use_doc_unwarping to enable/disable document unwarping module
# pipeline = PPStructureV3(use_textline_orientation=True) # Use use_textline_orientation to enable/disable textline orientation classification model
pipeline = PPStructureV3(device="gpu",
                         text_recognition_model_dir="./output2/inference/",
                         )  # Use device to specify GPU for model inference
img_path = "./OriginalImages/test2.png"
output = pipeline.predict(img_path)
for res in output:
    res.print()  ## Print the structured prediction output
    res.save_to_markdown(save_path="outputGit")  ## Save the current image's result in Markdown format
