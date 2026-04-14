import os

file_path = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\BytesData\Bytes.unity3d"

try:
    with open(file_path, 'rb') as f:
        header = f.read(16)
        print(f"Header: {header}")
        print(f"Hex: {header.hex()}")
except Exception as e:
    print(e)
