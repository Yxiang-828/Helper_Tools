import os
import UnityPy

BYTES_BUNDLE = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\BytesData\Bytes.unity3d"
OUTPUT_DIR = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Original_Extraction"

print(f"Loading: {BYTES_BUNDLE}")
env = UnityPy.load(BYTES_BUNDLE)

# Iterate over all files inside the environment
for path, obj_reader in env.container.items():
    print(f"Container Path: {path}")

print(f"Objects count: {len(env.objects)}")
for obj in env.objects:
    if obj.type.name == "TextAsset":
        print(f"Found TextAsset: {obj.read().name}")
        data = obj.read()
        save_name = f"{data.name}.bytes"
        with open(os.path.join(OUTPUT_DIR, save_name), "wb") as f:
            f.write(data.script)

print("scan complete")
