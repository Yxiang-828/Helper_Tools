import os
import UnityPy

DOCUMENT_BUNDLE = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\Document\Document.unity3d"

def inspect(bundle_path):
    print(f"Inspecting: {os.path.basename(bundle_path)}")
    env = UnityPy.load(bundle_path)
    for obj in env.objects:
        print(f"Found: {obj.type.name}")

inspect(DOCUMENT_BUNDLE)
