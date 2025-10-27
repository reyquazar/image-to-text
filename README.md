# Report on Browser Extension OCR Task Implementation

## Completed Work:

### 1. Environment Setup and Technology Selection

- Selected PaddleOCR as more powerful alternative to TesseractOCR
- Repository cloned: `git clone https://github.com/reyquazar/image-to-text.git` (develop branch)
- Dependencies installation:

```
python -m pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
```

```
python -m pip install "paddleocr[all]"
```

```
python -m pip install albumentations RapidFuzz lmdb scikit-image PyYAML
```

### 2. Data Annotation

- Data annotation launched via Python script:

```
python .\venv\Lib\site-packages\PPOCRLabel\PPOCRLabel.py --lang en
```

- 8 images annotated for model training
- Annotated images saved in `./text/typed_text/crop_image`
- Annotation file: `rec_gt.txt`

### 3. Model Training Preparation

- Studied PaddleOCR fine-tuning documentation
- Created working configuration file: `./text/typed_text/debug_rec.yaml`
- Prepared augmentation dictionary: `./text/typed_text/dict.txt`
- Downloaded additional fonts for training

### 4. Synthetic Data Generation

- Created `genDataTrainVal.py` program for synthetic data generation
- Implemented parameter support for data quantity (example: `python .\genDataTrainVal.py 80000 10000`)
- Created alternative program `TrainVal.py` for using original data from `crop_img`
- Generated `train_list.txt` and `val_list.txt` files

### 5. Model Training

- Downloaded PaddleOCR repository: `git clone https://github.com/PaddlePaddle/PaddleOCR.git`
- Downloaded pre-trained
  model: `wget https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-OCRv5_server_rec_pretrained -P ./text/typed_text/pretrain_models`
- Launched training process: `python ../PaddleOCR/tools/train.py -c ./text/typed_text/az_rec_config.yaml`
- Achieved accuracy above 90%

### 6. Model Export

- Created inference
  model: `python ../PaddleOCR/tools/export_model.py -c ./text/typed_text/debug_rec.yaml -o Global.pretrained_model=output/best_accuracy.pdparams Global.save_inference_dir=output/inference`

[//]: # (- REMOVE `CTCLABELENCODE: null` ```vim output/inference/inference.yml``` does not work with it)

### 7. Model Testing

- Implemented testing script: `python .\testFast.py .\img.png`
- Comparison between original and fine-tuned model results

### 8. Browser Extension Development

- Created server architecture for PaddleOCR integration into browser extension
- Functionality implemented in `./image-to-text/ExtensionServerPaddleOCR` folder
- Worked with JavaScript for interface creation
- Core extension functionality is operational
