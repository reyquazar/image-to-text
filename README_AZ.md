# Brauzer üçün OCR genişləndirməsinin yaradılması üzrə tapşırığın icrası hesabatı

## Yerinə yetirilən işlər:

### 1. Mühitin qurulması və texnologiyanın seçimi

- TesseractOCR ilə müqayisədə daha güclü alternativ kimi PaddleOCR seçildi
- Repozitoriya klonlandı: `git clone https://github.com/reyquazar/image-to-text.git` (develop qolu)
- Asılılıqların quraşdırılması:

```
python -m pip install paddlepaddle-gpu==3.0.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/
```

```
python -m pip install "paddleocr[all]"
```

```
python -m pip install albumentations RapidFuzz lmdb scikit-image PyYAML
```

### 2. Məlumatların işarələnməsi

- Python skripti vasitəsilə məlumatların işarələnməsi:

```
python .\venv\Lib\site-packages\PPOCRLabel\PPOCRLabel.py --lang en
```

- Modelin təlimi üçün 8 şəkil işarələndi
- İşarələnmiş şəkillər `./text/typed_text/crop_image` qovluğunda saxlanıldı
- İşarələmə faylı: `rec_gt.txt`

### 3. Modelin təliminə hazırlıq

- PaddleOCR sənədləşməsi öyrənildi (fine-tuning)
- İşləyən konfiqurasiya faylı yaradıldı: `./text/typed_text/debug_rec.yaml`
- Genişləndirmə üçün lüğət hazırlandı: `dict.txt`
- Təlim üçün əlavə fontlar yükləndi

### 4. Sintetik məlumatların yaradılması

- Sintetik məlumatların yaradılması üçün `genDataTrainVal.py` proqramı hazırlandı
- Məlumat miqdarı üçün parametr dəstəyi təmin edildi (nümunə: `python .\genDataTrainVal.py 80000 10000`)
- `crop_img` qovluğundan orijinal məlumatların istifadəsi üçün alternativ `TrainVal.py` proqramı yaradıldı
- `train_list.txt` və `val_list.txt` faylları yaradıldı

### 5. Modelin tədqiqi

- PaddleOCR repozitoriyası yükləndi: `git clone https://github.com/PaddlePaddle/PaddleOCR.git`
- Əvvəlcədən təlim keçmiş model
  yükləndi: `wget https://paddle-model-ecology.bj.bcebos.com/paddlex/official_pretrained_model/PP-OCRv5_server_rec_pretrained -P ./text/typed_text/pretrain_models`
- Təlim prosesi başladıldı: `python ../PaddleOCR/tools/train.py -c ./text/typed_text/debug_rec.yaml`
- 90%-dən yuxarı dəqiqlik əldə edildi

### 6. Modelin ixracı

- İnferens modeli
  yaradıldı: `python ../PaddleOCR/tools/export_model.py -c ./text/typed_text/az_rec_config.yaml -o Global.pretrained_model=output/best_accuracy.pdparams Global.save_inference_dir=output/inference`

[//]: # (- REMOVE CTCLABELENCODE: null vim output/inference.yml does not work with it)

### 7. Modelin sınaqdan keçirilməsi

- Test skripti hazırlandı: `python .\testFast.py .\img.png`
- Orijinal və təlim keçmiş model nəticələrinin müqayisəsi

### 8. Brauzer genişləndirməsinin hazırlanması

- PaddleOCR-in brauzer genişləndirməsinə inteqrasiyası üçün server arxitekturası yaradıldı
- Funksionallıq `./image-to-text/ExtensionServerPaddleOCR` qovluğunda həyata keçirildi
- İnterfeysin yaradılması üçün JavaScript ilə işlər aparıldı
- Genişləndirmənin əsas funksionallığı işlək vəziyyətdədir