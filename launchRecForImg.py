import os

commands = [
    "python testFast.py img.png > resimg.txt",
    "python testFast.py img_1.png > resimg1.txt",
    "python testFast.py img_2.png > resimg2.txt",
    "python testFast.py img_3.png > resimg3.txt"
]

for cmd in commands:
    os.system(cmd)
