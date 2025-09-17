from paddleocr import *


def Pstructure(img):
    pipeline = PPStructureV3()
    result = pipeline.predict(img)

    return result


def POCR(image):
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(
        use_doc_orientation_classify=False,  # Disables document orientation classification model via this parameter
        use_doc_unwarping=False,  # Disables text image rectification model via this parameter
        use_textline_orientation=False,  # Disables text line orientation classification model via this parameter
        text_det_thresh=0.25,
        lang="ru"

    )
    # ocr = PaddleOCR(
    #     text_detection_model_name="PP-OCRv5_mobile_det",
    #     text_recognition_model_name="PP-OCRv5_mobile_rec",
    result = ocr.predict(image)
    return result


def PRec(image):
    ocr = PaddleOCR(text_recognition_model_name='PP-OCRv5_server_rec')
    result = ocr.predict(image)
    return result


def PDet(image):
    model = TextDetection()
    result = model.predict(image)
    return result


def main():
    image_path = 'text/typed_text/test4.png'
    # image_path = 'img.png'
    result = ""
    # result = Pstructure(image)
    result = PRec(image_path)
    # result = PDet(image)
    # result = POCR(image_path)
    # print(result)
    count = 1
    for res in result:
        print(f"{count}. {res}")
        count += 1
        # res.save_to_img("output")
        # res.save_to_json("output")
        # res.save_to_markdown("output")


if __name__ == "__main__":
    main()
