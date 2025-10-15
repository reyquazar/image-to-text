import paddle
params = paddle.load('./text/typed_text/pretrain_models/PP-OCRv5_server_rec_pretrained.pdparams')
print('Keys:', list(params.keys())[:5])
print('Total layers:', len(params))