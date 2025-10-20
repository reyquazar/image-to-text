from paddleocr import *


def Pstructure(img):
    pipeline = PPStructureV3()
    result = pipeline.predict(img)

    return result


def POCR(image):
    from paddleocr import PaddleOCR

    ocr = PaddleOCR(text_recognition_model_name="PP-OCRv5_server_rec", use_textline_orientation=False)
    result = ocr.predict(image)
    return result


def PRec(image):
    ocr = PaddleOCR(text_recognition_model_name='PP-OCRv5_server_rec', use_textline_orientation=False)
    result = ocr.predict(image)
    return result


def PDet(image):
    model = TextDetection()
    result = model.predict(image)
    return result


def main():
    image_path = 'text/typed_text/az_config_train/img.png'
    # image_path = 'img.png'
    result = ""
    # result = Pstructure(image)
    result = PRec(image_path)
    # result = PDet(image)
    # result = POCR(image_path)
    # print(result)
    count = 1
    for res in result:
        count += 1
        res.save_to_img("output")
        # res.save_to_json("output")
        # res.save_to_markdown("output")


if __name__ == "__main__":
    main()
