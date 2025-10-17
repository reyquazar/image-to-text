import os
import subprocess

base_path = "../../../../image-to-text/text/typed_text/az_config_train"
subprocess.run([
    "python", "generate_multi_language_configs.py",
    "-l", "az",
    "--dict", f"{base_path}/dict.txt",
    "--train", f"{base_path}/train_list.txt",
    "--val", f"{base_path}/val_list.txt",
    "--data_dir", base_path
])
