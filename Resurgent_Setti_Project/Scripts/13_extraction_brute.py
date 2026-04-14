import os
import UnityPy

# Paths
GAME_DATA_ROOT = r"C:\Program Files (x86)\Silver And Blood\SilverAndBlood\SilverAndBlood_Data\StreamingAssets"
BYTES_BUNDLE = os.path.join(GAME_DATA_ROOT, "BytesData", "Bytes.unity3d")
OUTPUT_DIR = r"c:\Users\xiang\Helper_Tools\Resurgent_Setti_Project\Original_Extraction"

def extract_all_from_bundle(bundle_path):
    if not os.path.exists(bundle_path):
        print(f"!! Bundle not found: {bundle_path}")
        return

    print(f"Loading bundle: {os.path.basename(bundle_path)}")
    try:
        env = UnityPy.load(bundle_path)
        
        extracted_count = 0
        for obj in env.objects:
            if obj.type.name == "TextAsset":
                data = obj.read()
                
                # Save EVERY TextAsset to see what they are named internally
                # Prefix with bundle name to avoid collision/confusion
                bundle_name = os.path.basename(bundle_path).replace(".unity3d", "")
                save_name = f"{bundle_name}__{data.name}.bytes"
                
                # Clean up filename
                save_name = save_name.replace(" ", "_")
                
                save_path = os.path.join(OUTPUT_DIR, save_name)
                
                with open(save_path, "wb") as f:
                    f.write(data.script)
                extracted_count += 1
                
        print(f"  -> Extracted {extracted_count} assets from {os.path.basename(bundle_path)}")
    except Exception as e:
        print(f"Error reading {bundle_path}: {e}")

# 1. Extract EVERYTHING from Bytes.unity3d (to find C_Nair_Final)
# We will filter purely by file system checks later, for now we need to SEE what is inside.
# print("--- Extracting Core Logic ---")
# extract_all_from_bundle(BYTES_BUNDLE)

# 2. Extract State Scripts (Nair specific bundles)
print("\n--- Extracting State Scripts ---")
state_script_dir = os.path.join(GAME_DATA_ROOT, "BytesData", "StateScript")
for file in os.listdir(state_script_dir):
    if "Nair" in file and file.endswith(".unity3d"):
        full_path = os.path.join(state_script_dir, file)
        extract_all_from_bundle(full_path)
