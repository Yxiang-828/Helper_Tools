import os

def hex_head(file_path):
    print(f"Checking: {os.path.basename(file_path)}")
    try:
        with open(file_path, 'rb') as f:
            head = f.read(16)
            print(f"Magic: {head}")
            print(f"Hex:   {head.hex()}")
    except Exception as e:
        print(e)

file_path = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\BytesData\StateScript\20050_C_Nair_Attack.unity3d"
hex_head(file_path)
