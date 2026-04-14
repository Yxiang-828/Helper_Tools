import os
import UnityPy

PATH_JA = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets\LanResObj\LanResObj.unity3d"

def inspect_lang_bundle(bundle_path):
    print(f"Inspecting: {os.path.basename(bundle_path)}")
    env = UnityPy.load(bundle_path)
    for obj in env.objects:
        print(f" - Type: {obj.type.name} | ID: {obj.path_id}")

inspect_lang_bundle(PATH_JA)
