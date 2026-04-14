import os

def hex_dump_manifest(file_path):
    print(f"Hex Dump: {os.path.basename(file_path)}")
    try:
        with open(file_path, 'rb') as f:
            head = f.read(256)
            print(head)
            print("---")
            print(head.hex())
    except:
        pass

hex_dump_manifest(r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\Document\Document.unity3d")
