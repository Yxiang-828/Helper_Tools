import os
import UnityPy

# Paths
GAME_DATA_ROOT = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets"
BYTES_BUNDLE = os.path.join(GAME_DATA_ROOT, "BytesData", "Bytes.unity3d")
OUTPUT_DIR = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Original_Extraction"

def extract_assets(bundle_path, filter_name=None):
    if not os.path.exists(bundle_path):
        print(f"!! Bundle not found: {bundle_path}")
        return

    print(f"Loading bundle: {os.path.basename(bundle_path)}")
    env = UnityPy.load(bundle_path)
    
    for obj in env.objects:
        if obj.type.name == "TextAsset":
            data = obj.read()
            if filter_name and filter_name.lower() not in data.name.lower():
                continue
                
            # data.name often is just the name without extension, or verify script
            save_name = data.name
            if not save_name.endswith(".bytes"):
                save_name += ".bytes"
                
            save_path = os.path.join(OUTPUT_DIR, save_name)
            
            with open(save_path, "wb") as f:
                f.write(data.script)
            print(f"Extracted: {save_name}")

# 1. Extract Nair Core Logic from Bytes.unity3d
print("--- Extracting Core Logic ---")
extract_assets(BYTES_BUNDLE, "Nair")
extract_assets(BYTES_BUNDLE, "MaxSkill") 

# 2. Extract State Scripts (Nair specific bundles)
print("\n--- Extracting State Scripts ---")
state_script_dir = os.path.join(GAME_DATA_ROOT, "BytesData", "StateScript")
for file in os.listdir(state_script_dir):
    if "Nair" in file and file.endswith(".unity3d"):
        full_path = os.path.join(state_script_dir, file)
        extract_assets(full_path)
