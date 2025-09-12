import torch

print({torch.cuda.is_available()})

print({torch.cuda.device_count()})

if torch.cuda.is_available():
    print(f"Название GPU: {torch.cuda.get_device_name(0)}")
    print(f"Память GPU: {torch.cuda.get_device_properties(0).total_memory / 1024 ** 3:.2f} GB")

    a = torch.tensor([1.0, 2.0, 3.0]).cuda()
    b = torch.tensor([4.0, 5.0, 6.0]).cuda()
    c = a + b
    print(f"Результат вычисления на GPU: {c}")
    print(f"Где находится тензор: {c.device}")
else:
    print("CUDA недоступна. Убедитесь, что установлены драйверы NVIDIA.")