import paddle
from ppocr.modeling.architectures import build_model
from ppocr.utils.save_load import load_model

# Загрузи конфиг и модель
from tools.program import load_config
config = load_config('debug_rec.yaml')
model = build_model(config['Architecture'])

# Загрузи веса
load_model(config, model)

# Сохрани в inference формате
model.eval()
model = paddle.jit.to_static(
    model,
    input_spec=[paddle.static.InputSpec(shape=[None, 3, 32, 320], dtype='float32')]
)
paddle.jit.save(model, 'output_inference/model')